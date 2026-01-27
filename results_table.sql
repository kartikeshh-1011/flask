-- SQL Schema for Results Table
-- Run this in MySQL Workbench to create the results table

USE flask_auth;

CREATE TABLE IF NOT EXISTS results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    
    -- Student Information (from admissions or manual entry)
    student_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    class VARCHAR(50) NOT NULL,
    
    -- Subject Marks
    hindi_grammar DECIMAL(5,2) DEFAULT NULL,
    english_grammar DECIMAL(5,2) DEFAULT NULL,
    marathi_grammar DECIMAL(5,2) DEFAULT NULL,
    maths DECIMAL(5,2) DEFAULT NULL,
    science DECIMAL(5,2) DEFAULT NULL,
    physics DECIMAL(5,2) DEFAULT NULL,
    chemistry DECIMAL(5,2) DEFAULT NULL,
    biology DECIMAL(5,2) DEFAULT NULL,
    sst DECIMAL(5,2) DEFAULT NULL,
    vedic_maths DECIMAL(5,2) DEFAULT NULL,
    art_craft DECIMAL(5,2) DEFAULT NULL,
    
    -- Calculated Fields
    total_marks DECIMAL(6,2) DEFAULT NULL,
    percentage DECIMAL(5,2) DEFAULT NULL,
    grade VARCHAR(10) DEFAULT NULL,
    
    -- Metadata
    updated_by VARCHAR(255) DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Indexes
    INDEX idx_student_name (student_name),
    INDEX idx_email (email),
    INDEX idx_class (class),
    UNIQUE KEY unique_student (student_name, email, class)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
