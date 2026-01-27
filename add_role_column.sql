-- Add role column to existing users table
-- Run this in MySQL Workbench

USE flask_auth;

-- Check if role column exists, if not add it
ALTER TABLE users ADD COLUMN role ENUM('Admin', 'Teacher', 'Student') NOT NULL DEFAULT 'Student' AFTER password;

-- Verify the change
DESCRIBE users;
