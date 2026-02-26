# Database and Template Fixes

## Issues Fixed

### 1. ✅ Template Syntax Error (Jinja2)
**Error**: `jinja2.exceptions.TemplateSyntaxError: expected token ',', got '-'`

**Cause**: Footer links in feedback.html, contact.html, and complain.html were using old `.html` format instead of Flask `url_for()`

**Fixed Files**:
- `templates/feedback.html` - Updated footer links
- `templates/contact.html` - Updated footer links  
- `templates/complain.html` - Updated footer links

### 2. ⚠️ Database Error (Requires Manual Fix)
**Error**: `mysql.connector.errors.ProgrammingError: 1054 (42S22): Unknown column 'role' in 'field list'`

**Cause**: The `users` table in your MySQL database doesn't have the `role` column

**Solution**: Run the SQL script below in MySQL Workbench

## How to Fix the Database

### Step 1: Open MySQL Workbench
1. Launch MySQL Workbench
2. Connect to your local MySQL server

### Step 2: Execute the Fix Script

Open and execute [add_role_column.sql](file:///c:/Users/LOQ/OneDrive/Desktop/flask/add_role_column.sql) OR copy-paste this into MySQL Workbench:

```sql
USE flask_auth;

-- Add role column to users table
ALTER TABLE users 
ADD COLUMN role ENUM('Admin', 'Teacher', 'Student') 
NOT NULL DEFAULT 'Student' 
AFTER password;

-- Verify the change
DESCRIBE users;
```

### Step 3: Verify the Fix

After running the script, you should see output like this:

```
Field      | Type                                    | Null | Key | Default  | Extra
-----------+-----------------------------------------+------+-----+----------+----------------
id         | int                                     | NO   | PRI | NULL     | auto_increment
username   | varchar(50)                             | NO   | UNI | NULL     |
email      | varchar(100)                            | NO   | UNI | NULL     |
password   | varchar(255)                            | NO   |     | NULL     |
role       | enum('Admin','Teacher','Student')       | NO   |     | Student  |
created_at | timestamp                               | YES  |     | CURRENT_TIMESTAMP |
```

### Step 4: Restart Flask Application

After fixing the database:
1. Press `CTRL+C` in the terminal running Flask
2. Run: `python app.py`
3. Test signup again

## Testing After Fixes

### Test Signup (http://127.0.0.1:5000/signup)
1. Select a role (Admin/Teacher/Student)
2. Enter username, email, password
3. Click "Sign Up"
4. Should redirect to login page with success message

### Verify in MySQL
```sql
USE flask_auth;
SELECT * FROM users;
```

You should see your new user with:
- Hashed password (long encrypted string)
- Selected role (Admin/Teacher/Student)

### Test Login (http://127.0.0.1:5000/login)
1. Enter your username and password
2. Should redirect to home page
3. Login button should change to "Logout"

### Test Forms
All forms should now work without template errors:
- Contact: http://127.0.0.1:5000/contact
- Feedback: http://127.0.0.1:5000/feedback
- Complaint: http://127.0.0.1:5000/complain

## Summary

✅ **Fixed**: Template syntax errors in feedback, contact, and complaint pages
⚠️ **Action Required**: Add role column to database using the SQL script above

Once you run the SQL script, everything should work perfectly!
