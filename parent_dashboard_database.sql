-- ============================================
-- PARENT DASHBOARD DATABASE SCHEMA
-- SQL code to create tables and insert sample data
-- ============================================

-- 1. STUDENTS TABLE (if not exists)
CREATE TABLE IF NOT EXISTS students (
    student_id INT PRIMARY KEY AUTO_INCREMENT,
    student_name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(20),
    date_of_birth DATE,
    blood_group VARCHAR(5),
    class VARCHAR(10),
    section VARCHAR(5),
    roll_number INT,
    admission_date DATE,
    address TEXT,
    overall_grade VARCHAR(5),
    class_rank INT,
    attendance_percentage DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. PARENTS TABLE
CREATE TABLE IF NOT EXISTS parents (
    parent_id INT PRIMARY KEY AUTO_INCREMENT,
    parent_name VARCHAR(100) NOT NULL,
    student_id INT,
    relationship VARCHAR(20), -- Father, Mother, Guardian
    email VARCHAR(100),
    phone VARCHAR(20),
    status VARCHAR(20) DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);

-- 3. SUBJECTS TABLE
CREATE TABLE IF NOT EXISTS subjects (
    subject_id INT PRIMARY KEY AUTO_INCREMENT,
    subject_name VARCHAR(50) NOT NULL,
    subject_code VARCHAR(10),
    subject_type VARCHAR(20) -- Math, Science, English, etc.
);

-- 4. TEACHERS TABLE
CREATE TABLE IF NOT EXISTS teachers (
    teacher_id INT PRIMARY KEY AUTO_INCREMENT,
    teacher_name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(20),
    subject_id INT,
    qualification VARCHAR(100),
    experience_years INT,
    office_hours VARCHAR(50),
    room_number VARCHAR(100),
    rating DECIMAL(2,1),
    is_class_teacher BOOLEAN DEFAULT FALSE,
    class_assigned VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
);

-- 5. PROGRESS REPORTS TABLE
CREATE TABLE IF NOT EXISTS progress_reports (
    report_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    subject_id INT,
    teacher_id INT,
    unit_test_1 INT,
    unit_test_2 INT,
    unit_test_3 INT,
    average_marks DECIMAL(5,2),
    grade VARCHAR(5),
    academic_year VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id),
    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id)
);

-- 6. FEE STRUCTURE TABLE
CREATE TABLE IF NOT EXISTS fee_structure (
    fee_id INT PRIMARY KEY AUTO_INCREMENT,
    fee_type VARCHAR(50) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    academic_year VARCHAR(10)
);

-- 7. FEE PAYMENTS TABLE
CREATE TABLE IF NOT EXISTS fee_payments (
    payment_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    receipt_number VARCHAR(20) UNIQUE,
    payment_date DATE,
    description VARCHAR(100),
    amount DECIMAL(10,2),
    payment_mode VARCHAR(20), -- Online, Cheque, Cash
    status VARCHAR(20) DEFAULT 'Paid',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);

-- 8. CLASS SCHEDULE TABLE
CREATE TABLE IF NOT EXISTS class_schedule (
    schedule_id INT PRIMARY KEY AUTO_INCREMENT,
    class VARCHAR(10),
    section VARCHAR(5),
    day_of_week VARCHAR(10),
    start_time TIME,
    end_time TIME,
    subject_id INT,
    teacher_id INT,
    is_break BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id),
    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id)
);

-- 9. TEACHER ADMISSIONS TABLE
CREATE TABLE IF NOT EXISTS teacher_admissions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(20),
    subject VARCHAR(100),
    qualification VARCHAR(255),
    photo_path VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 10. STUDENT ADMISSION TABLES (GRADES)
