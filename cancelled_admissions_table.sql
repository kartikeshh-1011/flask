-- SQL Schema for Cancelled Admissions Table
-- This table stores all cancelled student admissions
-- Run this in MySQL Workbench or command line

USE flask_auth;

CREATE TABLE IF NOT EXISTS cancelled_admissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    
    -- Original admission ID (for reference)
    original_admission_id INT,
    
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
    original_created_at TIMESTAMP NULL,
    cancelled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cancellation_reason TEXT,
    
    INDEX idx_email (email),
    INDEX idx_student_name (student_name),
    INDEX idx_cancelled_at (cancelled_at),
    INDEX idx_original_admission_id (original_admission_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
