import sqlite3
import os

def get_db_path():
    """تحديد المسار المطلق لقاعدة البيانات ليعمل بسلاسة مع Python و PyInstaller EXE"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "school_system.db")

def init_db():
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    # 1. جدول الطالبات (Primary Key)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT UNIQUE NOT NULL,
            grade_level TEXT NOT NULL,
            class_name TEXT NOT NULL
        )
    ''')

    # 2. جدول الدرجات والاختبارات (Fact Table)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Grades (
            grade_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            subject TEXT NOT NULL,
            teacher_name TEXT NOT NULL,
            exam_type TEXT NOT NULL,
            score REAL NOT NULL,
            max_score REAL NOT NULL,
            percentage REAL NOT NULL,
            term TEXT NOT NULL,
            FOREIGN KEY (student_id) REFERENCES Students (student_id) ON DELETE CASCADE
        )
    ''')

    # 3. جدول المهارات
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Skills (
            skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            subject TEXT NOT NULL,
            skill_name TEXT NOT NULL,
            is_mastered INTEGER NOT NULL CHECK (is_mastered IN (0, 1)),
            FOREIGN KEY (student_id) REFERENCES Students (student_id) ON DELETE CASCADE
        )
    ''')

    # 4. جدول الغياب والحضور
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Attendance (
            attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            status TEXT NOT NULL,
            date_str TEXT NOT NULL,
            FOREIGN KEY (student_id) REFERENCES Students (student_id) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()