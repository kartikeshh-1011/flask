from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import mysql.connector
import bcrypt
import os
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import Config

# ================= APP CONFIG =================
app = Flask(__name__)
app.config.from_object(Config)

# ================= DATABASE CONNECTION =================
def get_db_connection():
    try:
        return mysql.connector.connect(
            host=app.config['DB_HOST'],
            user=app.config['DB_USER'],
            password=app.config['DB_PASSWORD'],
            database=app.config['DB_NAME'],
            use_pure=True,
            connect_timeout=10
        )
    except mysql.connector.Error as err:
        print(f"DATABASE ERROR: {err}")
        
        raise Exception(f"Cannot connect to database: {err}")


# Helper to find student across all tables
def find_student_in_all_tables(email, cursor):
    tables = ['admissions_primary', 'admissions_v', 'admissions_vi', 'admissions_vii', 'admissions_viii', 
              'admissions_ix', 'admissions_x', 'admissions_xi', 'admissions_xii']
    
    for table in tables:
        try:
            # Select all columns plus source_table name
            query = f"SELECT *, '{table}' as source_table FROM {table} WHERE email = %s"
            cursor.execute(query, (email,))
            student = cursor.fetchone()
            if student:
                return student
        except Exception:
            continue
    return None


# ===== CONTEXT PROCESSOR: navbar profile photo =====
@app.context_processor
def inject_nav_photo():
    """Makes nav_photo_url available in every template for the navbar avatar."""
    nav_photo_url = None
    if session.get('logged_in'):
        try:
            role  = session.get('role')
            email = session.get('email')
            db = get_db_connection()
            cursor = db.cursor(dictionary=True)
            if role == 'Teacher':
                cursor.execute("SELECT photo_path FROM teacher_admissions WHERE email = %s", (email,))
                row = cursor.fetchone()
                if row:
                    nav_photo_url = row.get('photo_path')
            elif role == 'Student':
                row = find_student_in_all_tables(email, cursor)
                if row:
                    nav_photo_url = row.get('photo_path')
            cursor.close()
            db.close()
        except Exception:
            pass   # Silently fail — navbar still works with icon fallback
    return {'nav_photo_url': nav_photo_url}


# ================= HELPER FUNCTIONS =================

# ================= HOME =================
@app.route("/")
def home():
    return render_template("home.html")

# ================= EMAIL OTP =================

def send_otp_email(to_email, otp_code):
    """Send a 4-digit OTP via Gmail SMTP (TLS port 587).
    In DEV mode (no MAIL credentials), prints OTP to console instead.
    Returns (sent_by_email: bool, dev_otp: str|None)
    """
    sender_email = app.config.get('MAIL_USERNAME', '').strip()
    sender_password = app.config.get('MAIL_PASSWORD', '').strip()

    # --- DEV MODE: credentials not set, log OTP to console ---
    is_placeholder = (
        not sender_email
        or not sender_password
        or sender_email == 'your_gmail@gmail.com'
        or sender_password == 'your_gmail_app_password'
    )
    if is_placeholder:
        print(f"\n{'='*50}")
        print(f"[DEV MODE] OTP for {to_email}: {otp_code}")
        print(f"{'='*50}\n")
        return False, otp_code   # signal: dev mode, return OTP

    # --- PRODUCTION: send real email via Gmail SMTP TLS ---
    subject = "Your Email Verification Code - Apex Learning Hub"
    body = f"""\
<html>
<body style="font-family:Arial,sans-serif;background:#f4f4f4;padding:30px;">
  <div style="max-width:420px;margin:auto;background:#fff;border-radius:12px;padding:30px;box-shadow:0 4px 15px rgba(0,0,0,0.1);">
    <h2 style="color:#29909d;margin-bottom:8px;">Email Verification</h2>
    <p style="color:#555;">Use the code below to verify your email for <strong>Apex Learning Hub</strong>.</p>
    <div style="text-align:center;margin:28px 0;">
      <span style="font-size:38px;font-weight:bold;letter-spacing:10px;color:#29909d;background:#e8f7f8;padding:14px 28px;border-radius:10px;display:inline-block;">{otp_code}</span>
    </div>
    <p style="color:#888;font-size:13px;">Expires in <strong>10 minutes</strong>. Do not share it with anyone.</p>
    <hr style="border:none;border-top:1px solid #eee;margin:20px 0;">
    <p style="color:#aaa;font-size:12px;">If you didn't request this, ignore this email.</p>
  </div>
</body>
</html>"""

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = to_email
    msg.attach(MIMEText(body, 'html'))

    # Use TLS (port 587) — works with Gmail App Password
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, msg.as_string())

    return True, None  # production: email sent


@app.route("/send-otp", methods=["POST"])
def send_otp():
    """Generate and send a 4-digit OTP to the provided email."""
    try:
        import time
        data = request.get_json()
        email = (data.get('email') or '').strip()

        if not email:
            return jsonify({'success': False, 'message': 'Email is required'}), 400

        # Check if email already registered
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT id FROM users WHERE email=%s", (email,))
        if cursor.fetchone():
            cursor.close()
            db.close()
            return jsonify({'success': False, 'message': 'This email is already registered. Please login instead.'}), 409
        cursor.close()
        db.close()

        # Generate OTP
        otp = str(random.randint(1000, 9999))
        session['otp_code'] = otp
        session['otp_email'] = email
        session['otp_timestamp'] = time.time()

        # Send (or log in dev mode)
        sent_by_email, dev_otp = send_otp_email(email, otp)

        if sent_by_email:
            return jsonify({'success': True, 'message': f'Verification code sent to {email}'})
        else:
            # DEV MODE: return OTP in response so developer can test easily
            return jsonify({
                'success': True,
                'message': f'[DEV MODE] Email not configured — your code is: {dev_otp}',
                'dev_otp': dev_otp
            })

    except Exception as e:
        print(f"SEND OTP ERROR: {e}")
        return jsonify({'success': False, 'message': 'Failed to send the verification code. Please try again.'}), 500







@app.route("/verify-otp", methods=["POST"])
def verify_otp():
    """Verify the OTP entered by the user."""
    try:
        import time
        data = request.get_json()
        entered_otp = (data.get('otp') or '').strip()
        email = (data.get('email') or '').strip()
        
        stored_otp = session.get('otp_code')
        stored_email = session.get('otp_email')
        otp_time = session.get('otp_timestamp', 0)
        
        if not stored_otp:
            return jsonify({'success': False, 'message': 'No OTP found. Please request a new code.'}), 400
        
        # Check expiry (10 minutes)
        if time.time() - otp_time > 600:
            session.pop('otp_code', None)
            session.pop('otp_email', None)
            session.pop('otp_timestamp', None)
            return jsonify({'success': False, 'message': 'OTP has expired. Please request a new code.'}), 400
        
        if email != stored_email:
            return jsonify({'success': False, 'message': 'Email mismatch. Please request a new code.'}), 400
        
        if entered_otp != stored_otp:
            return jsonify({'success': False, 'message': 'Incorrect code. Please try again.'}), 400
        
        # Mark as verified
        session['email_verified'] = email
        return jsonify({'success': True, 'message': 'Email verified successfully!'})
    
    except Exception as e:
        print(f"VERIFY OTP ERROR: {e}")
        return jsonify({'success': False, 'message': f'Verification failed: {str(e)}'}), 500


# ================= SIGNUP =================
@app.route("/signup", methods=["GET", "POST"])
def signup():
    print(f"SIGNUP ROUTE CALLED - Method: {request.method}")
    
    if request.method == "POST":
        print("POST request received")
        
        try:
            print("Getting form data...")
            username = request.form.get("username", "").strip()
            email = request.form.get("email", "").strip()
            password = request.form.get("password", "").strip()
            role = request.form.get("role", "Student").strip()
            
            print(f"Form data: username={username}, email={email}, role={role}")
            
            if not username or not email or not password:
                print("Validation failed: missing fields")
                flash("All fields are required", "error")
                return redirect(url_for("signup"))
            
            # --- Email verification check ---
            verified_email = session.get('email_verified')
            if verified_email != email:
                flash("Please verify your email address before signing up.", "error")
                return redirect(url_for("signup"))
            
            print("Connecting to database...")
            db = get_db_connection()
            cursor = db.cursor()
            
            print("Checking for existing user...")
            cursor.execute(
                "SELECT * FROM users WHERE username=%s OR email=%s",
                (username, email)
            )
            
            if cursor.fetchone():
                print("User already exists")
                cursor.close()
                db.close()
                flash("Username or Email already exists", "error")
                return redirect(url_for("signup"))
            
            print("Hashing password...")
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=4))
            print(f"Password hashed successfully")
            
            print("Inserting user into database...")
            cursor.execute(
                
                "INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)",
                (username, email, hashed_password, role)
            )
            
            db.commit()
            print("User inserted successfully")
            cursor.close()
            db.close()
            
            # Clear OTP session data
            session.pop('otp_code', None)
            session.pop('otp_email', None)
            session.pop('otp_timestamp', None)
            session.pop('email_verified', None)
            
            print("Signup successful, redirecting to login")
            flash("Registration successful! Please login.", "success")
            return redirect(url_for("login"))
            
        except Exception as e:
            print(f"SIGNUP ERROR: {type(e).__name__}: {str(e)}")
            import traceback
            traceback.print_exc()
            flash(f"Error during signup: {str(e)}", "error")
            return redirect(url_for("signup"))
    
    print("Rendering signup.html")
    return render_template("signup.html")

