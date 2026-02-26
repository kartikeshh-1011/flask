from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import mysql.connector
import bcrypt

# ================= DATABASE CONNECTION =================
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="vishal7084",
            database="flask_auth",
            autocommit=False
        )
        print("✓ Database connected")
        return connection
    except mysql.connector.Error as err:
        print(f"✗ Database error: {err}")
        raise

# ================= APP CONFIG =================
app = Flask(__name__)
app.secret_key = "your_secret_key_here"

# Error handler to prevent silent crashes
@app.errorhandler(Exception)
def handle_exception(e):
    print(f"UNHANDLED EXCEPTION: {str(e)}")
    import traceback
    traceback.print_exc()
    flash(f"An error occurred: {str(e)}", "error")
    return redirect(url_for("home"))

# ================= HOME =================
@app.route("/")
def home():
    return render_template("home.html")

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
                        # Safely get role with default value 'Student' if not set
                        session['role'] = user.get('role', 'Student') or 'Student'
                        session['logged_in'] = True
                        
                        print(f"SESSION CREATED: role={session['role']}")  # Debug
                        
                        flash(f"Welcome back, {user['username']}!", "success")
                        
                        # Redirect teachers to result update page
                        if session['role'] == 'Teacher':
                            print("REDIRECTING TO: update_result")  # Debug
                            return redirect(url_for("update_result"))
                        else:
                            print("REDIRECTING TO: home")  # Debug
                            return redirect(url_for("home"))
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
        
        flash("Thank you for your feedback!", "success")
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
@app.route("/addmision")
def addmision():
    return render_template("addmision.html")

@app.route("/submit-admission", methods=["POST"])
def submit_admission():
    try:
        # Extract form data
        student_name = request.form.get("student_name")
        date_of_birth = request.form.get("date_of_birth")
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
        
        # Insert into database
        db = get_db_connection()
        cursor = db.cursor()
        
        cursor.execute("""
            INSERT INTO admissions (
                student_name, date_of_birth, email, contact_number, 
                class_enroll, gender, guardian_name, guardian_contact, 
                guardian_occupation, guardian_address, previous_board, 
                previous_school, percentage_obtained, enrolled_board, 
                enrolled_school, program_enrolled, subjects
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            student_name, date_of_birth, email, contact_number,
            class_enroll, gender, guardian_name, guardian_contact,
            guardian_occupation, guardian_address, previous_board,
            previous_school, percentage_obtained, enrolled_board,
            enrolled_school, program_enrolled, subjects
        ))
        
        db.commit()
        cursor.close()
        db.close()
        
        flash(f"Admission application submitted successfully for {student_name}! We will contact you soon.", "success")
        return redirect(url_for("addmision"))
        
    except Exception as e:
        flash(f"Error submitting admission form: {str(e)}", "error")
        return redirect(url_for("addmision"))

@app.route("/view-admissions")
def view_admissions():
    """Admin page to view all admission records"""
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        
        # Get all admissions
        cursor.execute("SELECT * FROM admissions ORDER BY created_at DESC")
        admissions = cursor.fetchall()
        
        # Get statistics
        cursor.execute("SELECT COUNT(*) as total FROM admissions")
        total_admissions = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as count FROM admissions WHERE gender='Male'")
        male_count = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM admissions WHERE gender='Female'")
        female_count = cursor.fetchone()['count']
        
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
        
        # Get all students from admissions
        cursor.execute("SELECT student_name, email, class_enroll, subjects FROM admissions ORDER BY class_enroll, student_name")
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

# ================= STATIC PAGES =================
@app.route("/<page_name>")
def static_page(page_name):
    """
    This route serves any html file in templates corresponding to the URL
    Handles pages like aboutus, gallery, event, result, course pages, etc.
    """
    try:
        # Add .html extension if not present
        if not page_name.endswith('.html'):
            page_name += ".html"
        return render_template(page_name)
    except:
        flash("Page not found", "error")
        return redirect(url_for("home"))

# ================= RUN SERVER =================
if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)