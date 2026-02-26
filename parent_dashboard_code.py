"""
PARENT DASHBOARD - PYTHON CODE SNIPPETS
Use these code snippets in your Flask routes to fetch data from database
WITHOUT modifying your main app.py structure
"""

# ============================================
# IMPORT REQUIRED LIBRARIES (Add to your app.py imports)
# ============================================
from flask import Flask, render_template, session, redirect, url_for
import mysql.connector
from datetime import datetime

# ============================================
# DATABASE CONNECTION HELPER FUNCTION
# ============================================
def get_db_connection():
    """Create and return database connection"""
    connection = mysql.connector.connect(
        host='localhost',
        user='root',  # Replace with your MySQL username
        password='',  # Replace with your MySQL password
        database='school_db'  # Replace with your database name
    )
    return connection

# ============================================
# ROUTE: PARENT DASHBOARD
# Add this route to your app.py
# ============================================
@app.route('/parent')
def parent_dashboard():
    """Parent Dashboard Route"""
    
    # Get parent_id from session (you should set this during login)
    parent_id = session.get('parent_id', 1)  # Default to 1 for testing
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # ===== 1. GET PARENT AND STUDENT DETAILS =====
    cursor.execute("""
        SELECT 
            p.parent_id,
            p.parent_name,
            p.relationship,
            p.status,
            s.student_id,
            s.student_name,
            s.email AS student_email,
            s.phone AS student_phone,
            DATE_FORMAT(s.date_of_birth, '%%d %%M %%Y') AS date_of_birth,
            s.blood_group,
            CONCAT(s.class, ' ', s.section) AS class_section,
            s.class,
            s.section,
            s.roll_number,
            DATE_FORMAT(s.admission_date, '%%d %%M %%Y') AS admission_date,
            s.address,
            s.overall_grade,
            s.class_rank,
            s.attendance_percentage
        FROM parents p
        JOIN students s ON p.student_id = s.student_id
        WHERE p.parent_id = %s
    """, (parent_id,))
    
    parent_student_data = cursor.fetchone()
    
    if not parent_student_data:
        return "Parent not found", 404
    
    student_id = parent_student_data['student_id']
    
    # ===== 2. GET PROGRESS REPORTS =====
    cursor.execute("""
        SELECT 
            pr.report_id,
            sub.subject_name,
            sub.subject_type,
            t.teacher_name,
            pr.unit_test_1,
            pr.unit_test_2,
            pr.unit_test_3,
            pr.average_marks,
            pr.grade
        FROM progress_reports pr
        JOIN subjects sub ON pr.subject_id = sub.subject_id
        JOIN teachers t ON pr.teacher_id = t.teacher_id
        WHERE pr.student_id = %s
        ORDER BY sub.subject_name
    """, (student_id,))
    
    progress_reports = cursor.fetchall()
    
    # ===== 3. GET FEE SUMMARY =====
    cursor.execute("""
        SELECT 
            SUM(fs.amount) AS total_annual_fee,
            COALESCE((SELECT SUM(amount) FROM fee_payments WHERE student_id = %s), 0) AS amount_paid
        FROM fee_structure fs
        WHERE fs.academic_year = '2025-26'
    """, (student_id,))
    
    fee_summary = cursor.fetchone()
    fee_summary['balance_due'] = fee_summary['total_annual_fee'] - fee_summary['amount_paid']
    
    # ===== 4. GET PAYMENT HISTORY =====
    cursor.execute("""
        SELECT 
            receipt_number,
            DATE_FORMAT(payment_date, '%%d %%b %%Y') AS payment_date,
            description,
            amount,
            payment_mode,
            status
        FROM fee_payments
        WHERE student_id = %s
        ORDER BY payment_date DESC
    """, (student_id,))
    
    payment_history = cursor.fetchall()
    
    # ===== 5. GET FEE BREAKDOWN =====
    cursor.execute("""
        SELECT 
            fee_type,
            amount
        FROM fee_structure
        WHERE academic_year = '2025-26'
        ORDER BY fee_type
    """)
    
    fee_breakdown = cursor.fetchall()
    
    # ===== 6. GET CLASS SCHEDULE =====
    cursor.execute("""
        SELECT 
            cs.day_of_week,
            TIME_FORMAT(cs.start_time, '%%h:%%i %%p') AS start_time,
            TIME_FORMAT(cs.end_time, '%%h:%%i %%p') AS end_time,
            CASE 
                WHEN cs.is_break = TRUE THEN 'Break'
                ELSE sub.subject_name
            END AS subject,
            CASE 
                WHEN cs.is_break = TRUE THEN NULL
                ELSE t.teacher_name
            END AS teacher,
            cs.is_break
        FROM class_schedule cs
        LEFT JOIN subjects sub ON cs.subject_id = sub.subject_id
        LEFT JOIN teachers t ON cs.teacher_id = t.teacher_id
        WHERE cs.class = %s AND cs.section = %s
        ORDER BY 
            FIELD(cs.day_of_week, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'),
            cs.start_time
    """, (parent_student_data['class'], parent_student_data['section']))
    
    schedule_data = cursor.fetchall()
    
    # Group schedule by day
    schedule_by_day = {}
    for item in schedule_data:
        day = item['day_of_week']
        if day not in schedule_by_day:
            schedule_by_day[day] = []
        schedule_by_day[day].append(item)
    
    # ===== 7. GET CLASS TEACHER DETAILS =====
    cursor.execute("""
        SELECT 
            t.teacher_id,
            t.teacher_name,
            sub.subject_name,
            t.email,
            t.phone,
            t.qualification,
            t.experience_years,
            t.office_hours,
            t.room_number,
            t.rating
        FROM teachers t
        JOIN subjects sub ON t.subject_id = sub.subject_id
        WHERE t.is_class_teacher = TRUE AND t.class_assigned = %s
    """, (parent_student_data['class_section'],))
    
    class_teacher = cursor.fetchone()
    
    # ===== 8. GET SUBJECT TEACHERS =====
    cursor.execute("""
        SELECT DISTINCT
            t.teacher_id,
            t.teacher_name,
            sub.subject_name,
            sub.subject_type,
            t.email,
            t.phone,
            t.qualification
        FROM teachers t
        JOIN subjects sub ON t.subject_id = sub.subject_id
        JOIN progress_reports pr ON t.teacher_id = pr.teacher_id
        WHERE pr.student_id = %s
        ORDER BY sub.subject_name
    """, (student_id,))
    
    subject_teachers = cursor.fetchall()
    
    # Close connection
    cursor.close()
    conn.close()
    
    # ===== RENDER TEMPLATE WITH ALL DATA =====
    return render_template('parent.html',
        parent=parent_student_data,
        student=parent_student_data,
        progress_reports=progress_reports,
        fee_summary=fee_summary,
        payment_history=payment_history,
        fee_breakdown=fee_breakdown,
        schedule_by_day=schedule_by_day,
        class_teacher=class_teacher,
        subject_teachers=subject_teachers
    )


