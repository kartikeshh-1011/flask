-- Create teacher_admissions table
CREATE TABLE IF NOT EXISTS teacher_admissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender VARCHAR(20) NOT NULL,
    blood_group VARCHAR(10),
    address TEXT NOT NULL,
    
    employee_id VARCHAR(50) NOT NULL UNIQUE,
    designation VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL,
    joining_date DATE NOT NULL,
    experience INT NOT NULL,
    specialization VARCHAR(255),
    
    highest_qualification VARCHAR(100) NOT NULL,
    university VARCHAR(255) NOT NULL,
    graduation_year INT NOT NULL,
    certifications TEXT,
    
    emergency_contact_name VARCHAR(255) NOT NULL,
    emergency_contact_phone VARCHAR(20) NOT NULL,
    emergency_contact_relation VARCHAR(100) NOT NULL,
    
    -- Document Paths
    photo_path VARCHAR(255),
    resume_path VARCHAR(255),
    aadhaar_path VARCHAR(255),
    pan_path VARCHAR(255),
    other_docs_path TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_email (email),
    INDEX idx_employee_id (employee_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
