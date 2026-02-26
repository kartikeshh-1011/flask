-- Create tables for each class
-- Schema based on original admissions table

-- Class V
CREATE TABLE IF NOT EXISTS admissions_v (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_name VARCHAR(255) NOT NULL,
    date_of_birth DATE NOT NULL,
    email VARCHAR(255) NOT NULL,
    contact_number VARCHAR(20) NOT NULL,
    class_enroll VARCHAR(50) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    guardian_name VARCHAR(255) NOT NULL,
    guardian_contact VARCHAR(20) NOT NULL,
    guardian_occupation VARCHAR(100),
    guardian_address TEXT,
    previous_board VARCHAR(50) NOT NULL,
    previous_school VARCHAR(255),
    percentage_obtained VARCHAR(10),
    enrolled_board VARCHAR(50) NOT NULL,
    enrolled_school VARCHAR(255),
    program_enrolled VARCHAR(100) NOT NULL,
    subjects TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_student_name (student_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Class VI
CREATE TABLE IF NOT EXISTS admissions_vi LIKE admissions_v;

-- Class VII
CREATE TABLE IF NOT EXISTS admissions_vii LIKE admissions_v;

-- Class VIII
CREATE TABLE IF NOT EXISTS admissions_viii LIKE admissions_v;

-- Class IX
CREATE TABLE IF NOT EXISTS admissions_ix LIKE admissions_v;

-- Class X
CREATE TABLE IF NOT EXISTS admissions_x LIKE admissions_v;

-- Class XI
CREATE TABLE IF NOT EXISTS admissions_xi LIKE admissions_v;

-- Class XII
CREATE TABLE IF NOT EXISTS admissions_xii LIKE admissions_v;
