-- Primary Section Table: stores Class 1, Class 2, Class 3, Class 4
-- class_enroll column holds the specific class value for each student

CREATE TABLE IF NOT EXISTS `admissions_primary` (
  `id` int NOT NULL AUTO_INCREMENT,
  `student_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `date_of_birth` date NOT NULL,
  `email` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `contact_number` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `class_enroll` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `gender` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `guardian_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `guardian_contact` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `guardian_occupation` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `guardian_address` text COLLATE utf8mb4_unicode_ci,
  `previous_board` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `previous_school` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `percentage_obtained` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `enrolled_board` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `enrolled_school` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `program_enrolled` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `subjects` text COLLATE utf8mb4_unicode_ci,
  `photo_path` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `aadhaar_path` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `marksheet_path` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_email` (`email`),
  KEY `idx_student_name` (`student_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