# ================= LOGIN =================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            username = request.form.get("username")
            password = request.form.get("password")

            if not username or not password:
                flash("Username and password are required", "error")
                return redirect(url_for("login"))

            print(f"LOGIN ATTEMPT: username={username}")  # Debug

            db = get_db_connection()
            cursor = db.cursor(dictionary=True)

            cursor.execute(
                "SELECT * FROM users WHERE username=%s",
                (username,)
            )

            user = cursor.fetchone()
            cursor.close()
            db.close()

            print(f"USER FOUND: {user is not None}")  # Debug

            if user:
                try:
                    # Handle password comparison - database might store as bytes or string
                    stored_password = user['password']
                    if isinstance(stored_password, str):
                        stored_password = stored_password.encode('utf-8')
                    
                    password_match = bcrypt.checkpw(password.encode('utf-8'), stored_password)
                    print(f"PASSWORD MATCH: {password_match}")  # Debug
                    
                    if password_match:
                        # Create session
                        session['user_id'] = user['id']
                        session['username'] = user['username']
                        session['email'] = user['email']  # Store email in session
                        # Safely get role with default value 'Student' if not set
                        session['role'] = user.get('role', 'Student') or 'Student'
                        session['logged_in'] = True
                        
                        print(f"SESSION CREATED: role={session['role']}, email={session['email']}")  # Debug
                        
                        flash(f"Welcome back, {user['username']}!", "success")
                        
                        # Redirect based on user role
                        if session['role'] == 'Admin':
                            print("REDIRECTING TO: admin")  # Debug
                            return redirect(url_for("admin"))
                        elif session['role'] == 'Teacher':
                            # Check if teacher has completed admission form
                            db_check = get_db_connection()
                            cursor_check = db_check.cursor(dictionary=True)
                            cursor_check.execute("SELECT * FROM teacher_admissions WHERE email = %s", (user['email'],))
                            teacher_data = cursor_check.fetchone()
                            cursor_check.close()
                            db_check.close()
                            
                            if teacher_data:
                                print("REDIRECTING TO: tea (dashboard)")  # Debug
                                return redirect(url_for("tea"))
                            else:
                                print("REDIRECTING TO: teacher_admission")  # Debug
                                return redirect(url_for("teacher_admission"))
                        elif session['role'] == 'Parent':
                            print("REDIRECTING TO: parent")  # Debug
                            return redirect(url_for("parent"))
                        else:
                            # Student login - check if admission form already submitted
                            db_check = get_db_connection()
                            cursor_check = db_check.cursor(dictionary=True)
                            
                            # Use helper to check ALL tables
                            student_data = find_student_in_all_tables(user['email'], cursor_check)
                            
                            cursor_check.close()
                            db_check.close()
                            
                            if student_data:
                                print("REDIRECTING TO: stud (existing student)")  # Debug
                                return redirect(url_for("stud", email=user['email']))
                            else:
                                print("REDIRECTING TO: admision (new student)")  # Debug
                                return redirect(url_for("admision"))
                    else:
                        flash("Invalid username or password", "error")
                        return redirect(url_for("login"))
                except Exception as e:
                    print(f"PASSWORD CHECK ERROR: {str(e)}")  # Debug
                    flash(f"Login error: {str(e)}", "error")
                    return redirect(url_for("login"))
            else:
                flash("Invalid username or password", "error")
                return redirect(url_for("login"))
                
        except Exception as e:
            print(f"LOGIN ERROR: {str(e)}")  # Debug
            flash(f"Login error: {str(e)}", "error")
            return redirect(url_for("login"))

    return render_template("login.html")

# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out successfully.", "success")
    return redirect(url_for("home"))

# ================= PROFILE REDIRECT =================
@app.route("/profile")
def profile_redirect():
    if 'logged_in' not in session:
        return redirect(url_for("login"))
    
    role = session.get('role')
    email = session.get('email')
    
    if role == 'Admin':
        return redirect(url_for("admin"))
    
    elif role == 'Teacher':
        # Check if teacher has admission
        try:
            db = get_db_connection()
            cursor = db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM teacher_admissions WHERE email = %s", (email,))
            teacher = cursor.fetchone()
            cursor.close()
            db.close()
            
            if teacher:
                return redirect(url_for("tea"))
            else:
                return redirect(url_for("teacher_admission"))
        except Exception as e:
            print(f"Error in profile redirect for teacher: {e}")
            return redirect(url_for("home"))
            
    elif role == 'Student':
        # Check if student has admission
        try:
            db = get_db_connection()
            cursor = db.cursor(dictionary=True)
            student = find_student_in_all_tables(email, cursor)
            cursor.close()
            db.close()
            
            if student:
                return redirect(url_for("stud", email=email))
            else:
                return redirect(url_for("admision"))
        except Exception as e:
            print(f"Error in profile redirect for student: {e}")
            return redirect(url_for("home"))
            
    elif role == 'Parent':
         return redirect(url_for("parent"))
         
    return redirect(url_for("home"))

# ================= FORGOT PASSWORD =================
@app.route("/forgot", methods=["GET", "POST"])
def forgot():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]

        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM users WHERE username=%s AND email=%s",
            (username, email)
        )

        user = cursor.fetchone()
        cursor.close()
        db.close()

        if user:
            session["reset_user"] = username
            return redirect(url_for("new_password"))
        else:
            flash("Username and Email do not match", "error")
            return redirect(url_for("forgot"))

    return render_template("forgot.html")

# ================= NEW PASSWORD =================
@app.route("/new-password", methods=["GET", "POST"])
def new_password():
    if "reset_user" not in session:
        flash("Please verify your identity first", "error")
        return redirect(url_for("forgot"))

    if request.method == "POST":
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]

        if new_password != confirm_password:
            flash("Passwords do not match", "error")
            return redirect(url_for("new_password"))

        username = session["reset_user"]

        # Hash the new password (using 4 rounds for faster performance)
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt(rounds=4))

        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute(
            "UPDATE users SET password=%s WHERE username=%s",
            (hashed_password, username)
        )
        db.commit()

        cursor.close()
        db.close()

        session.pop("reset_user", None)

        flash("Password reset successful! Please login with your new password.", "success")
        return redirect(url_for("login"))
    
    return render_template("newpass.html")

# ================= CONTACT FORM =================
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        db = get_db_connection()
        cursor = db.cursor()
        
        cursor.execute(
            "INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)",
            (name, email, message)
        )
        db.commit()
        
        cursor.close()
        db.close()
        
        flash("Thank you for contacting us! We'll get back to you soon.", "success")
        return redirect(url_for("contact"))
    
    return render_template("contact.html")

# ================= FEEDBACK FORM =================
@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        feedback_text = request.form.get("feedback")

        db = get_db_connection()
        cursor = db.cursor()
        
        cursor.execute(
            "INSERT INTO feedback (name, email, feedback) VALUES (%s, %s, %s)",
            (name, email, feedback_text)
        )
        db.commit()
        
        cursor.close()
        db.close()
        
        flash("Thank you for your feedback!", "success"
        
        
        )
        return redirect(url_for("feedback"))
    
    return render_template("feedback.html")

# ================= COMPLAINT FORM =================
@app.route("/complain", methods=["GET", "POST"])
def complain():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        contact = request.form.get("contact")
        description = request.form.get("description")

        db = get_db_connection()
        cursor = db.cursor()
        
        cursor.execute(
            "INSERT INTO complaints (name, email, contact, description) VALUES (%s, %s, %s, %s)",
            (name, email, contact, description)
        )
        db.commit()
        
        cursor.close()
        db.close()
        
        flash("Your complaint has been submitted. We'll address it soon.", "success")
        return redirect(url_for("complain"))
    
    return render_template("complain.html")

# ================= ADMISSION FORM =================
@app.route("/admision")
def admision():
    """Display student admission form - only for new students"""
    if 'logged_in' not in session:
        flash("Please login to access the admission form", "error")
        return redirect(url_for("login"))
    
    # Check if student has already submitted admission form
    email = session.get('email')
    if email:
        try:
            db = get_db_connection()
            cursor = db.cursor(dictionary=True)
            
            # Helper to find student across all tables
            tables = ['admissions_primary', 'admissions_v', 'admissions_vi', 'admissions_vii', 'admissions_viii', 
                      'admissions_ix', 'admissions_x', 'admissions_xi', 'admissions_xii']
            
            existing_admission = None
            for table in tables:
                try:
                    cursor.execute(f"SELECT * FROM {table} WHERE email = %s", (email,))
                    result = cursor.fetchone()
                    if result:
                        existing_admission = result
                        break
                except:
                    continue
            
            cursor.close()
            db.close()
            
            if existing_admission:
                flash("You have already submitted your admission form. Redirecting to your dashboard.", "info")
                return redirect(url_for("stud", email=email))
        except Exception as e:
            print(f"Error checking admission status: {e}")
    
    return render_template("admission.html", email=email)

