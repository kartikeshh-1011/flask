# Apex Learning Hub - Flask Learning Management System

![Flask](https://img.shields.io/badge/Flask-3.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange)

A comprehensive Learning Management System built with Flask, featuring student admissions, result management, authentication, and more.

## 🌟 Features

### User Management
- **Student & Teacher Signup/Login** with role-based access
- Secure password hashing using bcrypt
- Password reset functionality
- Session management

### Student Features
- Online admission form submission
- View exam results
- Submit feedback and complaints
- Contact administration

### Teacher Features
- Update student results
- Manage multiple subjects and grades
- Automatic grade calculation
- View student admissions

### Admin Features
- View all admissions
- Access contact form submissions
- Review feedback and complaints
- Manage user data

## 📋 Prerequisites

- Python 3.8 or higher
- MySQL 8.0 or higher
- pip (Python package manager)

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup

#### Create MySQL Database
```sql
CREATE DATABASE flask_auth;
USE flask_auth;
```

#### Run Schema Files
Execute the following SQL files in order:
1. `schema.sql` - Creates users, contacts, feedback, complaints tables
2. `admissions_table.sql` - Creates admissions table
3. `results_table.sql` - Creates results table
4. `add_role_column.sql` - Adds role column to users table

Or use the Python setup scripts:
```bash
python setup_admissions_db.py
python setup_results_db.py
```

### 5. Configure Environment Variables

Create a `.env` file in the project root:
```bash
cp .env.example .env
```

Edit `.env` with your credentials:
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=flask_auth
SECRET_KEY=your_secret_key_here
FLASK_ENV=development
```

### 6. Run the Application
```bash
python app.py
```

The application will be available at: `http://127.0.0.1:5000`

## 📊 Database Schema

### Tables
- **users** - User authentication (username, email, password, role)
- **admissions** - Student admission applications
- **results** - Student exam results with subject-wise marks
- **contacts** - Contact form submissions
- **feedback** - User feedback
- **complaints** - User complaints

## 🔐 Security Features

- Passwords hashed with bcrypt
- SQL injection protection using parameterized queries
- Session-based authentication
- Environment variable configuration for sensitive data
- CSRF protection via Flask sessions

## 🌐 Deployment

### Option 1: PythonAnywhere (Recommended for Beginners)
1. Sign up at [PythonAnywhere](https://www.pythonanywhere.com)
2. Clone your repository
3. Create MySQL database
4. Configure WSGI file
5. Set environment variables
6. Access at: `yourusername.pythonanywhere.com`

### Option 2: Railway
1. Sign up at [Railway](https://railway.app)
2. Connect GitHub repository
3. Add MySQL database service
4. Set environment variables
5. Deploy automatically

### Option 3: Render
1. Sign up at [Render](https://render.com)
2. Create new Web Service
3. Connect GitHub repository
4. Add MySQL database
5. Configure environment variables

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions.

## 📱 How User Data is Stored

### When Users Interact with Your Deployed App

1. **Signup/Login**: User credentials stored in `users` table with hashed passwords
2. **Admission Forms**: Student data stored in `admissions` table
3. **Results**: Teacher-updated marks stored in `results` table
4. **Feedback/Complaints**: Stored in respective tables with timestamps

### Accessing Your Data

**As Admin/Developer:**
- Login to your hosting platform's database console
- Use phpMyAdmin or MySQL Workbench
- Create admin dashboard routes in the app (e.g., `/view-admissions`)

**Important:** 
- GitHub repository contains only CODE, not data
- Deployed app connects to online MySQL database
- Only you (and authorized users) can access the database

## 🎨 Project Structure

```
flask/
├── app.py                      # Main application file
├── config.py                   # Configuration management
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
├── static/                    # CSS, JS, images
├── templates/                 # HTML templates
│   ├── home.html
│   ├── signup.html
│   ├── login.html
│   ├── addmision.html
│   ├── update_result.html
│   └── ...
└── SQL files/
    ├── schema.sql
    ├── admissions_table.sql
    └── results_table.sql
```

## 🛠️ Technologies Used

- **Backend**: Flask (Python)
- **Database**: MySQL
- **Authentication**: bcrypt
- **Frontend**: HTML, CSS, JavaScript
- **Session Management**: Flask sessions

## 📝 Usage

### For Students
1. Sign up with Student role
2. Submit admission form
3. Check results using name, email, and class
4. Submit feedback or complaints

### For Teachers
1. Sign up with Teacher role
2. Login redirects to result update page
3. Select student and enter marks
4. System automatically calculates total, percentage, and grade

### For Admins
1. Access `/view-admissions` to see all applications
2. View statistics (total admissions, gender distribution)
3. Access database for detailed reports

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

Created by [Your Name]

## 📧 Contact

For questions or support, please use the contact form in the application or reach out via GitHub issues.

---

**Note**: Remember to never commit your `.env` file or expose your database credentials. Always use environment variables for sensitive information.
