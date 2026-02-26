# Deployment Guide - Flask Learning Management System

This guide provides step-by-step instructions for deploying your Flask application online so it's accessible from any device via a URL.

## Table of Contents
1. [Installing Git](#installing-git)
2. [Uploading to GitHub](#uploading-to-github)
3. [Deployment Options](#deployment-options)
4. [PythonAnywhere Deployment (Recommended)](#pythonanywhere-deployment)
5. [Railway Deployment](#railway-deployment)
6. [Render Deployment](#render-deployment)
7. [Accessing User Data](#accessing-user-data)

---

## Installing Git

### Windows
1. Download Git from: https://git-scm.com/download/win
2. Run the installer
3. Use default settings (click "Next" through the wizard)
4. Verify installation:
   - Open Command Prompt or PowerShell
   - Type: `git --version`
   - You should see the Git version number

---

## Uploading to GitHub

### Step 1: Create GitHub Account
1. Go to https://github.com/signup
2. Create your account (it's free)
3. Verify your email address

### Step 2: Create New Repository
1. Click the "+" icon in top-right corner
2. Select "New repository"
3. Fill in details:
   - **Repository name**: `flask-learning-hub` (or any name you prefer)
   - **Description**: "Flask Learning Management System with student admissions and result management"
   - **Visibility**: Choose "Public" (required for free hosting)
   - **DO NOT** check "Add a README file" (we already have one)
4. Click "Create repository"

### Step 3: Upload Your Code

#### Option A: Using Git Bash (Recommended)
1. Open Git Bash in your project folder:
   - Navigate to `C:\Users\LOQ\OneDrive\Desktop\flask`
   - Right-click in the folder → "Git Bash Here"

2. Run these commands one by one:
```bash
# Initialize Git repository
git init

# Add all files (respecting .gitignore)
git add .

# Create first commit
git commit -m "Initial commit: Flask Learning Management System"

# Add your GitHub repository as remote
# Replace YOUR_USERNAME and YOUR_REPO_NAME with your actual values
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to GitHub
git branch -M main
git push -u origin main
```

3. Enter your GitHub username and password when prompted
   - **Note**: You may need to use a Personal Access Token instead of password
   - Generate token at: https://github.com/settings/tokens

#### Option B: Using GitHub Desktop (Easier for Beginners)
1. Download GitHub Desktop: https://desktop.github.com/
2. Install and sign in with your GitHub account
3. Click "Add" → "Add Existing Repository"
4. Choose your project folder: `C:\Users\LOQ\OneDrive\Desktop\flask`
5. Click "Publish repository"
6. Uncheck "Keep this code private" (for free hosting)
7. Click "Publish Repository"

### Step 4: Verify Upload
1. Go to your GitHub repository URL: `https://github.com/YOUR_USERNAME/YOUR_REPO_NAME`
2. You should see all your files
3. **Important**: Check that `app.py` does NOT show your database password
   - If it does, we need to update the code first (see Security Note below)

---

## Security Note: Removing Hardcoded Credentials

**IMPORTANT**: Before uploading to GitHub, you should remove the hardcoded database password from `app.py`.

### Quick Fix:
1. Open `app.py`
2. Find line 10: `password=\"vishal7084\",`
3. Replace the entire `get_db_connection()` function with:

```python
from config import Config

def get_db_connection():
    try:
        config = Config()
        return mysql.connector.connect(
            host=config.DB_HOST,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            database=config.DB_NAME,
            use_pure=True,
            connect_timeout=10
        )
    except mysql.connector.Error as err:
        print(f"DATABASE ERROR: {err}")
        raise Exception(f"Cannot connect to database: {err}")
```

4. Create `.env` file with your actual credentials:
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=vishal7084
DB_NAME=flask_auth
SECRET_KEY=apex_learning_hub_secret_key_2026
```

5. Now commit and push again:
```bash
git add .
git commit -m "Security: Use environment variables for credentials"
git push
```

---

## Deployment Options

### Comparison Table

| Platform | Free Tier | Ease of Use | Database Included | Best For |
|----------|-----------|-------------|-------------------|----------|
| **PythonAnywhere** | ✅ Yes | ⭐⭐⭐⭐⭐ Easy | ✅ MySQL included | Beginners |
| **Railway** | ✅ $5 credit | ⭐⭐⭐⭐ Moderate | ✅ Yes (add-on) | Modern apps |
| **Render** | ✅ Yes | ⭐⭐⭐⭐ Moderate | ✅ PostgreSQL free | Production apps |
| **Heroku** | ❌ No free tier | ⭐⭐⭐ Moderate | ❌ Paid only | Legacy apps |

---

## PythonAnywhere Deployment

### Step 1: Create Account
1. Go to https://www.pythonanywhere.com
2. Click "Start running Python online in less than a minute!"
3. Create a **Beginner** account (free)
4. Verify your email

### Step 2: Create MySQL Database
1. Go to "Databases" tab
2. Set a MySQL password (remember this!)
3. Click "Initialize MySQL"
4. Create a new database:
   - Database name: `yourusername$flask_auth`
   - Click "Create"

### Step 3: Upload Your Code
1. Go to "Consoles" tab
2. Start a new "Bash" console
3. Clone your GitHub repository:
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

### Step 4: Install Dependencies
```bash
# Create virtual environment
python3.10 -m venv venv
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### Step 5: Setup Database
1. Go to "Databases" tab
2. Click "Start a console" on your database
3. Copy and paste contents of your SQL files:
   - `schema.sql`
   - `admissions_table.sql`
   - `results_table.sql`
   - `add_role_column.sql`

Or use the MySQL console:
```bash
mysql -u yourusername -p -h yourusername.mysql.pythonanywhere-services.com yourusername$flask_auth < schema.sql
```

### Step 6: Configure Web App
1. Go to "Web" tab
2. Click "Add a new web app"
3. Choose "Manual configuration"
4. Select Python 3.10
5. Click "Next"

### Step 7: Configure WSGI File
1. In "Web" tab, click on WSGI configuration file
2. Replace contents with:
```python
import sys
import os

# Add your project directory to the sys.path
project_home = '/home/yourusername/YOUR_REPO_NAME'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Set environment variables
os.environ['DB_HOST'] = 'yourusername.mysql.pythonanywhere-services.com'
os.environ['DB_USER'] = 'yourusername'
os.environ['DB_PASSWORD'] = 'your_mysql_password'
os.environ['DB_NAME'] = 'yourusername$flask_auth'
os.environ['SECRET_KEY'] = 'your_secret_key_here'

# Import flask app
from app import app as application
```

### Step 8: Set Virtual Environment
1. In "Web" tab, find "Virtualenv" section
2. Enter path: `/home/yourusername/YOUR_REPO_NAME/venv`

### Step 9: Set Static Files
1. In "Web" tab, find "Static files" section
2. Add mapping:
   - URL: `/static/`
   - Directory: `/home/yourusername/YOUR_REPO_NAME/static`

### Step 10: Reload and Test
1. Click the big green "Reload" button
2. Visit your site: `https://yourusername.pythonanywhere.com`
3. Test signup, login, and other features

### Your App is Now Live! 🎉
- **URL**: `https://yourusername.pythonanywhere.com`
- Share this URL with anyone
- Accessible from any device with internet

---

## Railway Deployment

### Step 1: Create Account
1. Go to https://railway.app
2. Sign up with GitHub
3. Verify email

### Step 2: Create New Project
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your repository
4. Railway will auto-detect Flask

### Step 3: Add MySQL Database
1. Click "New" → "Database" → "Add MySQL"
2. Railway will create a MySQL instance
3. Note the connection details

### Step 4: Set Environment Variables
1. Go to your web service
2. Click "Variables" tab
3. Add these variables:
   - `DB_HOST`: (from MySQL service)
   - `DB_USER`: (from MySQL service)
   - `DB_PASSWORD`: (from MySQL service)
   - `DB_NAME`: `flask_auth`
   - `SECRET_KEY`: (generate a random string)

### Step 5: Setup Database
1. Connect to MySQL using provided credentials
2. Run your SQL schema files
3. Create tables

### Step 6: Deploy
1. Railway automatically deploys on push
2. Get your URL from "Settings" → "Domains"
3. Click "Generate Domain"

---

## Render Deployment

### Step 1: Create Account
1. Go to https://render.com
2. Sign up with GitHub

### Step 2: Create Web Service
1. Click "New" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name**: flask-learning-hub
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

### Step 3: Add PostgreSQL Database
1. Click "New" → "PostgreSQL"
2. Create database (free tier available)
3. Note connection details

**Note**: You'll need to convert MySQL to PostgreSQL or use external MySQL service.

### Step 4: Set Environment Variables
1. In your web service, go to "Environment"
2. Add variables (same as Railway)

### Step 5: Deploy
1. Render automatically deploys
2. Get your URL from dashboard
3. Format: `https://your-app-name.onrender.com`

---

## Accessing User Data

### How Data is Stored

When someone interacts with your deployed application:

1. **Signup/Login**
   - Data stored in `users` table
   - Password is hashed (secure)
   - Includes: username, email, hashed password, role

2. **Admission Form**
   - Data stored in `admissions` table
   - Includes: student details, guardian info, academic history

3. **Results**
   - Data stored in `results` table
   - Updated by teachers
   - Includes: marks, grades, percentages

4. **Feedback/Complaints/Contact**
   - Stored in respective tables
   - Includes: name, email, message, timestamp

### How to View Your Data

#### Method 1: Hosting Platform Database Console
**PythonAnywhere:**
1. Go to "Databases" tab
2. Click "Start a console on yourusername$flask_auth"
3. Run SQL queries:
```sql
-- View all users
SELECT * FROM users;

-- View all admissions
SELECT * FROM admissions ORDER BY created_at DESC;

-- View all results
SELECT * FROM results;

-- View feedback
SELECT * FROM feedback ORDER BY created_at DESC;
```

**Railway/Render:**
1. Go to your database service
2. Use provided connection details
3. Connect with MySQL Workbench or similar tool

#### Method 2: Admin Dashboard (Already in Your App!)
Your app already has admin routes:

- **View Admissions**: `https://your-url.com/view-admissions`
  - Shows all admission applications
  - Displays statistics

You can create similar admin pages for other data:
```python
@app.route("/admin/users")
def view_users():
    # Add authentication check
    # Query users table
    # Display in template
```

#### Method 3: Database Management Tools
- **MySQL Workbench**: https://www.mysql.com/products/workbench/
- **phpMyAdmin**: Often included with hosting platforms
- **DBeaver**: https://dbeaver.io/ (free, supports all databases)

### Important Notes

> [!IMPORTANT]
> **GitHub vs Deployed App**
> - **GitHub repository**: Contains only CODE (no data)
> - **Deployed app**: Connects to online DATABASE (contains data)
> - Users accessing GitHub see code only
> - Users accessing deployed URL interact with your live app and database

> [!WARNING]
> **Data Privacy**
> - Only you (and authorized admins) can access the database
> - Regular users can only see their own data
> - Implement proper authentication for admin routes
> - Never expose database credentials in code

---

## Troubleshooting

### Common Issues

**1. "Module not found" error**
- Solution: Make sure all dependencies are in `requirements.txt`
- Run: `pip freeze > requirements.txt`

**2. Database connection failed**
- Check environment variables are set correctly
- Verify database host, username, password
- Ensure database exists and tables are created

**3. Static files not loading**
- Configure static file path in hosting platform
- Check `/static/` URL mapping

**4. Application error on startup**
- Check application logs in hosting platform
- Verify WSGI configuration
- Ensure `app.py` has no syntax errors

### Getting Help
- PythonAnywhere: https://help.pythonanywhere.com/
- Railway: https://docs.railway.app/
- Render: https://render.com/docs

---

## Next Steps

After deployment:
1. ✅ Test all features (signup, login, forms)
2. ✅ Submit test data and verify it's stored
3. ✅ Share URL with friends/colleagues for testing
4. ✅ Create admin dashboard for data management
5. ✅ Set up regular database backups
6. ✅ Monitor application performance

**Congratulations! Your app is now live and accessible worldwide! 🚀**
