CREATE TABLE IF NOT EXISTS syllabus (
    id INT AUTO_INCREMENT PRIMARY KEY,
    teacher_email VARCHAR(255) NOT NULL,
    class_name VARCHAR(50) NOT NULL,
    subject VARCHAR(100) NOT NULL,
    chapter_number INT NOT NULL,
    chapter_name VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL, -- 'pending', 'progress', 'complete'
    topics_covered INT DEFAULT 0,
    total_topics INT DEFAULT 1,
    duration INT DEFAULT 0, -- in weeks
    target_date DATE,
    date_label VARCHAR(50), -- 'Start Date', 'Expected Completion', 'Last Updated'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX (class_name),
    INDEX (teacher_email),
    INDEX (subject)
);
