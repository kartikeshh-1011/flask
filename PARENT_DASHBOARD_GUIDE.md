# Parent Dashboard Integration Guide

## 📋 Overview
This guide will help you integrate the parent dashboard with your MySQL database without modifying your main `app.py` structure.

## 🗄️ Step 1: Create Database Tables

1. Open MySQL Workbench or your MySQL command line
2. Run the SQL file: `parent_dashboard_database.sql`

```bash
mysql -u root -p school_db < parent_dashboard_database.sql
```

Or copy-paste the SQL commands from `parent_dashboard_database.sql` into MySQL Workbench.

## 📝 Step 2: Update Your parent.html Template

Replace the hardcoded data in `parent.html` with Jinja2 template variables:

### Example Changes:

**Before (Hardcoded):**
```html
<h2 class="parent-name">Mr. Rajesh Singh</h2>
<p class="parent-details">Parent of Aman Singh</p>
```

**After (Dynamic):**
```html
<h2 class="parent-name">{{ parent.parent_name }}</h2>
<p class="parent-details">Parent of {{ student.student_name }}</p>
```

### Key Template Variables Available:

- `{{ parent.parent_name }}` - Parent name
- `{{ student.student_name }}` - Student name
- `{{ student.attendance_percentage }}` - Attendance percentage
- `{{ student.overall_grade }}` - Overall grade
- `{{ fee_summary.total_annual_fee }}` - Total fee
- `{{ fee_summary.amount_paid }}` - Amount paid
- `{{ fee_summary.balance_due }}` - Balance due

### Loop Through Data:

**Progress Reports:**
```html
{% for report in progress_reports %}
<div class="subject-card">
    <h3>{{ report.subject_name }}</h3>
    <p>Teacher: {{ report.teacher_name }}</p>
    <span class="mark">{{ report.unit_test_1 }}/100</span>
    <div class="grade-badge">{{ report.grade }}</div>
</div>
{% endfor %}
```

**Payment History:**
```html
{% for payment in payment_history %}
<tr>
    <td>{{ payment.receipt_number }}</td>
    <td>{{ payment.payment_date }}</td>
    <td>{{ payment.description }}</td>
    <td>₹{{ payment.amount }}</td>
    <td>{{ payment.payment_mode }}</td>
    <td><span class="status-paid">{{ payment.status }}</span></td>
</tr>
{% endfor %}
```

**Class Schedule:**
```html
{% for day, classes in schedule_by_day.items() %}
<div class="day-schedule">
    <h3 class="day-name">{{ day }}</h3>
    <div class="schedule-items">
        {% for class in classes %}
        <div class="schedule-item {% if class.is_break %}break{% endif %}">
            <span class="time">{{ class.start_time }} - {{ class.end_time }}</span>
            <span class="subject">{{ class.subject }}</span>
            {% if not class.is_break %}
            <span class="teacher">{{ class.teacher }}</span>
            {% endif %}
        </div>
        {% endfor %}
    </div>
</div>
{% endfor %}
```

## 🔧 Step 3: Add Route to app.py

Open your `app.py` and add the parent dashboard route. You can copy the code from `parent_dashboard_code.py`:

```python
@app.route('/parent')
def parent_dashboard():
    # Get parent_id from session
    parent_id = session.get('parent_id', 1)
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # ... (copy all the queries from parent_dashboard_code.py)
    
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
```

## 🔐 Step 4: Set Parent ID in Session (During Login)

When a parent logs in, store their `parent_id` in the session:

```python
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    
    # Your authentication logic here
    # ...
    
    # If parent login successful:
    session['parent_id'] = parent_id  # Store parent_id
    session['role'] = 'parent'
    
    return redirect(url_for('parent_dashboard'))
```

## 📊 Step 5: Using Pandas (Optional)

If you prefer using pandas DataFrames for data manipulation:

```python
import pandas as pd

# Example: Get progress reports as DataFrame
progress_df = pd.read_sql("""
    SELECT * FROM progress_reports WHERE student_id = %s
""" % student_id, conn)

# Convert to dictionary for template
progress_reports = progress_df.to_dict('records')
```

## ✅ Step 6: Test Your Dashboard

1. Run your Flask app: `python app.py`
2. Navigate to: `http://localhost:5000/parent`
3. Check that all data is displaying correctly

## 🎨 Customization Tips

### Format Currency:
```python
# In Python
fee_summary['total_annual_fee'] = f"₹{fee_summary['total_annual_fee']:,.0f}"

# In Template
{{ "₹{:,.0f}".format(fee_summary.total_annual_fee) }}
```

### Format Dates:
```python
# Already formatted in SQL queries using DATE_FORMAT
# Example: DATE_FORMAT(payment_date, '%d %b %Y')
```

### Calculate Totals:
```python
# Calculate total from fee breakdown
total_fee = sum([item['amount'] for item in fee_breakdown])
```

## 🐛 Troubleshooting

**Issue: "Table doesn't exist"**
- Make sure you ran the SQL file completely
- Check database name in connection

**Issue: "No data showing"**
- Verify sample data was inserted
- Check parent_id in session
- Print variables to debug: `print(parent_student_data)`

**Issue: "Template not found"**
- Ensure `parent.html` is in `templates/` folder
- Check file name spelling

## 📚 Database Schema Summary

**Tables Created:**
- `students` - Student information
- `parents` - Parent information
- `subjects` - Subject details
- `teachers` - Teacher information
- `progress_reports` - Student marks and grades
- `fee_structure` - Fee breakdown
- `fee_payments` - Payment history
- `class_schedule` - Class timetable

## 🚀 Next Steps

1. ✅ Run SQL file to create tables
2. ✅ Update parent.html with Jinja2 variables
3. ✅ Add route to app.py
4. ✅ Test the dashboard
5. ✅ Customize as needed

---

**Need Help?** Check the comments in `parent_dashboard_code.py` for detailed explanations of each query.
