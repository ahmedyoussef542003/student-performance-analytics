import sqlite3

def init_db():
    # السطر ده بيكرّت ملف قاعدة البيانات باسم school_system.db تلقائياً
    conn = sqlite3.connect("school_system.db")
    cursor = conn.cursor()
    
    # 1. جدول الطالبات والصفوف
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            grade_level TEXT NOT NULL,
            class_name TEXT NOT NULL
        )
    ''')
    
    # 2. جدول الدرجات والاختبارات
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Grades (
            grade_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            subject TEXT NOT NULL,
            teacher_name TEXT NOT NULL,
            exam_type TEXT NOT NULL,
            score REAL NOT NULL,
            max_score REAL NOT NULL,
            percentage REAL NOT NULL,
            term TEXT NOT NULL
        )
    ''')
    
    # 3. جدول المهارات
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Skills (
            skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            subject TEXT NOT NULL,
            skill_name TEXT NOT NULL,
            is_mastered INTEGER NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()
    print("تم إنشاء قاعدة البيانات بنجاح!")

if __name__ == "__main__":
    init_db()