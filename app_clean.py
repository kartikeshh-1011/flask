from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import mysql.connector
import bcrypt

# ================= DATABASE CONNECTION =================
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="vishal7084",
        database="flask_auth"
    )

# ================= APP CONFIG =================
app = Flask(__name__)
app.secret_key = "apex_learning_hub_secret_key_2026"

# ================= HOME =================
@app.route("/")
def home():
    return render_template("home.html")

# ================= SIGNUP =================
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        try:
            username = request.form.get("username", "").strip()
            email = request.form.get("email", "").strip()
            password = request.form.get("password", "").strip()
            role = request.form.get("role", "Student").strip()
            
            if not username or not email or not password:
                flash("All fields are required", "error")
                return redirect(url_for("signup"))
            
            db = get_db_connection()
            cursor = db.cursor()
            
            # Check if username or email already exists
            cursor.execute(
                "SELECT * FROM users WHERE username=%s OR email=%s",
                (username, email)
            )
            
            if cursor.fetchone():
                cursor.close()
                db.close()
                flash("Username or Email already exists", "error")
                return redirect(url_for("signup"))
            
            # Hash the password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=4))
            
            # Insert user
            cursor.execute(
                "INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)",
                (username, email, hashed_password, role)
            )
            
            db.commit()
            cursor.close()
            db.close()
            
            flash("Registration successful! Please login.", "success")
            return redirect(url_for("login"))
            
        except Exception as e:
            flash(f"Signup error. Please try again.", "error")
            return redirect(url_for("signup"))
    
    return render_template("signup.html")

# ================= LOGIN =================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "").strip()
            
            if not username or not password:
                flash("Username and password are required", "error")
                return redirect(url_for("login"))
            
            db = get_db_connection()
            cursor = db.cursor(dictionary=True)
            
            cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
            user = cursor.fetchone()
            
            cursor.close()
            db.close()
            
            if user:
                # Handle password - might be bytes or string
                stored_password = user['password']
                if isinstance(stored_password, str):
                    stored_password = stored_password.encode('utf-8')
                
                if bcrypt.checkpw(password.encode('utf-8'), stored_password):
                    # Create session
                    session['user_id'] = user['id']
                    session['username'] = user['username']
                    session['role'] = user.get('role') or 'Student'
                    session['logged_in'] = True
                    
                    flash(f"Welcome back, {user['username']}!", "success")
                    
                    # Redirect based on role
                    if session['role'] == 'Teacher':
                        return redirect(url_for("update_result"))
                    else:
                        return redirect(url_for("home"))
                else:
                    flash("Invalid username or password", "error")
                    return redirect(url_for("login"))
            else:
                flash("Invalid username or password", "error")
                return redirect(url_for("login"))
                
        except Exception as e:
            flash("Login error. Please try again.", "error")
            return redirect(url_for("login"))
    
    return render_template("login.html")

# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out successfully", "success")
    return redirect(url_for("home"))

# ================= FORGOT PASSWORD =================
@app.route("/forgot", methods=["GET", "POST"])
def forgot():
    if request.method == "POST":
        email = request.form.get("email")
        flash("Password reset link has been sent to your email", "success")
        return redirect(url_for("login"))
    return render_template("forgot.html")
