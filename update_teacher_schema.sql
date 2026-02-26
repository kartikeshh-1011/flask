-- Add columns for document uploads to teacher_admissions table
ALTER TABLE teacher_admissions
ADD COLUMN resume_path VARCHAR(255),
ADD COLUMN aadhaar_path VARCHAR(255),
ADD COLUMN pan_path VARCHAR(255),
ADD COLUMN other_docs_path TEXT;