# ============================================
# ALTERNATIVE: USING PANDAS DATAFRAME
# If you prefer using pandas for data manipulation
# ============================================
import pandas as pd

@app.route('/parent_pandas')
def parent_dashboard_pandas():
    """Parent Dashboard using Pandas DataFrames"""
    
    parent_id = session.get('parent_id', 1)
    
    conn = get_db_connection()
    
    # Get parent and student data
    parent_student_df = pd.read_sql("""
        SELECT 
            p.parent_id, p.parent_name, p.relationship, p.status,
            s.student_id, s.student_name, s.email, s.phone,
            s.date_of_birth, s.blood_group, s.class, s.section,
            s.roll_number, s.admission_date, s.address,
            s.overall_grade, s.class_rank, s.attendance_percentage
        FROM parents p
        JOIN students s ON p.student_id = s.student_id
        WHERE p.parent_id = %s
    """ % parent_id, conn)
    
    if parent_student_df.empty:
        return "Parent not found", 404
    
    student_id = parent_student_df.iloc[0]['student_id']
    
    # Get progress reports
    progress_df = pd.read_sql("""
        SELECT 
            sub.subject_name, sub.subject_type, t.teacher_name,
            pr.unit_test_1, pr.unit_test_2, pr.unit_test_3,
            pr.average_marks, pr.grade
        FROM progress_reports pr
        JOIN subjects sub ON pr.subject_id = sub.subject_id
        JOIN teachers t ON pr.teacher_id = t.teacher_id
        WHERE pr.student_id = %s
    """ % student_id, conn)
    
    # Get fee data
    fee_summary_df = pd.read_sql("""
        SELECT 
            SUM(fs.amount) AS total_annual_fee,
            COALESCE((SELECT SUM(amount) FROM fee_payments WHERE student_id = %s), 0) AS amount_paid
        FROM fee_structure fs
        WHERE fs.academic_year = '2025-26'
    """ % student_id, conn)
    
    # Get payment history
    payment_history_df = pd.read_sql("""
        SELECT * FROM fee_payments WHERE student_id = %s ORDER BY payment_date DESC
    """ % student_id, conn)
    
    # Get schedule
    schedule_df = pd.read_sql("""
        SELECT 
            cs.day_of_week, cs.start_time, cs.end_time,
            sub.subject_name, t.teacher_name, cs.is_break
        FROM class_schedule cs
        LEFT JOIN subjects sub ON cs.subject_id = sub.subject_id
        LEFT JOIN teachers t ON cs.teacher_id = t.teacher_id
        WHERE cs.class = '%s' AND cs.section = '%s'
        ORDER BY FIELD(cs.day_of_week, 'Monday', 'Tuesday', 'Wednesday'), cs.start_time
    """ % (parent_student_df.iloc[0]['class'], parent_student_df.iloc[0]['section']), conn)
    
    conn.close()
    
    # Convert DataFrames to dictionaries for template
    return render_template('parent.html',
        parent=parent_student_df.iloc[0].to_dict(),
        progress_reports=progress_df.to_dict('records'),
        fee_summary=fee_summary_df.iloc[0].to_dict(),
        payment_history=payment_history_df.to_dict('records'),
        schedule_by_day=schedule_df.groupby('day_of_week').apply(lambda x: x.to_dict('records')).to_dict()
    )
