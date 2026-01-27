-- SQL Schema for Admissions Table
-- Run this in MySQL Workbench to create the admissions table

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