CREATE TABLE IF NOT EXISTS admissions_primary (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    date_of_birth DATE,
    contact_number VARCHAR(20),
    class_enroll VARCHAR(50),
    gender VARCHAR(20),
    guardian_name VARCHAR(100),
    photo_path VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- (Explicitly defining all grade tables)
CREATE TABLE IF NOT EXISTS admissions_v (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    date_of_birth DATE,
    contact_number VARCHAR(20),
    class_enroll VARCHAR(50),
    gender VARCHAR(20),
    guardian_name VARCHAR(100),
    photo_path VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS admissions_vi (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    date_of_birth DATE,
    contact_number VARCHAR(20),
    class_enroll VARCHAR(50),
    gender VARCHAR(20),
    guardian_name VARCHAR(100),
    photo_path VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS admissions_vii (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    date_of_birth DATE,
    contact_number VARCHAR(20),
    class_enroll VARCHAR(50),
    gender VARCHAR(20),
    guardian_name VARCHAR(100),
    photo_path VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS admissions_viii (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    date_of_birth DATE,
    contact_number VARCHAR(20),
    class_enroll VARCHAR(50),
    gender VARCHAR(20),
    guardian_name VARCHAR(100),
    photo_path VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS admissions_ix (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    date_of_birth DATE,
    contact_number VARCHAR(20),
    class_enroll VARCHAR(50),
    gender VARCHAR(20),
    guardian_name VARCHAR(100),
    photo_path VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS admissions_x (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    date_of_birth DATE,
    contact_number VARCHAR(20),
    class_enroll VARCHAR(50),
    gender VARCHAR(20),
    guardian_name VARCHAR(100),
    photo_path VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS admissions_xi (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    date_of_birth DATE,
    contact_number VARCHAR(20),
    class_enroll VARCHAR(50),
    gender VARCHAR(20),
    guardian_name VARCHAR(100),
    photo_path VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS admissions_xii (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    date_of_birth DATE,
    contact_number VARCHAR(20),
    class_enroll VARCHAR(50),
    gender VARCHAR(20),
    guardian_name VARCHAR(100),
    photo_path VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- 11. CONTACTS & FEEDBACK & COMPLAINTS
CREATE TABLE IF NOT EXISTS contacts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    email VARCHAR(100),
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS feedback (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    email VARCHAR(100),
    feedback TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS complaints (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    email VARCHAR(100),
    contact VARCHAR(20),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ============================================
-- INSERT SAMPLE DATA
-- ============================================

-- Insert Subjects
INSERT INTO subjects (subject_name, subject_code, subject_type) VALUES
('Mathematics', 'MATH101', 'math'),
('Science', 'SCI101', 'science'),
('English', 'ENG101', 'english'),
('Hindi', 'HIN101', 'hindi'),
('Social Studies', 'SS101', 'social'),
('Computer Science', 'CS101', 'computer'),
('Physical Education', 'PE101', 'sports'),
('Art & Craft', 'ART101', 'art');

-- Insert Teachers
INSERT INTO teachers (teacher_name, email, phone, subject_id, qualification, experience_years, office_hours, room_number, rating, is_class_teacher, class_assigned) VALUES
('Mrs. Priya Sharma', 'priya.sharma@school.edu', '+91 98765 43210', 1, 'M.Sc. Mathematics', 15, 'Mon-Fri, 2:30 PM - 4:00 PM', 'Staff Room - 2nd Floor', 4.8, TRUE, '10th A'),
('Mr. Rajesh Sharma', 'rajesh.sharma@school.edu', '+91 98765 11111', 1, 'M.Sc. Mathematics', 12, 'Mon-Fri, 3:00 PM - 4:30 PM', 'Room 201', 4.7, FALSE, NULL),
('Dr. Amit Patel', 'amit.patel@school.edu', '+91 98765 22222', 2, 'Ph.D. Physics', 18, 'Mon-Fri, 2:00 PM - 3:30 PM', 'Lab 1', 4.9, FALSE, NULL),
('Mrs. Anjali Gupta', 'anjali.gupta@school.edu', '+91 98765 33333', 3, 'M.A. English Literature', 10, 'Mon-Fri, 2:30 PM - 4:00 PM', 'Room 105', 4.6, FALSE, NULL),
('Mrs. Sunita Verma', 'sunita.verma@school.edu', '+91 98765 44444', 4, 'M.A. Hindi', 8, 'Mon-Fri, 3:00 PM - 4:00 PM', 'Room 106', 4.5, FALSE, NULL),
('Mr. Vikram Kumar', 'vikram.kumar@school.edu', '+91 98765 55555', 5, 'M.A. History & Geography', 14, 'Mon-Fri, 2:30 PM - 4:00 PM', 'Room 107', 4.7, FALSE, NULL),
('Mr. Arjun Singh', 'arjun.singh@school.edu', '+91 98765 66666', 6, 'B.Tech Computer Science', 6, 'Mon-Fri, 3:00 PM - 5:00 PM', 'Computer Lab', 4.8, FALSE, NULL),
('Coach Reddy', 'coach.reddy@school.edu', '+91 98765 77777', 7, 'B.P.Ed', 20, 'Mon-Fri, 4:00 PM - 5:00 PM', 'Sports Ground', 4.9, FALSE, NULL),
('Ms. Mehta', 'ms.mehta@school.edu', '+91 98765 88888', 8, 'B.F.A', 5, 'Mon-Fri, 2:00 PM - 3:00 PM', 'Art Room', 4.6, FALSE, NULL);

-- Insert Students
INSERT INTO students (student_name, email, phone, date_of_birth, blood_group, class, section, roll_number, admission_date, address, overall_grade, class_rank, attendance_percentage) VALUES
('Aman Singh', 'aman.singh@school.edu', '+91 98765 43210', '2010-03-15', 'O+', '10th', 'A', 1, '2020-04-01', '123, Park Street, New Delhi - 110001', 'A+', 2, 92.00);

-- Insert Parents
INSERT INTO parents (parent_name, student_id, relationship, email, phone, status) VALUES
('Mr. Rajesh Singh', 1, 'Father', 'rajesh.singh@email.com', '+91 98765 43210', 'Active');

-- Insert Progress Reports
INSERT INTO progress_reports (student_id, subject_id, teacher_id, unit_test_1, unit_test_2, unit_test_3, average_marks, grade, academic_year) VALUES
(1, 1, 2, 92, 88, 95, 91.67, 'A+', '2025-26'),
(1, 2, 3, 85, 90, 88, 87.67, 'A', '2025-26'),
(1, 3, 4, 90, 92, 94, 92.00, 'A+', '2025-26');

-- Insert Fee Structure
INSERT INTO fee_structure (fee_type, amount, academic_year) VALUES
('Tuition Fee', 50000.00, '2025-26'),
('Library Fee', 5000.00, '2025-26'),
('Sports Fee', 5000.00, '2025-26'),
('Lab Fee', 8000.00, '2025-26'),
('Computer Fee', 5000.00, '2025-26'),
('Miscellaneous', 2000.00, '2025-26');

-- Insert Fee Payments
INSERT INTO fee_payments (student_id, receipt_number, payment_date, description, amount, payment_mode, status) VALUES
(1, 'RCP001', '2025-04-01', 'Term 1 Fees', 25000.00, 'Online', 'Paid'),
(1, 'RCP002', '2025-08-01', 'Term 2 Fees', 25000.00, 'Cheque', 'Paid'),
(1, 'RCP003', '2025-12-01', 'Term 3 Fees', 25000.00, 'Online', 'Paid');

-- Insert Class Schedule for 10th A
INSERT INTO class_schedule (class, section, day_of_week, start_time, end_time, subject_id, teacher_id, is_break) VALUES
-- Monday
('10th', 'A', 'Monday', '09:00:00', '10:00:00', 1, 2, FALSE),
('10th', 'A', 'Monday', '10:00:00', '11:00:00', 3, 4, FALSE),
('10th', 'A', 'Monday', '11:00:00', '11:30:00', NULL, NULL, TRUE),
('10th', 'A', 'Monday', '11:30:00', '12:30:00', 2, 3, FALSE),
('10th', 'A', 'Monday', '13:30:00', '14:30:00', 5, 6, FALSE),
-- Tuesday
('10th', 'A', 'Tuesday', '09:00:00', '10:00:00', 4, 5, FALSE),
('10th', 'A', 'Tuesday', '10:00:00', '11:00:00', 1, 2, FALSE),
('10th', 'A', 'Tuesday', '11:00:00', '11:30:00', NULL, NULL, TRUE),
('10th', 'A', 'Tuesday', '11:30:00', '12:30:00', 6, 7, FALSE),
('10th', 'A', 'Tuesday', '13:30:00', '14:30:00', 7, 8, FALSE),
-- Wednesday
('10th', 'A', 'Wednesday', '09:00:00', '10:00:00', 2, 3, FALSE),
('10th', 'A', 'Wednesday', '10:00:00', '11:00:00', 3, 4, FALSE),
('10th', 'A', 'Wednesday', '11:00:00', '11:30:00', NULL, NULL, TRUE),
('10th', 'A', 'Wednesday', '11:30:00', '12:30:00', 1, 2, FALSE),
('10th', 'A', 'Wednesday', '13:30:00', '14:30:00', 8, 9, FALSE);

-- ============================================
-- USEFUL QUERIES FOR PARENT DASHBOARD
-- ============================================

-- Query 1: Get Parent and Student Details
SELECT 
    p.parent_id,
    p.parent_name,
    p.relationship,
    p.status,
    s.student_id,
    s.student_name,
    s.email AS student_email,
    s.phone AS student_phone,
    s.date_of_birth,
    s.blood_group,
    CONCAT(s.class, ' ', s.section) AS class_section,
    s.roll_number,
    s.admission_date,
    s.address,
    s.overall_grade,
    s.class_rank,
    s.attendance_percentage
FROM parents p
JOIN students s ON p.student_id = s.student_id
WHERE p.parent_id = 1; -- Replace with actual parent_id from session

-- Query 2: Get Progress Reports with Subject and Teacher Details
SELECT 
    pr.report_id,
    sub.subject_name,
    sub.subject_type,
    t.teacher_name,
    pr.unit_test_1,
    pr.unit_test_2,
    pr.unit_test_3,
    pr.average_marks,
    pr.grade
FROM progress_reports pr
JOIN subjects sub ON pr.subject_id = sub.subject_id
JOIN teachers t ON pr.teacher_id = t.teacher_id
WHERE pr.student_id = 1 -- Replace with actual student_id
ORDER BY sub.subject_name;

-- Query 3: Get Fee Summary
SELECT 
    SUM(fs.amount) AS total_annual_fee,
    COALESCE(SUM(fp.amount), 0) AS amount_paid,
    SUM(fs.amount) - COALESCE(SUM(fp.amount), 0) AS balance_due
FROM fee_structure fs
LEFT JOIN fee_payments fp ON fp.student_id = 1 -- Replace with actual student_id
WHERE fs.academic_year = '2025-26';

-- Query 4: Get Payment History
SELECT 
    receipt_number,
    DATE_FORMAT(payment_date, '%d %b %Y') AS payment_date,
    description,
    CONCAT('₹', FORMAT(amount, 0)) AS amount,
    payment_mode,
    status
FROM fee_payments
WHERE student_id = 1 -- Replace with actual student_id
ORDER BY payment_date DESC;

-- Query 5: Get Fee Breakdown
SELECT 
    fee_type,
    CONCAT('₹', FORMAT(amount, 0)) AS amount
FROM fee_structure
WHERE academic_year = '2025-26'
ORDER BY fee_type;

-- Query 6: Get Class Schedule
SELECT 
    cs.day_of_week,
    TIME_FORMAT(cs.start_time, '%h:%i %p') AS start_time,
    TIME_FORMAT(cs.end_time, '%h:%i %p') AS end_time,
    CASE 
        WHEN cs.is_break = TRUE THEN 'Break'
        ELSE sub.subject_name
    END AS subject,
    t.teacher_name AS teacher
FROM class_schedule cs
LEFT JOIN subjects sub ON cs.subject_id = sub.subject_id
LEFT JOIN teachers t ON cs.teacher_id = t.teacher_id
WHERE cs.class = '10th' AND cs.section = 'A'
ORDER BY 
    FIELD(cs.day_of_week, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'),
    cs.start_time;

-- Query 7: Get Class Teacher Details
SELECT 
    t.teacher_id,
    t.teacher_name,
    sub.subject_name,
    t.email,
    t.phone,
    t.qualification,
    t.experience_years,
    t.office_hours,
    t.room_number,
    t.rating
FROM teachers t
JOIN subjects sub ON t.subject_id = sub.subject_id
WHERE t.is_class_teacher = TRUE AND t.class_assigned = '10th A';

-- Query 8: Get All Subject Teachers
SELECT 
    t.teacher_id,
    t.teacher_name,
    sub.subject_name,
    sub.subject_type,
    t.email,
    t.phone,
    t.qualification
FROM teachers t
JOIN subjects sub ON t.subject_id = sub.subject_id
JOIN progress_reports pr ON t.teacher_id = pr.teacher_id
WHERE pr.student_id = 1 -- Replace with actual student_id
GROUP BY t.teacher_id;
