# 📊 ADMISSION FORM DATABASE - QUICK REFERENCE

## Database Information
- **Database Name**: `flask_auth`
- **Table Name**: `admissions`
- **Location**: MySQL Server (localhost)

---

## 🔧 How to Run the Database in MySQL Workbench

### Method 1: Using the SQL File (Recommended)

1. **Open MySQL Workbench**
2. **Connect to your local server** (localhost)
3. **Open the SQL file:**
   - File → Open SQL Script
   - Navigate to: `C:\Users\LOQ\OneDrive\Desktop\flask\admissions_table.sql`
4. **Execute the script:**
   - Click the lightning bolt icon (⚡) or press `Ctrl+Shift+Enter`
5. **Verify:**
   ```sql
   USE flask_auth;
   SHOW TABLES;
   SELECT * FROM admissions;
   ```

### Method 2: Copy-Paste SQL

Copy and paste this into MySQL Workbench and execute:

```sql
USE flask_auth;

CREATE TABLE IF NOT EXISTS admissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    
    -- Student Information
    student_name VARCHAR(255) NOT NULL,
    date_of_birth DATE NOT NULL,
    email VARCHAR(255) NOT NULL,
    contact_number VARCHAR(20) NOT NULL,
    class_enroll VARCHAR(50) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    
    -- Guardian Information
    guardian_name VARCHAR(255) NOT NULL,
    guardian_contact VARCHAR(20) NOT NULL,
    guardian_occupation VARCHAR(100),
    guardian_address TEXT,
    
    -- Previous Board Details
    previous_board VARCHAR(50) NOT NULL,
    previous_school VARCHAR(255),
    percentage_obtained VARCHAR(10),
    
    -- Enrolled Board
    enrolled_board VARCHAR(50) NOT NULL,
    enrolled_school VARCHAR(255),
    
    -- Program & Subjects
    program_enrolled VARCHAR(100) NOT NULL,
    subjects TEXT,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_email (email),
    INDEX idx_student_name (student_name),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

---

## 📋 Viewing Admission Data

### Option 1: Using the Web Interface (Easiest)

1. Start your Flask server: `python app.py`
2. Open browser and go to: `http://127.0.0.1:5000/view-admissions`
3. You'll see all submissions in a beautiful table with statistics!

### Option 2: Using MySQL Workbench

Execute these queries:

```sql
-- View all admissions
SELECT * FROM admissions ORDER BY created_at DESC;

-- Count total admissions
SELECT COUNT(*) as total_admissions FROM admissions;

-- Count by gender
SELECT gender, COUNT(*) as count 
FROM admissions 
GROUP BY gender;

-- View recent admissions (last 10)
SELECT student_name, email, class_enroll, created_at 
FROM admissions 
ORDER BY created_at DESC 
LIMIT 10;

-- Search by student name
SELECT * FROM admissions 
WHERE student_name LIKE '%search_term%';

-- View admissions by program
SELECT program_enrolled, COUNT(*) as count 
FROM admissions 
GROUP BY program_enrolled;
```

---

## 🔍 Useful SQL Queries

### View specific student details
```sql
SELECT * FROM admissions WHERE email = 'student@example.com';
```

### Export to CSV (in MySQL Workbench)
```sql
SELECT * FROM admissions 
INTO OUTFILE 'C:/admissions_export.csv'
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n';
```

### Delete all test data (BE CAREFUL!)
```sql
DELETE FROM admissions WHERE student_name LIKE '%test%';
```

### View table structure
```sql
DESCRIBE admissions;
```

---

## 📊 Table Structure

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| `id` | INT | Auto-increment primary key |
| `student_name` | VARCHAR(255) | Student's full name |
| `date_of_birth` | DATE | Birth date (YYYY-MM-DD) |
| `email` | VARCHAR(255) | Student's email |
| `contact_number` | VARCHAR(20) | Student's phone |
| `class_enroll` | VARCHAR(50) | Class enrolling for |
| `gender` | VARCHAR(10) | Male/Female |
| `guardian_name` | VARCHAR(255) | Guardian's name |
| `guardian_contact` | VARCHAR(20) | Guardian's phone |
| `guardian_occupation` | VARCHAR(100) | Guardian's job |
| `guardian_address` | TEXT | Full address |
| `previous_board` | VARCHAR(50) | CBSE/ICSE/etc. |
| `previous_school` | VARCHAR(255) | Previous school name |
| `percentage_obtained` | VARCHAR(10) | Previous marks |
| `enrolled_board` | VARCHAR(50) | Board enrolling in |
| `enrolled_school` | VARCHAR(255) | School name |
| `program_enrolled` | VARCHAR(100) | Program type |
| `subjects` | TEXT | Comma-separated subjects |
| `created_at` | TIMESTAMP | Submission timestamp |

---

## ✅ Database Status

**Current Status**: ✅ **ACTIVE AND READY**

The database table has been successfully created and is connected to your Flask application. All admission form submissions will be automatically stored in this table.

---

## 🚀 Quick Start

1. **Database is already set up!** (Created by `setup_admissions_db.py`)
2. **Flask server is running** on `http://127.0.0.1:5000`
3. **Test the form**: Go to `http://127.0.0.1:5000/addmision`
4. **View submissions**: Go to `http://127.0.0.1:5000/view-admissions`

---

## 🔗 Important Links

- **Admission Form**: http://127.0.0.1:5000/addmision
- **View All Records**: http://127.0.0.1:5000/view-admissions
- **Home Page**: http://127.0.0.1:5000/

---

## 📝 Notes

- All data is stored permanently in MySQL
- Timestamps are automatically added
- The table uses UTF-8 encoding for international characters
- Indexes are created for faster searches on email, name, and date