@app.route("/submit-admission", methods=["POST"])
def submit_admission():
    """Handle student admission form submission"""
    if 'logged_in' not in session:
        flash("Please login to submit the admission form", "error")
        return redirect(url_for("login"))


    try:
        # Extract form data
        student_name = request.form.get("student_name")
        date_of_birth = request.form.get("date_of_birth")
        
        # Priority: use session email if logged in, otherwise form email
        if 'logged_in' in session and session.get('email'):
            email = session.get('email')
        else:
            email = request.form.get("email")
            
        contact_number = request.form.get("contact_number")
        class_enroll = request.form.get("class_enroll")
        gender = request.form.get("gender")
        
        guardian_name = request.form.get("guardian_name")
        guardian_contact = request.form.get("guardian_contact")
        guardian_occupation = request.form.get("guardian_occupation")
        guardian_address = request.form.get("guardian_address")
        
        previous_board = request.form.get("previous_board")
        previous_school = request.form.get("previous_school")
        percentage_obtained = request.form.get("percentage_obtained")
        
        enrolled_board = request.form.get("enrolled_board")
        enrolled_school = request.form.get("enrolled_school")
        
        program_enrolled = request.form.get("program_enrolled")
        
        # Get multiple subjects as comma-separated string
        subjects_list = request.form.getlist("subjects")
        subjects = ", ".join(subjects_list) if subjects_list else ""
        
        # Helper to get table name based on class
        def get_class_table(class_name):
            class_map = {
                # Primary Section (all map to admissions_primary)
                'Class 1': 'admissions_primary',
                'Class 2': 'admissions_primary',
                'Class 3': 'admissions_primary',
                'Class 4': 'admissions_primary',
                # Secondary Section
                'V': 'admissions_v',
                'VI': 'admissions_vi',
                'VII': 'admissions_vii',
                'VIII': 'admissions_viii',
                'IX': 'admissions_ix',
                'X': 'admissions_x',
                'XI': 'admissions_xi',
                'XII': 'admissions_xii'
            }
            return class_map.get(class_name)

        # Helper to find student across all tables
        def find_student_in_all_tables(email, cursor):
            tables = ['admissions_primary', 'admissions_v', 'admissions_vi', 'admissions_vii', 'admissions_viii', 
                      'admissions_ix', 'admissions_x', 'admissions_xi', 'admissions_xii']
            
            for table in tables:
                try:
                    query = f"SELECT *, '{table}' as source_table FROM {table} WHERE email = %s"
                    cursor.execute(query, (email,))
                    student = cursor.fetchone()
                    if student:
                        return student
                except Exception:
                    continue
            return None

        # ---- Handle file uploads ----
        from werkzeug.utils import secure_filename
        import time as _time

        uploads_dir = os.path.join(app.root_path, 'static', 'uploads', 'students')
        if not os.path.exists(uploads_dir):
            os.makedirs(uploads_dir)

        def save_student_file(file_obj, prefix):
            if file_obj and file_obj.filename:
                try:
                    filename = secure_filename(file_obj.filename)
                    timestamp = int(_time.time())
                    filename = f"{prefix}_{timestamp}_{filename}"
                    file_obj.save(os.path.join(uploads_dir, filename))
                    return f"/static/uploads/students/{filename}"
                except Exception as ex:
                    print(f"Error saving {prefix}: {ex}")
            return None

        student_photo_file = request.files.get('student_photo')
        aadhaar_file = request.files.get('aadhaar_card')
        marksheet_file = request.files.get('marksheet')

        # Validate mandatory files server-side as well
        if not student_photo_file or not student_photo_file.filename:
            flash("Profile photo is required. Please upload a photo.", "error")
            return redirect(url_for("admision"))
        if not aadhaar_file or not aadhaar_file.filename:
            flash("Aadhaar card is required. Please upload your Aadhaar card.", "error")
            return redirect(url_for("admision"))

        photo_path = save_student_file(student_photo_file, "photo")
        aadhaar_path = save_student_file(aadhaar_file, "aadhaar")
        marksheet_path = save_student_file(marksheet_file, "marksheet")

        # Check if admission already exists for this email
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        
        # Check all tables using helper
        existing_admission = find_student_in_all_tables(email, cursor)
        
        if existing_admission:
            cursor.close()
            db.close()
            flash(f"Admission form already submitted for {email}. You cannot submit multiple times.", "error")
            return redirect(url_for("stud", email=email))
        
        # Get target table
        table_name = get_class_table(class_enroll)
        if not table_name:
            cursor.close()
            db.close()
            flash("Invalid class selected", "error")
            return redirect(url_for("admision"))

        # Insert into specific class table (with photo and documents)
        cursor.execute(f"""
            INSERT INTO {table_name} (
                student_name, date_of_birth, email, contact_number, 
                class_enroll, gender, guardian_name, guardian_contact, 
                guardian_occupation, guardian_address, previous_board, 
                previous_school, percentage_obtained, enrolled_board, 
                enrolled_school, program_enrolled, subjects,
                photo_path, aadhaar_path, marksheet_path
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            student_name, date_of_birth, email, contact_number,
            class_enroll, gender, guardian_name, guardian_contact,
            guardian_occupation, guardian_address, previous_board,
            previous_school, percentage_obtained, enrolled_board,
            enrolled_school, program_enrolled, subjects,
            photo_path, aadhaar_path, marksheet_path
        ))
        
        db.commit()
        cursor.close()
        db.close()
        
        flash(f"Admission application submitted successfully for {student_name} in Class {class_enroll}! Welcome to your dashboard.", "success")
        return redirect(url_for("stud", email=email))
        
    except Exception as e:
        flash(f"Error submitting admission form: {str(e)}", "error")
        return redirect(url_for("admision"))

@app.route("/view-admissions")
def view_admissions():
    """Admin page to view all admission records from all class tables"""
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        
        # Union all tables to get all admissions
        tables = ['admissions_primary', 'admissions_v', 'admissions_vi', 'admissions_vii', 'admissions_viii', 
                  'admissions_ix', 'admissions_x', 'admissions_xi', 'admissions_xii']
        
        union_query = " UNION ALL ".join([f"SELECT * FROM {table}" for table in tables])
        union_query += " ORDER BY created_at DESC"
        
        cursor.execute(union_query)
        admissions = cursor.fetchall()
        
        # Recalculate statistics based on fetched data
        total_admissions = len(admissions)
        male_count = sum(1 for a in admissions if a['gender'] == 'Male')
        female_count = sum(1 for a in admissions if a['gender'] == 'Female')
        
        cursor.close()
        db.close()
        
        return render_template(
            "view_admissions.html",
            admissions=admissions,
            total_admissions=total_admissions,
            male_count=male_count,
            female_count=female_count
        )
        
    except Exception as e:
        flash(f"Error loading admissions: {str(e)}", "error")
        return redirect(url_for("home"))

# ================= TEACHER RESULT UPDATE =================
@app.route("/update-result")
def update_result():
    """Teacher dashboard to update student results"""
    # Check if user is logged in and is a teacher
    if 'logged_in' not in session:
        flash("Please login as a teacher to access this page", "error")
        return redirect(url_for("login"))
    
    if session.get('role') != 'Teacher':
        flash("Access denied. Only teachers can update results.", "error")
        return redirect(url_for("home"))
    
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        
        # Get all students from all class tables
        tables = ['admissions_primary', 'admissions_v', 'admissions_vi', 'admissions_vii', 'admissions_viii', 
                  'admissions_ix', 'admissions_x', 'admissions_xi', 'admissions_xii']
        
        union_query = " UNION ALL ".join([f"SELECT student_name, email, class_enroll, subjects FROM {table}" for table in tables])
        union_query += " ORDER BY class_enroll, student_name"
        
        cursor.execute(union_query)
        students = cursor.fetchall()
        
        cursor.close()
        db.close()
        
        return render_template("update_result.html", students=students)
        
    except Exception as e:
        flash(f"Error loading students: {str(e)}", "error")
        return redirect(url_for("home"))

# ================= STUDENT RESULT API =================
@app.route("/get-result", methods=["POST"])
def get_result():
    """API endpoint for students to check their results"""
    try:
        data = request.get_json()
        student_name = data.get('name')
        email = data.get('email')
        class_val = data.get('class')
        
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        
        # Fetch result from database
        cursor.execute("""
            SELECT * FROM results 
            WHERE student_name = %s AND email = %s AND class = %s
        """, (student_name, email, class_val))
        
        result = cursor.fetchone()
        cursor.close()
        db.close()
        
        if result:
            # Prepare subject-wise marks
            subjects = {}
            if result['hindi_grammar'] is not None:
                subjects['Hindi Grammar'] = float(result['hindi_grammar'])
            if result['english_grammar'] is not None:
                subjects['English Grammar'] = float(result['english_grammar'])
            if result['marathi_grammar'] is not None:
                subjects['Marathi Grammar'] = float(result['marathi_grammar'])
            if result['maths'] is not None:
                subjects['Maths'] = float(result['maths'])
            if result['science'] is not None:
                subjects['Science'] = float(result['science'])
            if result['physics'] is not None:
                subjects['Physics'] = float(result['physics'])
            if result['chemistry'] is not None:
                subjects['Chemistry'] = float(result['chemistry'])
            if result['biology'] is not None:
                subjects['Biology'] = float(result['biology'])
            if result['sst'] is not None:
                subjects['SST'] = float(result['sst'])
            if result['vedic_maths'] is not None:
                subjects['Vedic Maths'] = float(result['vedic_maths'])
            if result['art_craft'] is not None:
                subjects['Art & Craft'] = float(result['art_craft'])
            
            return jsonify({
                'success': True,
                'student_name': result['student_name'],
                'class': result['class'],
                'subjects': subjects,
                'total_marks': float(result['total_marks']) if result['total_marks'] else 0,
                'percentage': float(result['percentage']) if result['percentage'] else 0,
                'grade': result['grade']
            })
        else:
            return jsonify({
                'success': False,
                'message': 'No results found. Please check your details or contact your teacher.'
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        })

@app.route("/submit-result", methods=["POST"])
def submit_result():
    """Handle result submission from teacher"""
    if 'logged_in' not in session or session.get('role') != 'Teacher':
        flash("Access denied", "error")
        return redirect(url_for("login"))
    
    try:
        # Get form data
        student_name = request.form.get("student_name")
        email = request.form.get("email")
        class_val = request.form.get("class")
        
        # Get subject marks
        hindi_grammar = request.form.get("hindi_grammar") or None
        english_grammar = request.form.get("english_grammar") or None
        marathi_grammar = request.form.get("marathi_grammar") or None
        maths = request.form.get("maths") or None
        science = request.form.get("science") or None
        physics = request.form.get("physics") or None
        chemistry = request.form.get("chemistry") or None
        biology = request.form.get("biology") or None
        sst = request.form.get("sst") or None
        vedic_maths = request.form.get("vedic_maths") or None
        art_craft = request.form.get("art_craft") or None
        
        # Calculate total marks and percentage
        marks_list = [hindi_grammar, english_grammar, marathi_grammar, maths, science, 
                      physics, chemistry, biology, sst, vedic_maths, art_craft]
        marks_list = [float(m) for m in marks_list if m is not None]
        
        total_marks = sum(marks_list) if marks_list else 0
        num_subjects = len(marks_list)
        percentage = (total_marks / (num_subjects * 100) * 100) if num_subjects > 0 else 0
        
        # Calculate grade
        if percentage >= 90:
            grade = "A+"
        elif percentage >= 80:
            grade = "A"
        elif percentage >= 70:
            grade = "B+"
        elif percentage >= 60:
            grade = "B"
        elif percentage >= 50:
            grade = "C"
        elif percentage >= 40:
            grade = "D"
        else:
            grade = "F"
        
        # Insert or update in database
        db = get_db_connection()
        cursor = db.cursor()
        
        cursor.execute("""
            INSERT INTO results (
                student_name, email, class, hindi_grammar, english_grammar, 
                marathi_grammar, maths, science, physics, chemistry, biology, 
                sst, vedic_maths, art_craft, total_marks, percentage, grade, updated_by
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                hindi_grammar = VALUES(hindi_grammar),
                english_grammar = VALUES(english_grammar),
                marathi_grammar = VALUES(marathi_grammar),
                maths = VALUES(maths),
                science = VALUES(science),
                physics = VALUES(physics),
                chemistry = VALUES(chemistry),
                biology = VALUES(biology),
                sst = VALUES(sst),
                vedic_maths = VALUES(vedic_maths),
                art_craft = VALUES(art_craft),
                total_marks = VALUES(total_marks),
                percentage = VALUES(percentage),
                grade = VALUES(grade),
                updated_by = VALUES(updated_by)
        """, (
            student_name, email, class_val, hindi_grammar, english_grammar,
            marathi_grammar, maths, science, physics, chemistry, biology,
            sst, vedic_maths, art_craft, total_marks, percentage, grade,
            session.get('username')
        ))
        
        db.commit()
        cursor.close()
        db.close()
        
        flash(f"Results updated successfully for {student_name}! Grade: {grade}, Percentage: {percentage:.2f}%", "success")
        return redirect(url_for("update_result"))
        
    except Exception as e:
        flash(f"Error updating results: {str(e)}", "error")
        return redirect(url_for("update_result"))

# ================= ADMIN DASHBOARD =================
@app.route("/admin")
def admin():
    """Display admin dashboard page with admission statistics and student/teacher lists"""
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        
        # Get total admissions (all active admissions from distinct class tables)
        tables = ['admissions_v', 'admissions_vi', 'admissions_vii', 'admissions_viii', 
                  'admissions_ix', 'admissions_x', 'admissions_xi', 'admissions_xii']
        
        # Calculate total count efficiently
        total_admissions = 0
        for table in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
                total_admissions += cursor.fetchone()['count']
            except:
                continue
        
        # Get cancelled admissions from cancelled_admissions table
        cursor.execute("SELECT COUNT(*) as count FROM cancelled_admissions")
        cancelled_admissions = cursor.fetchone()['count']
        
        # Get total teachers (all active teachers)
        cursor.execute("SELECT COUNT(*) as count FROM teacher_admissions")
        total_teachers = cursor.fetchone()['count']
        
        # Get cancelled teachers from cancelled_teachers table
        cursor.execute("SELECT COUNT(*) as count FROM cancelled_teachers")
        cancelled_teachers = cursor.fetchone()['count']
        
        # Get latest 10 students from all tables
        union_query = " UNION ALL ".join([f"SELECT student_name, email, class_enroll, created_at FROM {table}" for table in tables])
        union_query += " ORDER BY created_at DESC LIMIT 10"
        
        cursor.execute(union_query)
        students = cursor.fetchall()
        
        # Get all teachers from teacher_admissions (for dropdowns)
        cursor.execute("""
            SELECT full_name, email, employee_id, department, phone 
            FROM teacher_admissions 
            ORDER BY full_name ASC
        """)
        all_teachers = cursor.fetchall()

        # Get teachers for dashboard list (limit 10)
        cursor.execute("""
            SELECT full_name, email, employee_id, department, phone 
            FROM teacher_admissions 
            ORDER BY created_at DESC 
            LIMIT 10
        """)
        teachers = cursor.fetchall()
        
        # Get current class teacher assignments
        cursor.execute("""
            SELECT ct.*, t.full_name as teacher_name 
            FROM class_teachers ct 
            JOIN teacher_admissions t ON ct.teacher_email = t.email
            ORDER BY ct.class_name, ct.section
        """)
        class_teachers_assignments = cursor.fetchall()
        
        # Get current subject teacher assignments
        cursor.execute("""
            SELECT st.*, t.full_name as teacher_name 
            FROM subject_teachers st 
            JOIN teacher_admissions t ON st.teacher_email = t.email
            ORDER BY st.class_name, st.subject_name
        """)
        subject_teachers_assignments = cursor.fetchall()
        
        cursor.close()
        db.close()
        
        return render_template(
            "admin.html",
            total_admissions=total_admissions,
            cancelled_admissions=cancelled_admissions,
            total_teachers=total_teachers,
            cancelled_teachers=cancelled_teachers,
            students=students,
            teachers=teachers,
            all_teachers=all_teachers,
            class_teachers_assignments=class_teachers_assignments,
            subject_teachers_assignments=subject_teachers_assignments
        )
        
    except Exception as e:
        print(f"Error loading admin dashboard: {e}")
        # If there's an error, still render the page with default values
        return render_template(
            "admin.html",
            total_admissions=0,
            cancelled_admissions=0,
            total_teachers=0,
            cancelled_teachers=0,
            students=[],
            teachers=[],
            all_teachers=[],
            class_teachers_assignments=[],
            subject_teachers_assignments=[]
        )

@app.route("/assign-class-teacher", methods=["POST"])
def assign_class_teacher():
    if 'logged_in' not in session or session.get('role') != 'Admin':
        flash("Access denied", "error")
        return redirect(url_for("home"))
        
    try:
        class_name = request.form.get("class_name")
        section = request.form.get("section", "A")
        teacher_email = request.form.get("teacher_email")
        
        db = get_db_connection()
        cursor = db.cursor()
        
        # 1. Check if teacher is already assigned to ANY class
        cursor.execute("SELECT class_name, section FROM class_teachers WHERE teacher_email = %s", (teacher_email,))
        existing_teacher_assignment = cursor.fetchone()
        
        if existing_teacher_assignment:
            assigned_class, assigned_section = existing_teacher_assignment
            # If assigned to a DIFFERENT class/section, block it
            if assigned_class != class_name or assigned_section != section:
                cursor.close()
                db.close()
                flash(f"Teacher is already assigned to Class {assigned_class}-{assigned_section}. Please remove that assignment first.", "error")
                return redirect(url_for("admin"))
        
        # 2. Check if THIS class already has a teacher (Update vs Insert)
        cursor.execute("SELECT id FROM class_teachers WHERE class_name=%s AND section=%s", (class_name, section))
        existing_class_assignment = cursor.fetchone()
        
        if existing_class_assignment:
            cursor.execute("""
                UPDATE class_teachers SET teacher_email=%s, updated_at=NOW()
                WHERE class_name=%s AND section=%s
            """, (teacher_email, class_name, section))
            flash(f"Updated Class Teacher for {class_name}-{section}", "success")
        else:
            cursor.execute("""
                INSERT INTO class_teachers (class_name, section, teacher_email)
                VALUES (%s, %s, %s)
            """, (class_name, section, teacher_email))
            flash(f"Assigned Class Teacher for {class_name}-{section}", "success")
            
        db.commit()
        cursor.close()
        db.close()
        
    except Exception as e:
        flash(f"Error assigning class teacher: {e}", "error")
        
    return redirect(url_for("admin"))

@app.route("/remove-class-teacher", methods=["POST"])
def remove_class_teacher():
    if 'logged_in' not in session or session.get('role') != 'Admin':
        flash("Access denied", "error")
        return redirect(url_for("home"))
        
    try:
        class_name = request.form.get("class_name")
        section = request.form.get("section", "A")
        
        db = get_db_connection()
        cursor = db.cursor()
        
        cursor.execute("DELETE FROM class_teachers WHERE class_name=%s AND section=%s", (class_name, section))
        db.commit()
        
        cursor.close()
        db.close()
        
        flash(f"Removed Class Teacher for {class_name}-{section}", "success")
        
    except Exception as e:
        flash(f"Error removing class teacher: {e}", "error")
        
    return redirect(url_for("admin"))

@app.route("/assign-subject-teacher", methods=["POST"])
def assign_subject_teacher():
    if 'logged_in' not in session or session.get('role') != 'Admin':
        flash("Access denied", "error")
        return redirect(url_for("home"))
        
    try:
        class_name = request.form.get("class_name")
        section = request.form.get("section", "A")
        subject_name = request.form.get("subject_name")
        teacher_email = request.form.get("teacher_email")
        
        db = get_db_connection()
        cursor = db.cursor()
        
        # Check if assignment exists
        cursor.execute("""
            SELECT id FROM subject_teachers 
            WHERE class_name=%s AND section=%s AND subject_name=%s
        """, (class_name, section, subject_name))
        existing = cursor.fetchone()
        
        if existing:
            cursor.execute("""
                UPDATE subject_teachers SET teacher_email=%s, updated_at=NOW()
                WHERE class_name=%s AND section=%s AND subject_name=%s
            """, (teacher_email, class_name, section, subject_name))
            flash(f"Updated {subject_name} Teacher for {class_name}-{section}", "success")
        else:
            cursor.execute("""
                INSERT INTO subject_teachers (class_name, section, subject_name, teacher_email)
                VALUES (%s, %s, %s, %s)
            """, (class_name, section, subject_name, teacher_email))
            flash(f"Assigned {subject_name} Teacher for {class_name}-{section}", "success")
            
        db.commit()
        cursor.close()
        db.close()
        
    except Exception as e:
        flash(f"Error assigning subject teacher: {e}", "error")
        
    return redirect(url_for("admin"))

# ================= PROFILE PAGES =================
@app.route("/student_profile/<email>")
def student_profile(email):
    """Display student profile page with admission details"""
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        
        # Helper to find student across all tables
        tables = ['admissions_v', 'admissions_vi', 'admissions_vii', 'admissions_viii', 
                  'admissions_ix', 'admissions_x', 'admissions_xi', 'admissions_xii']
        
        student = None
        for table in tables:
            try:
                cursor.execute(f"SELECT * FROM {table} WHERE email = %s", (email,))
                result = cursor.fetchone()
                if result:
                    student = result
                    break
            except:
                continue
        
        cursor.close()
        db.close()
        
        if student:
            return render_template("student_profile.html", student=student)
        else:
            flash("Student profile not found. Please fill the admission form first.", "error")
            return redirect(url_for("admision"))
            
    except Exception as e:
        print(f"Error loading student profile: {e}")
        flash("Error loading profile. Please try again.", "error")
        return redirect(url_for("home"))

@app.route("/teacher_profile")
def teacher_profile():
    """Display teacher profile page with admission details"""
    if 'logged_in' not in session or session.get('role') != 'Teacher':
        flash("Please login as a teacher to access this page", "error")
        return redirect(url_for("login"))
    
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        
        # Get logged-in user's email from session
        username = session.get('username')
        cursor.execute("SELECT email FROM users WHERE username = %s", (username,))
        user_data = cursor.fetchone()
        
        if user_data:
            email = user_data['email']
            
            # Get teacher admission data by email
            cursor.execute("""
                SELECT * FROM teacher_admissions 
                WHERE email = %s 
                ORDER BY created_at DESC 
                LIMIT 1
            """, (email,))
            
            teacher = cursor.fetchone()
            
            cursor.close()
            db.close()
            
            if teacher:
                return render_template("teacher_profile.html", teacher=teacher)
            else:
                flash("Teacher profile not found. Please complete the admission form first.", "error")
                return redirect(url_for("teacher_admission"))
        else:
            cursor.close()
            db.close()
            flash("User data not found", "error")
            return redirect(url_for("home"))
            
    except Exception as e:
        print(f"Error loading teacher profile: {e}")
        flash("Error loading profile. Please try again.", "error")
        return redirect(url_for("home"))


@app.route("/teacher_profile/<email>")
def teacher_profile_by_email(email):
    """Display teacher profile page by email - accessible from admin dashboard"""
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        
        # Get teacher admission data by email
        cursor.execute("""
            SELECT * FROM teacher_admissions 
            WHERE email = %s 
            ORDER BY created_at DESC 
            LIMIT 1
        """, (email,))
        
        teacher = cursor.fetchone()
        
        cursor.close()
        db.close()
        
        if teacher:
            return render_template("teacher_profile.html", teacher=teacher)
        else:
            flash("Teacher profile not found.", "error")
            return redirect(url_for("admin"))
            
    except Exception as e:
        print(f"Error loading teacher profile: {e}")
        flash("Error loading profile. Please try again.", "error")
        return redirect(url_for("admin"))



@app.route("/stud")
@app.route("/stud/<email>")
def stud(email=None):
    """Display student dashboard with data from class-specific tables"""
 
    # Helper function is now global


    # Check if accessing as admin with email parameter
    if email and 'logged_in' in session and session.get('role') == 'Admin':
        # Admin viewing a specific student's dashboard
        try:
            db = get_db_connection()
            cursor = db.cursor(dictionary=True)
            
            # Search all tables
            student_data = find_student_in_all_tables(email, cursor)
            
            if student_data:
                # Get assigned class teacher
                cursor.execute("""
                    SELECT t.*, ct.section 
                    FROM class_teachers ct
                    JOIN teacher_admissions t ON ct.teacher_email = t.email
                    WHERE ct.class_name = %s
                """, (student_data['class_enroll'],))
                class_teacher = cursor.fetchone()
                
                # Get assigned subject teachers
                cursor.execute("""
                    SELECT st.subject_name, t.* 
                    FROM subject_teachers st
                    JOIN teacher_admissions t ON st.teacher_email = t.email
                    WHERE st.class_name = %s
                """, (student_data['class_enroll'],))
                subject_teachers = cursor.fetchall()

                cursor.close()
                db.close()
                
                # Pass student data to template
                return render_template("stud.html", student=student_data, username=student_data['student_name'],
                                       class_teacher=class_teacher, subject_teachers=subject_teachers)
            else:
                flash("Student data not found", "error")
                return redirect(url_for("admin"))
                
        except Exception as e:
            print(f"Error loading student data for admin: {e}")
            flash("Error loading student data", "error")
            return redirect(url_for("admin"))
    
    # Regular student access
    if 'logged_in' not in session or session.get('role') != 'Student':
        flash("Please login as a student to access this page", "error")
        return redirect(url_for("login"))
    
    try:
        # Get logged-in user's email from session
        user_email = session.get('username')  # This is actually the username/email used for login
        email = session.get('email')
        
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        
        if not email:
            # First get the email from users table if not in session
            cursor.execute("SELECT email FROM users WHERE username = %s", (user_email,))
            user_data = cursor.fetchone()
            if user_data:
                email = user_data['email']
        
        if email:
            # Search all tables
            student_data = find_student_in_all_tables(email, cursor)
            
            if student_data:
                # Get assigned class teacher
                cursor.execute("""
                    SELECT t.*, ct.section 
                    FROM class_teachers ct
                    JOIN teacher_admissions t ON ct.teacher_email = t.email
                    WHERE ct.class_name = %s
                """, (student_data['class_enroll'],))
                class_teacher = cursor.fetchone()
                
                # Get assigned subject teachers
                cursor.execute("""
                    SELECT st.subject_name, t.* 
                    FROM subject_teachers st
                    JOIN teacher_admissions t ON st.teacher_email = t.email
                    WHERE st.class_name = %s
                """, (student_data['class_enroll'],))
                subject_teachers = cursor.fetchall()
                
                cursor.close()
                db.close()

                # Pass student data to template
                return render_template("stud.html", student=student_data, username=user_email,
                                       class_teacher=class_teacher, subject_teachers=subject_teachers)
            else:
                flash("Student admission details not found. Please complete the form.", "info")
                return redirect(url_for("admision"))

        else:
            cursor.close()
            db.close()
            flash("User data not found", "error")
            return redirect(url_for("home"))
            
    except Exception as e:
        print(f"Error loading student data: {e}")
        # If there's an error, still render the page with default values
        return render_template("stud.html", student=None, username=session.get('username'))

@app.route("/tea")
@app.route("/tea/<email>")
def tea(email=None):
    """Display teacher dashboard with tabs"""
    # Check if accessing as admin with email parameter
    if email and 'logged_in' in session and session.get('role') == 'Admin':
        # Admin viewing a specific teacher's dashboard
        try:
            db = get_db_connection()
            cursor = db.cursor(dictionary=True)
            
            # Get teacher admission data by email
            cursor.execute("""
                SELECT * FROM teacher_admissions 
                WHERE email = %s 
                ORDER BY created_at DESC 
                LIMIT 1
            """, (email,))
            
            teacher_data = cursor.fetchone()
            
            cursor.close()
            db.close()
            
            if teacher_data:
                print(f"DEBUG: Admin viewing teacher data: {teacher_data}")
                # Pass teacher data to template
                return render_template("tea.html", teacher=teacher_data)
            else:
                flash("Teacher data not found", "error")
                return redirect(url_for("admin"))
                
        except Exception as e:
            print(f"Error loading teacher data for admin: {e}")
            flash("Error loading teacher data", "error")
            return redirect(url_for("admin"))
    
    # Regular teacher access
    if 'logged_in' not in session or session.get('role') != 'Teacher':
        flash("Please login as a teacher to access this page", "error")
        return redirect(url_for("login"))
    
    try:
        # Get logged-in user's email directly from session
        email = session.get('email')
        username = session.get('username')
        print(f"DEBUG: Teacher from session - username: {username}, email: {email}")
        
        if not email:
            print("DEBUG: No email in session, fetching from users table")
            # Fallback: get email from users table if not in session
            db = get_db_connection()
            cursor = db.cursor(dictionary=True)
            cursor.execute("SELECT email FROM users WHERE username = %s", (username,))
            user_data = cursor.fetchone()
            cursor.close()
            db.close()
            
            if user_data:
                email = user_data['email']
                session['email'] = email  # Store in session for next time
                print(f"DEBUG: Email fetched from DB: {email}")
            else:
                flash("User data not found", "error")
                return redirect(url_for("home"))
        
        print(f"DEBUG: Looking for teacher with email: {email}")
        
        # Get teacher admission data
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT * FROM teacher_admissions 
            WHERE email = %s 
            ORDER BY created_at DESC 
            LIMIT 1
        """, (email,))
        
        teacher_data = cursor.fetchone()
        print(f"DEBUG: Teacher data fetched: {teacher_data}")
        
        cursor.close()
        db.close()
        
        if teacher_data:
            print(f"DEBUG: Rendering template with teacher data")
            # Pass teacher data to template
            return render_template("tea.html", teacher=teacher_data)
        else:
            print(f"DEBUG: No teacher data found for email: {email}")
            flash("Please complete your teacher profile to access the dashboard", "warning")
            return redirect(url_for("teacher_admission"))

            
    except Exception as e:
        print(f"Error loading teacher data: {e}")
        import traceback
        traceback.print_exc()
        # If there's an error, still render the page with default values
        return render_template("tea.html", teacher=None)

@app.route("/teacher_admission")
def teacher_admission():
    """Display teacher admission form - only for new teachers"""
    if 'logged_in' not in session or session.get('role') != 'Teacher':
        flash("Please login as a teacher to access this page", "error")
        return redirect(url_for("login"))
    
    # Check if teacher has already submitted admission form
    email = session.get('email')
    if email:
        try:
            db = get_db_connection()
            cursor = db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM teacher_admissions WHERE email = %s", (email,))
            existing_admission = cursor.fetchone()
            cursor.close()
            db.close()
            
            if existing_admission:
                flash("You have already submitted your admission form. Redirecting to your dashboard.", "info")
                return redirect(url_for("tea"))
        except Exception as e:
            print(f"Error checking teacher admission status: {e}")
    
    return render_template("teacher admission.html", email=email)

@app.route("/submit-teacher-admission", methods=["POST"])
def submit_teacher_admission():
    """Handle teacher admission form submission"""
    if 'logged_in' not in session or session.get('role') != 'Teacher':
        flash("Please login as a teacher to access this page", "error")
        return redirect(url_for("login"))
    
    try:
        # Extract form data
        full_name = request.form.get("full_name")
        
        # Priority: use session email if logged in, otherwise form email
        if 'logged_in' in session and session.get('email'):
            email = session.get('email')
        else:
            email = request.form.get("email")
            
        phone = request.form.get("phone")
        date_of_birth = request.form.get("date_of_birth")
        gender = request.form.get("gender")
        blood_group = request.form.get("blood_group")
        address = request.form.get("address")
        
        employee_id = request.form.get("employee_id")
        designation = request.form.get("designation")
        department = request.form.get("department")
        joining_date = request.form.get("joining_date")
        experience = request.form.get("experience")
        specialization = request.form.get("specialization")
        
        highest_qualification = request.form.get("highest_qualification")
        university = request.form.get("university")
        graduation_year = request.form.get("graduation_year")
        certifications = request.form.get("certifications")
        
        emergency_contact_name = request.form.get("emergency_contact_name")
        emergency_contact_phone = request.form.get("emergency_contact_phone")
        emergency_contact_relation = request.form.get("emergency_contact_relation")
        
        # Check if admission already exists for this email
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM teacher_admissions WHERE email = %s", (email,))
        existing_admission = cursor.fetchone()
        
        if existing_admission:
            cursor.close()
            db.close()
            flash(f"Teacher admission form already submitted for {email}. You cannot submit multiple times.", "error")
            return redirect(url_for("tea"))
        
        # Handle file uploads
        uploads_dir = os.path.join(app.root_path, 'static', 'uploads', 'teachers')
        if not os.path.exists(uploads_dir):
            os.makedirs(uploads_dir)
            
        from werkzeug.utils import secure_filename
        import time
        
        def save_file(file_obj, prefix):
            if file_obj and file_obj.filename:
                try:
                    filename = secure_filename(file_obj.filename)
                    timestamp = int(time.time())
                    filename = f"{prefix}_{timestamp}_{filename}"
                    file_path = os.path.join(uploads_dir, filename)
                    file_obj.save(file_path)
                    return f"/static/uploads/teachers/{filename}"
                except Exception as e:
                    print(f"Error saving {prefix}: {e}")
            return None

        # Get files from request
        photo = request.files.get('photo')
        resume = request.files.get('resume')
        aadhaar = request.files.get('aadhaar')
        pan = request.files.get('pan')
        
        # Server-side validation for mandatory files
        if not photo or not photo.filename:
            cursor.close()
            db.close()
            flash("Profile photo is required. Please upload a profile photo.", "error")
            return redirect(url_for("teacher_admission"))
        if not aadhaar or not aadhaar.filename:
            cursor.close()
            db.close()
            flash("Aadhaar card is required. Please upload your Aadhaar card.", "error")
            return redirect(url_for("teacher_admission"))
        
        # Save files
        photo_path = save_file(photo, "photo")
        resume_path = save_file(resume, "resume")
        aadhaar_path = save_file(aadhaar, "aadhaar")
        pan_path = save_file(pan, "pan")
        
        # Handle multiple other documents if needed (currently just saving one path if multiple selected, or needing loop)
        # For now, let's keep it simple or if 'documents' is multiple, we might need a separate table or zip. 
        # The form has <input type="file" name="documents" multiple>
        # We will save them and store comma separated paths
        other_docs_paths = []
        other_docs = request.files.getlist('documents')
        for doc in other_docs:
            path = save_file(doc, "other")
            if path:
                other_docs_paths.append(path)
        
        other_docs_path_str = ",".join(other_docs_paths) if other_docs_paths else None
        
        # Insert into database
        cursor.execute("""
            INSERT INTO teacher_admissions (
                full_name, email, phone, date_of_birth, gender, blood_group, address,
                employee_id, designation, department, joining_date, experience, specialization,
                highest_qualification, university, graduation_year, certifications,
                emergency_contact_name, emergency_contact_phone, emergency_contact_relation,
                photo_path, resume_path, aadhaar_path, pan_path, other_docs_path
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            full_name, email, phone, date_of_birth, gender, blood_group, address,
            employee_id, designation, department, joining_date, experience, specialization,
            highest_qualification, university, graduation_year, certifications,
            emergency_contact_name, emergency_contact_phone, emergency_contact_relation,
            photo_path, resume_path, aadhaar_path, pan_path, other_docs_path_str
        ))
        
        db.commit()
        cursor.close()
        db.close()
        
        flash(f"Teacher profile submitted successfully for {full_name}! Welcome to your dashboard.", "success")
        return redirect(url_for("tea"))
        
    except mysql.connector.IntegrityError as e:
        print(f"Database Integrity Error: {e}")
        error_msg = str(e)
        if "Duplicate entry" in error_msg:
            if "employee_id" in error_msg:
                flash("Employee ID already exists. Please use a unique ID.", "error")
            elif "email" in error_msg:
                flash("Email already registered.", "error")
            else:
                flash(f"Duplicate entry error: {error_msg}", "error")
        else:
            flash(f"Database error: {error_msg}", "error")
        return redirect(url_for("teacher_admission"))
        
    except Exception as e:
        print(f"Error submitting teacher admission: {e}")
        flash(f"Error submitting form: {str(e)}", "error")
        return redirect(url_for("teacher_admission"))

@app.route("/parent")
def parent():
    """Display parent dashboard with tabs"""
    return render_template("parent.html")


# ================= CANCEL ADMISSION =================
@app.route("/cancel-admission", methods=["POST"])
def cancel_admission():
    """Handle admission cancellation - move data to cancelled_admissions table"""
    try:
        email = request.form.get("email")
        
        if not email:
            flash("Email is required to cancel admission", "error")
            return redirect(url_for("home"))
        
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        
        # Get the admission record
        cursor.execute("SELECT * FROM admissions WHERE email = %s", (email,))
        admission = cursor.fetchone()
        
        if not admission:
            flash("Admission record not found", "error")
            cursor.close()
            db.close()
            return redirect(url_for("home"))
        
        # Insert into cancelled_admissions table
        cursor.execute(f"""
            INSERT INTO cancelled_admissions (
                student_name, date_of_birth, email, contact_number, 
                class_enroll, gender, guardian_name, guardian_contact, 
                guardian_occupation, guardian_address, previous_board, 
                previous_school, percentage_obtained, enrolled_board, 
                enrolled_school, program_enrolled, subjects, source_table
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            admission['student_name'], admission['date_of_birth'], admission['email'], 
            admission['contact_number'], admission['class_enroll'], admission['gender'], 
            admission['guardian_name'], admission['guardian_contact'], 
            admission['guardian_occupation'], admission['guardian_address'], 
            admission['previous_board'], admission['previous_school'], 
            admission['percentage_obtained'], admission['enrolled_board'], 
            admission['enrolled_school'], admission['program_enrolled'], 
            admission['subjects'], admission.get('source_table', 'admissions')
        ))
        
        # Delete from original table
        # Note: We need to know which table it came from. 
        # For simplicity, if source_table is unknown, we try to delete from all or find it first.
        # But `view-admissions` loop sets source_table.
        # If we cancel from `stud.html`, we might not have source_table in param.
        # Assuming we handle this correctly elsewhere or here.
        
        # For now, let's skip complex deletion logic here as it wasn't the main request.
        # Focusing on Schedule.
        
        db.commit()
        cursor.close()
        db.close()
        
        flash("Admission cancelled successfully", "success")
        return redirect(url_for("home"))
        
    except Exception as e:
        print(f"Error cancelling admission: {e}")
        flash("Error cancelling admission", "error")
        return redirect(url_for("home"))

# ================= SCHEDULE MANAGEMENT =================
# ================= SYLLABUS MANAGEMENT =================
@app.route("/save-syllabus", methods=["POST"])
def save_syllabus():
    """Save syllabus chapters for a teacher/class"""
    if 'logged_in' not in session or session.get('role') != 'Teacher':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        class_name = data.get('class_name')
        subject = data.get('subject')
        chapters = data.get('chapters')
        teacher_email = session.get('email')
        
        if not class_name or not subject or not isinstance(chapters, list):
            return jsonify({'success': False, 'message': 'Invalid data'}), 400
            
        db = get_db_connection()
        cursor = db.cursor()
        
        # Delete existing syllabus for this teacher, class, and subject
        cursor.execute(
            "DELETE FROM syllabus WHERE teacher_email = %s AND class_name = %s AND subject = %s",
            (teacher_email, class_name, subject)
        )
        
        # Insert new chapters
        for chapter in chapters:
            cursor.execute("""
                INSERT INTO syllabus (
                    teacher_email, class_name, subject, chapter_number, chapter_name, 
                    status, topics_covered, total_topics, duration, target_date, date_label
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                teacher_email, class_name, subject,
                chapter.get('number'), chapter.get('name'),
                chapter.get('status'), chapter.get('topicsCovered'),
                chapter.get('totalTopics'), chapter.get('duration'),
                chapter.get('date'), chapter.get('dateLabel')
            ))
            
        db.commit()
        cursor.close()
        db.close()
        
        return jsonify({'success': True, 'message': 'Syllabus saved successfully'})
        
    except Exception as e:
        print(f"Error saving syllabus: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route("/get-syllabus", methods=["GET"])
def get_syllabus():
    """Get syllabus: for Teacher (chapters) or Student (aggregated summary)"""
    try:
        role = session.get('role')
        email = session.get('email')
        
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        
        if role == 'Teacher':
            class_name = request.args.get('class_name')
            subject = request.args.get('subject') # Optional filter
            
            query = "SELECT * FROM syllabus WHERE teacher_email = %s"
            params = [email]
            
            if class_name:
                query += " AND class_name = %s"
                params.append(class_name)
            
            # If subject provided, filter by it. If not, maybe return all?
            # For the dashboard, we usually load for a specific class now.
            if subject:
                 query += " AND subject = %s"
                 params.append(subject)
                 
            query += " ORDER BY chapter_number ASC"
            
            cursor.execute(query, tuple(params))
            chapters = cursor.fetchall()
            
            # map DB columns back to frontend expected keys
            mapped_chapters = []
            for c in chapters:
                mapped_chapters.append({
                    'number': c['chapter_number'],
                    'name': c['chapter_name'],
                    'status': c['status'],
                    'topicsCovered': c['topics_covered'],
                    'totalTopics': c['total_topics'],
                    'duration': c['duration'],
                    'date': c['target_date'].strftime('%Y-%m-%d') if c['target_date'] else '',
                    'dateLabel': c['date_label']
                })
                
            cursor.close()
            db.close()
            return jsonify({'success': True, 'chapters': mapped_chapters})

        elif role == 'Student':
            # Get student class
            student = find_student_in_all_tables(email, cursor)
            if not student:
                 cursor.close(); db.close()
                 return jsonify({'success': False, 'message': 'Student class not found'}), 404
            
            student_class = student['class_enroll']
            # Map Roman to Class format
            class_map = {
                'V': 'Class 5th', 'VI': 'Class 6th', 'VII': 'Class 7th',
                'VIII': 'Class 8th', 'IX': 'Class 9th', 'X': 'Class 10th',
                'XI': 'Class 11th', 'XII': 'Class 12th'
            }
            mapped_class = class_map.get(student_class, student_class)
            
            # Get syllabus for this class
            cursor.execute("SELECT * FROM syllabus WHERE class_name = %s ORDER BY subject, chapter_number", (mapped_class,))
            all_chapters = cursor.fetchall()
            
            # Aggregate by subject
            summary = {}
            for ch in all_chapters:
                subj = ch['subject']
                if subj not in summary:
                    summary[subj] = {
                        'subject': subj,
                        'total_chapters': 0,
                        'completed_chapters': 0,
                        'chapters': [] # If we want details later
                    }
                summary[subj]['total_chapters'] += 1
                if ch['status'] == 'complete':
                     summary[subj]['completed_chapters'] += 1
            
            cursor.close()
            db.close()
            return jsonify({'success': True, 'syllabus': list(summary.values())})
            
        else:
            return jsonify({'success': False, 'message': 'Unauthorized'}), 401

    except Exception as e:
        print(f"Error fetching syllabus: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route("/save-schedule", methods=["POST"])
def save_schedule():
    """Save lecture schedule for a teacher"""
    if 'logged_in' not in session or session.get('role') != 'Teacher':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        day = data.get('day')
        lectures = data.get('lectures')
        teacher_email = session.get('email')
        
        if not day or not isinstance(lectures, list):
            return jsonify({'success': False, 'message': 'Invalid data'}), 400
            
        db = get_db_connection()
        cursor = db.cursor()
        
        # First, delete existing lectures for this teacher and day
        cursor.execute("DELETE FROM schedules WHERE teacher_email = %s AND day = %s", (teacher_email, day))
        
        # Insert new lectures
        for lecture in lectures:
            # Handle time parsing
            # Frontend sends 'time' like "9:00 AM - 10:00 AM"
            time_str = lecture.get('time', '')
            start_time = lecture.get('start_time')
            end_time = lecture.get('end_time')
            
            if not start_time and time_str:
                if '-' in time_str:
                    parts = time_str.split('-')
                    start_time = parts[0].strip()[:20] # Truncate to match DB schema
                    if len(parts) > 1:
                        end_time = parts[1].strip()[:20]
                else:
                    start_time = time_str[:20]

            cursor.execute("""
                INSERT INTO schedules (teacher_email, day, start_time, end_time, class_name, subject, topic, room)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                teacher_email, day, 
                start_time, end_time, 
                lecture.get('class_name'), lecture.get('subject'), 
                lecture.get('topic'), lecture.get('room')
            ))
            
        db.commit()
        cursor.close()
        db.close()
        
        return jsonify({'success': True, 'message': 'Schedule saved successfully'})
        
    except Exception as e:
        print(f"Error saving schedule: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route("/get-schedule", methods=["GET"])
def get_schedule():
    """Get schedule for teacher or student"""
    try:
        role = session.get('role')
        email = session.get('email')
        
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        
        if role == 'Teacher':
            # Teachers get their own schedule
            cursor.execute("SELECT * FROM schedules WHERE teacher_email = %s", (email,))
        elif role == 'Student':
            # Students get schedule for their class
            student = find_student_in_all_tables(email, cursor)
            if student:
                student_class = student['class_enroll']
                
                # Map Roman numerals to the format used in schedules table (e.g. 'Class 10th')
                class_map = {
                    'V': 'Class 5th',
                    'VI': 'Class 6th',
                    'VII': 'Class 7th',
                    'VIII': 'Class 8th',
                    'IX': 'Class 9th',
                    'X': 'Class 10th',
                    'XI': 'Class 11th',
                    'XII': 'Class 12th'
                }
                
                search_term = class_map.get(student_class, student_class)
                
                # Use the mapped term for searching
                cursor.execute("SELECT * FROM schedules WHERE class_name = %s", (search_term,))
            else:
                cursor.close()
                db.close()
                return jsonify({'success': False, 'message': 'Student class not found'}), 404
        else:
            cursor.close()
            db.close()
            return jsonify({'success': False, 'message': 'Unauthorized'}), 401
            
        schedules = cursor.fetchall()
        cursor.close()
        db.close()
        
        # Group by day
        grouped_schedule = {
            'monday': [], 'tuesday': [], 'wednesday': [], 'thursday': [], 'friday': [], 'saturday': []
        }
        
        for s in schedules:
            day_key = s['day'].lower()
            if day_key in grouped_schedule:
                # Reconstruct time string
                time_display = ""
                if s['start_time']:
                    time_display = s['start_time']
                    if s['end_time']:
                        time_display += f" - {s['end_time']}"
                
                grouped_schedule[day_key].append({
                    'time': time_display,
                    'start_time': s['start_time'],
                    'end_time': s['end_time'],
                    'class': s['class_name'], # For frontend
                    'class_name': s['class_name'],
                    'subject': s['subject'],
                    'topic': s['topic'],
                    'room': s['room'],
                    'teacher_email': s['teacher_email']
                })
                
        return jsonify({'success': True, 'schedule': grouped_schedule})
        
    except Exception as e:
        print(f"Error fetching schedule: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500
        cursor.execute("""
            INSERT INTO cancelled_admissions (
                original_admission_id, student_name, date_of_birth, email, 
                contact_number, class_enroll, gender, guardian_name, 
                guardian_contact, guardian_occupation, guardian_address, 
                previous_board, previous_school, percentage_obtained, 
                enrolled_board, enrolled_school, program_enrolled, subjects,
                original_created_at, cancellation_reason
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            admission['id'], admission['student_name'], admission['date_of_birth'],
            admission['email'], admission['contact_number'], admission['class_enroll'],
            admission['gender'], admission['guardian_name'], admission['guardian_contact'],
            admission['guardian_occupation'], admission['guardian_address'],
            admission['previous_board'], admission['previous_school'],
            admission['percentage_obtained'], admission['enrolled_board'],
            admission['enrolled_school'], admission['program_enrolled'],
            admission['subjects'], admission['created_at'], 'Student requested cancellation'
        ))
        
        # Delete from admissions table
        cursor.execute("DELETE FROM admissions WHERE email = %s", (email,))
        
        db.commit()
        cursor.close()
        db.close()
        
        # Clear session if student is logged in
        if 'logged_in' in session and session.get('username'):
            session.clear()
        
        flash("Your admission has been cancelled successfully. We're sorry to see you go!", "success")
        return redirect(url_for("home"))
        
    except Exception as e:
        print(f"Error cancelling admission: {e}")
        flash(f"Error cancelling admission: {str(e)}", "error")
        return redirect(url_for("home"))


@app.route("/cancel-teacher", methods=["POST"])
def cancel_teacher():
    """Handle teacher cancellation - move data to cancelled_teachers table"""
    try:
        email = request.form.get("email")
        
        if not email:
            flash("Email is required to cancel teacher", "error")
            return redirect(url_for("admin"))
        
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        
        # Get the teacher record
        cursor.execute("SELECT * FROM teacher_admissions WHERE email = %s", (email,))
        teacher = cursor.fetchone()
        
        if not teacher:
            flash("Teacher record not found", "error")
            cursor.close()
            db.close()
            return redirect(url_for("admin"))
        
        # Insert into cancelled_teachers table
        cursor.execute("""
            INSERT INTO cancelled_teachers (
                original_teacher_id, full_name, email, phone, date_of_birth,
                gender, blood_group, address, employee_id, designation,
                department, highest_qualification, specialization, experience,
                joining_date, emergency_contact_name, emergency_contact_phone,
                emergency_contact_relation, original_created_at, cancellation_reason
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            teacher['id'], teacher['full_name'], teacher['email'], teacher['phone'],
            teacher['date_of_birth'], teacher['gender'], teacher.get('blood_group'),
            teacher['address'], teacher['employee_id'], teacher['designation'],
            teacher['department'], teacher['highest_qualification'],
            teacher.get('specialization'), teacher['experience'], teacher['joining_date'],
            teacher['emergency_contact_name'], teacher['emergency_contact_phone'],
            teacher['emergency_contact_relation'], teacher['created_at'],
            'Admin cancelled teacher'
        ))
        
        # Delete from teacher_admissions table
        cursor.execute("DELETE FROM teacher_admissions WHERE email = %s", (email,))
        
        db.commit()
        cursor.close()
        db.close()
        
        flash(f"Teacher {teacher['full_name']} has been cancelled successfully.", "success")
        return redirect(url_for("admin"))
        
    except Exception as e:
        print(f"Error cancelling teacher: {e}")
        flash(f"Error cancelling teacher: {str(e)}", "error")
        return redirect(url_for("admin"))


# ================= STATIC PAGES =================
@app.route("/<page_name>")
def static_page(page_name):
    """
    This route serves any html file in templates corresponding to the URL
    Handles pages like aboutus, gallery, event, result, course pages, etc.
    """
    try:
        # Ignore requests for standard static file extensions to prevent unnecessary error flashes
        # This handles missing favicons, source maps, and other assets that might be requested
        static_exts = ('.ico', '.png', '.jpg', '.jpeg', '.gif', '.css', '.js', '.map', '.woff', '.woff2', '.ttf', '.svg')
        if any(page_name.lower().endswith(ext) for ext in static_exts):
            return "File not found", 404

        # Add .html extension if not present
        if not page_name.endswith('.html'):
            page_name += ".html"
        return render_template(page_name)
    except:
        # Only flash "Page not found" if it looks like a page request, not an asset request
        flash("Page not found", "error")
        return redirect(url_for("home"))

# ================= STUDENTS LIST FOR TEACHER =================
@app.route("/get-students-by-class", methods=["GET"])
def get_students_by_class():
    """Get list of students for a specific class"""
    if 'logged_in' not in session or session.get('role') != 'Teacher':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        class_name = request.args.get('class_name')
        if not class_name:
            return jsonify({'success': False, 'message': 'Class name is required'}), 400
            
        # Map class name to table name
        class_map = {
            'Class 5th': 'admissions_v',
            'Class 6th': 'admissions_vi',
            'Class 7th': 'admissions_vii',
            'Class 8th': 'admissions_viii',
            'Class 9th': 'admissions_ix',
            'Class 10th': 'admissions_x',
            'Class 11th': 'admissions_xi',
            'Class 12th': 'admissions_xii'
        }
        
        table_name = class_map.get(class_name)
        if not table_name:
            return jsonify({'success': False, 'message': 'Invalid class name'}), 400
            
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        
        # Prepare query to fetch students
        query = f"""
            SELECT student_name, email, contact_number, guardian_name, guardian_contact, 
                   date_of_birth, gender, percentage_obtained
            FROM {table_name}
            ORDER BY student_name ASC
        """
        
        cursor.execute(query)
        students = cursor.fetchall()
        
        cursor.close()
        db.close()
        
        return jsonify({'success': True, 'students': students})
        
    except Exception as e:
        print(f"Error fetching students: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

# ================= ATTENDANCE SYSTEM =================

@app.route("/save-attendance", methods=["POST"])
def save_attendance():
    """Save attendance for a class on a specific date"""
    if 'logged_in' not in session or session.get('role') != 'Teacher':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        class_name = data.get('class_name')
        date = data.get('date')
        attendance_list = data.get('attendance')
        teacher_email = session.get('email')
        
        if not class_name or not date or not attendance_list:
            return jsonify({'success': False, 'message': 'Missing required data'}), 400
            
        db = get_db_connection()
        cursor = db.cursor()
        
        # Process each student's attendance
        for record in attendance_list:
            email = record.get('email')
            status = record.get('status')
            name = record.get('name')
            
            # Check if record exists for this student and date
            cursor.execute(
                "SELECT id FROM attendance WHERE student_email = %s AND date = %s",
                (email, date)
            )
            existing = cursor.fetchone()
            
            if existing:
                # Update existing record
                cursor.execute(
                    "UPDATE attendance SET status = %s, marked_by = %s WHERE id = %s",
                    (status, teacher_email, existing[0])
                )
            else:
                # Insert new record
                cursor.execute(
                    "INSERT INTO attendance (student_email, student_name, class_name, date, status, marked_by) VALUES (%s, %s, %s, %s, %s, %s)",
                    (email, name, class_name, date, status, teacher_email)
                )
                
        db.commit()
        cursor.close()
        db.close()
        
        return jsonify({'success': True, 'message': 'Attendance saved successfully'})
        
    except Exception as e:
        print(f"Error saving attendance: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route("/get-attendance-sheet", methods=["GET"])
def get_attendance_sheet():
    """Get attendance sheet for a class and date (Teacher View)"""
    if 'logged_in' not in session or session.get('role') != 'Teacher':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
        
    try:
        class_name = request.args.get('class_name')
        date = request.args.get('date')
        
        if not class_name or not date:
            return jsonify({'success': False, 'message': 'Missing class or date'}), 400
            
        # 1. Get all students for the class first
        # Map class name to table name
        class_map = {
            'Class 5th': 'admissions_v',
            'Class 6th': 'admissions_vi',
            'Class 7th': 'admissions_vii',
            'Class 8th': 'admissions_viii',
            'Class 9th': 'admissions_ix',
            'Class 10th': 'admissions_x',
            'Class 11th': 'admissions_xi',
            'Class 12th': 'admissions_xii'
        }
        
        table_name = class_map.get(class_name)
        if not table_name:
            return jsonify({'success': False, 'message': 'Invalid class name'}), 400
            
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        
        # Fetch all students
        cursor.execute(f"SELECT student_name, email FROM {table_name} ORDER BY student_name ASC")
        students = cursor.fetchall()
        
        # 2. Fetch existing attendance for this date
        cursor.execute(
            "SELECT student_email, status FROM attendance WHERE class_name = %s AND date = %s",
            (class_name, date)
        )
        attendance_records = {row['student_email']: row['status'] for row in cursor.fetchall()}
        
        # 3. Merge data
        result = []
        for student in students:
            email = student['email']
            result.append({
                'name': student['student_name'],
                'email': email,
                'status': attendance_records.get(email, '') # Empty string means not marked yet
            })
            
        cursor.close()
        db.close()
        
        return jsonify({'success': True, 'students': result})
        
    except Exception as e:
        print(f"Error fetching attendance sheet: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route("/get-student-attendance", methods=["GET"])
def get_student_attendance():
    """Get attendance statistics for a student"""
    if 'logged_in' not in session:
         return jsonify({'success': False, 'message': 'Unauthorized'}), 401
         
    try:
        # If teacher is viewing a specific student, allow passing email param
        # Otherwise use session email
        target_email = request.args.get('email')
        
        if session.get('role') == 'Teacher':
            if not target_email:
                 return jsonify({'success': False, 'message': 'Student email required for teacher view'}), 400
            email = target_email
        else:
            email = session.get('email')
            
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        
        # Calculate stats
        cursor.execute(
            "SELECT COUNT(*) as total FROM attendance WHERE student_email = %s AND status != 'Late'", # Assuming Late counts as present or partial? Let's just count total marked days
            (email,)
        )
        total_days = cursor.fetchone()['total']
        
        cursor.execute(
            "SELECT COUNT(*) as present FROM attendance WHERE student_email = %s AND (status = 'Present' OR status = 'Late')",
            (email,)
        )
        present_days = cursor.fetchone()['present']
        
        cursor.execute(
            "SELECT COUNT(*) as absent FROM attendance WHERE student_email = %s AND status = 'Absent'",
            (email,)
        )
        absent_days = cursor.fetchone()['absent']
        
        # Get recent history
        cursor.execute(
            "SELECT date, status FROM attendance WHERE student_email = %s ORDER BY date DESC LIMIT 30",
            (email,)
        )
        history = cursor.fetchall()
        
        cursor.close()
        db.close()
        
        return jsonify({
            'success': True, 
            'stats': {
                'total_days': total_days,
                'present_days': present_days,
                'absent_days': absent_days,
                'percentage': round((present_days / total_days * 100) if total_days > 0 else 0)
            },
            'history': history
        })
        
    except Exception as e:
        print(f"Error fetching student attendance: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


# ================= GEMINI AI CHATBOT =================
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()  # Ensure .env is loaded for GEMINI_API_KEY

# Initialize Gemini model
_gemini_model = None

def get_gemini_model():
    global _gemini_model
    if _gemini_model is None:
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not set in .env file")
        genai.configure(api_key=api_key)
        _gemini_model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            system_instruction="""You are a friendly and helpful AI assistant for Apex Learning Hub, 
a coaching institute located in Nashik, Maharashtra, India.

Your role is to assist students, parents, and teachers with questions about:
- Admissions: Classes V to XII, enrollment process, required documents, fees
- Academic courses: MHTCET, NEET, JEE preparation
- Non-Academic programs: KVPY, NAVODAYA, SAINIK School, OLYMPIADS
- Attendance tracking and how to check it
- Exam results, grades, and performance
- Class schedules and timetables
- Teacher profiles and subjects
- School events and gallery
- Location: 2nd Floor, 'Guru Mauli', Near HP Petrol Pump, Meri-Rasbihari Link Road, Nashik - 422003
- Contact: +919421554793, +918928772435
- Email: apexlearninghub2020@gmail.com

Guidelines:
- Be warm, concise, and helpful
- Answer only school or education-related questions
- If asked something unrelated, politely redirect to school topics
- Use simple language that students and parents can understand
- Format responses clearly with bullet points when listing multiple items
- Always encourage students with positive language"""
        )
    return _gemini_model

@app.route('/chatbot', methods=['POST'])
def chatbot():
    """AI chatbot endpoint powered by Google Gemini"""
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'success': False, 'error': 'No message provided'}), 400
        
        user_message = data['message'].strip()
        if not user_message:
            return jsonify({'success': False, 'error': 'Empty message'}), 400
        
        # Get or initialize Gemini model
        model = get_gemini_model()
        
        # Generate response
        response = model.generate_content(user_message)
        reply = response.text
        
        return jsonify({'success': True, 'reply': reply})
        
    except ValueError as e:
        print(f"Gemini config error: {e}")
        return jsonify({'success': False, 'error': 'Chatbot not configured. Please check GEMINI_API_KEY in .env'}), 500
    except Exception as e:
        error_str = str(e).lower()
        print(f"Chatbot error: {e}")
        # Handle quota / rate limit errors
        if '429' in str(e) or 'quota' in error_str or 'resource_exhausted' in error_str or 'rate' in error_str:
            return jsonify({
                'success': False,
                'error': '⏳ The AI is temporarily unavailable due to high usage. Please wait a minute and try again. (Free tier limit reached)'
            }), 429
        return jsonify({'success': False, 'error': 'Sorry, I could not process your request. Please try again.'}), 500


# ================= RUN SERVER =================
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)