"""
Migration: Add photo_path, aadhaar_path, marksheet_path columns to all student admission tables.
Safe to run multiple times (uses IF NOT EXISTS check via INFORMATION_SCHEMA).
"""
import mysql.connector
from config import Config

def add_columns():
    try:
        db = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        cursor = db.cursor()

        tables = [
            'admissions', 'admissions_v', 'admissions_vi', 'admissions_vii',
            'admissions_viii', 'admissions_ix', 'admissions_x', 'admissions_xi', 'admissions_xii'
        ]

        new_columns = [
            ('photo_path',    'VARCHAR(255) DEFAULT NULL'),
            ('aadhaar_path',  'VARCHAR(255) DEFAULT NULL'),
            ('marksheet_path','VARCHAR(255) DEFAULT NULL'),
        ]

        for table in tables:
            for col_name, col_def in new_columns:
                # Check if column already exists
                cursor.execute("""
                    SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
                    WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s AND COLUMN_NAME = %s
                """, (Config.DB_NAME, table, col_name))
                exists = cursor.fetchone()[0]
                if not exists:
                    cursor.execute(f"ALTER TABLE {table} ADD COLUMN {col_name} {col_def}")
                    print(f"  Added column '{col_name}' to table '{table}'")
                else:
                    print(f"  Column '{col_name}' already exists in '{table}' — skipped")

        db.commit()
        cursor.close()
        db.close()
        print("\nMigration complete!")
    except Exception as e:
        print(f"Migration error: {e}")
        import traceback; traceback.print_exc()

if __name__ == '__main__':
    add_columns()
