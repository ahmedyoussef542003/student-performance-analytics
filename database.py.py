import sqlite3

def init_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 1. جدول الطالبات مع إضافة القسم
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT UNIQUE NOT NULL,
            grade_level TEXT,
            class_name TEXT,
            section TEXT DEFAULT 'عام'
        )
    ''')
    
    # 2. جدول الدرجات (نوع الاختبار مفتوح TEXT)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Grades (
            grade_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            subject TEXT,
            teacher_name TEXT,
            exam_type TEXT,
            score REAL,
            max_score REAL,
            percentage REAL,
            term TEXT,
            FOREIGN KEY (student_id) REFERENCES Students(student_id)
        )
    ''')
    
    # 3. جدول المهارات (يدعم عدة مهارات لكل طالب)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Skills (
            skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            subject TEXT,
            skill_name TEXT,
            is_mastered INTEGER,
            FOREIGN KEY (student_id) REFERENCES Students(student_id)
        )
    ''')
    
    conn.commit()
    conn.close()