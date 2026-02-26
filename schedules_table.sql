CREATE TABLE IF NOT EXISTS schedules (
    id INT AUTO_INCREMENT PRIMARY KEY,
    teacher_email VARCHAR(255) NOT NULL,
    day VARCHAR(20) NOT NULL,
    start_time VARCHAR(20),
    end_time VARCHAR(20),
    class_name VARCHAR(50) NOT NULL,
    subject VARCHAR(100),
    topic VARCHAR(255),
    room VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX (class_name),
    INDEX (teacher_email)
);
