import sqlite3

def init_db(db_path="school_system.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # تفعيل قيود المفاتيح الأجنبية
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    # 1. جدول الطالبات
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT UNIQUE NOT NULL,
            grade_level TEXT NOT NULL,
            class_name TEXT NOT NULL,
            section TEXT NOT NULL DEFAULT 'عام'
        )
    ''')
    
    # 2. جدول دليل المهارات المعتمدة للمواد (Subject Skills Master)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Subject_Skills (
            skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            skill_name TEXT NOT NULL,
            description TEXT,
            UNIQUE(subject, skill_name)
        )
    ''')
    
    # 3. جدول تقييم مهارات الطالبات (Student Skill Evaluations)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Student_Skills_Evaluation (
            eval_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            skill_id INTEGER NOT NULL,
            is_mastered INTEGER NOT NULL CHECK (is_mastered IN (0, 1)),
            eval_date TEXT DEFAULT (DATE('now')),
            FOREIGN KEY (student_id) REFERENCES Students (student_id) ON DELETE CASCADE,
            FOREIGN KEY (skill_id) REFERENCES Subject_Skills (skill_id) ON DELETE CASCADE,
            UNIQUE(student_id, skill_id)
        )
    ''')
    
    # 4. جدول الدرجات الأكاديمية
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
    
    # 5. جدول الحضور والغياب الشهري
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Attendance (
            attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            month_year TEXT NOT NULL,
            total_days INTEGER NOT NULL,
            attended_days INTEGER NOT NULL,
            FOREIGN KEY (student_id) REFERENCES Students (student_id) ON DELETE CASCADE,
            UNIQUE(student_id, month_year)
        )
    ''')
    
    # تعبئة مهارات قياسية أولية للمواد (Seed Data)
    seed_skills(cursor)
    
    conn.commit()
    conn.close()

def seed_skills(cursor):
    """إضافة مهارات أولية معتمدة للغات والمواد"""
    default_skills = [
        # اللغة العربية
        ("اللغة العربية", "القراءة الجهرية والمعبرة"),
        ("اللغة العربية", "الفهم الاستيعابي والتحليل"),
        ("اللغة العربية", "التعبير الكتابي والإملاء"),
        ("اللغة العربية", "القواعد النحوية والصرفية"),
        
        # اللغة الإنجليزية
        ("English", "Reading Comprehension"),
        ("English", "Writing & Grammar"),
        ("English", "Listening & Speaking"),
        ("English", "Vocabulary Usage"),
        
        # الرياضيات
        ("الرياضيات", "العمليات الحسابية الأساسية"),
        ("الرياضيات", "حل المشكلات والتفكير الناقد"),
        ("الرياضيات", "الهندسة والقياس")
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO Subject_Skills (subject, skill_name) 
        VALUES (?, ?)
    ''', default_skills)

if __name__ == "__main__":
    init_db()
    print("تم تحديث هيكل قاعدة البيانات بنجاح!")