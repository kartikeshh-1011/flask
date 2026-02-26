# Quick Start Guide - Upload to GitHub & Deploy Online

## 📋 What You Need to Do

### Step 1: Install Git (5 minutes)
1. Download Git: https://git-scm.com/download/win
2. Run installer (use default settings)
3. Restart your computer

### Step 2: Create GitHub Account (3 minutes)
1. Go to: https://github.com/signup
2. Sign up (it's free!)
3. Verify your email

### Step 3: Upload Your Code to GitHub (10 minutes)

**Option A - Using GitHub Desktop (Easiest):**
1. Download: https://desktop.github.com/
2. Install and sign in
3. Click "Add" → "Add Existing Repository"
4. Select folder: `C:\Users\LOQ\OneDrive\Desktop\flask`
5. Click "Publish repository"
6. Uncheck "Keep this code private"
7. Click "Publish"
8. ✅ Done! Your code is on GitHub

**Option B - Using Git Bash:**
1. Right-click in your flask folder → "Git Bash Here"
2. Run these commands:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

### Step 4: Deploy Online (30 minutes)

**Recommended: PythonAnywhere (Free & Easy)**

1. **Sign up**: https://www.pythonanywhere.com
   - Choose "Beginner" account (free)

2. **Setup Database**:
   - Go to "Databases" tab
   - Set MySQL password
   - Create database: `yourusername$flask_auth`

3. **Upload Code**:
   - Go to "Consoles" → Start "Bash"
   - Run:
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   cd YOUR_REPO_NAME
   python3.10 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Setup Tables**:
   - Go to "Databases" → "Start a console"
   - Copy-paste SQL from these files (in order):
     - `schema.sql`
     - `admissions_table.sql`
     - `results_table.sql`
     - `add_role_column.sql`

5. **Create Web App**:
   - Go to "Web" tab → "Add a new web app"
   - Choose "Manual configuration" → Python 3.10

6. **Configure WSGI** (click WSGI file link):
   ```python
   import sys
   import os
   
   project_home = '/home/yourusername/YOUR_REPO_NAME'
   if project_home not in sys.path:
       sys.path = [project_home] + sys.path
   
   os.environ['DB_HOST'] = 'yourusername.mysql.pythonanywhere-services.com'
   os.environ['DB_USER'] = 'yourusername'
   os.environ['DB_PASSWORD'] = 'your_mysql_password'
   os.environ['DB_NAME'] = 'yourusername$flask_auth'
   os.environ['SECRET_KEY'] = 'apex_learning_hub_secret_key_2026'
   
   from app import app as application
   ```

7. **Set Virtualenv**:
   - Path: `/home/yourusername/YOUR_REPO_NAME/venv`

8. **Set Static Files**:
   - URL: `/static/`
   - Directory: `/home/yourusername/YOUR_REPO_NAME/static`

9. **Reload & Test**:
   - Click green "Reload" button
   - Visit: `https://yourusername.pythonanywhere.com`

### 🎉 Your App is Live!

**Your URL**: `https://yourusername.pythonanywhere.com`
- Share this with anyone
- Works on any device (phone, tablet, computer)
- Accessible from anywhere in the world

---

## 📊 How User Data is Stored

### When Someone Uses Your App:

1. **They visit**: `https://yourusername.pythonanywhere.com`
2. **They interact**: Signup, submit forms, etc.
3. **Data is saved**: To YOUR MySQL database on PythonAnywhere
4. **You can view it**:
   - PythonAnywhere → "Databases" → "Start a console"
   - Run SQL: `SELECT * FROM users;` (or admissions, feedback, etc.)
   - Or visit: `https://yourusername.pythonanywhere.com/view-admissions`

### Important Notes:

✅ **GitHub Repository** = Your CODE only (no data)
- Anyone can see the code
- No one can access your data

✅ **Deployed App** = Your CODE + DATABASE
- Users interact with your app
- Data stored in YOUR database
- Only YOU can access the database

✅ **Your Database Tables**:
- `users` - Signup/login data
- `admissions` - Student admission forms
- `results` - Exam results (teacher updates)
- `feedback` - User feedback
- `complaints` - User complaints
- `contacts` - Contact form messages

---

## 🔐 Security Note

**IMPORTANT**: Your `app.py` currently has a hardcoded password on line 10.

Before uploading to GitHub, you should either:
1. Remove the password and use environment variables (recommended)
2. Or make sure `.gitignore` excludes `app.py` (not recommended)

I can help you update `app.py` to use environment variables if you'd like!

---

## 📚 Full Documentation

For detailed instructions, see:
- **README.md** - Complete project documentation
- **DEPLOYMENT_GUIDE.md** - Step-by-step deployment for all platforms
- **implementation_plan.md** - Technical implementation details

---

## ❓ Need Help?

Common issues:
- **Git not recognized**: Restart computer after installing Git
- **Permission denied**: Use Personal Access Token instead of password
- **Database connection failed**: Check environment variables
- **Static files not loading**: Verify static file path in PythonAnywhere

For more help, check the full DEPLOYMENT_GUIDE.md!
