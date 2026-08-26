import sqlite3

def get_connection(db_path="school_system.db"):
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def seed_skills(cursor):
    """إضافة مهارات أولية معتمدة للغات والمواد"""
    default_skills = [
        ("اللغة العربية", "القراءة الجهرية والمعبرة"),
        ("اللغة العربية", "الفهم الاستيعابي والتحليل"),
        ("اللغة العربية", "التعبير الكتابي والإملاء"),
        ("اللغة العربية", "القواعد النحوية والصرفية"),
        ("English", "Reading Comprehension"),
        ("English", "Writing & Grammar"),
        ("English", "Listening & Speaking"),
        ("English", "Vocabulary Usage"),
        ("الرياضيات", "العمليات الحسابية الأساسية"),
        ("الرياضيات", "حل المشكلات والتفكير الناقد"),
        ("الرياضيات", "الهندسة والقياس")
    ]
    cursor.executemany('''
        INSERT OR IGNORE INTO Subject_Skills (subject, skill_name) 
        VALUES (?, ?)
    ''', default_skills)

def init_db(db_path="school_system.db"):
    conn = get_connection(db_path)
    cursor = conn.cursor()
    
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
    
    # 2. جدول دليل المهارات المعتمدة للمواد
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Subject_Skills (
            skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            skill_name TEXT NOT NULL,
            description TEXT,
            UNIQUE(subject, skill_name)
        )
    ''')
    
    # 3. جدول تقييم مهارات الطالبات
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
            academic_year TEXT NOT NULL DEFAULT '2025 - 2026',
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

    # التأكد من التوافقية عند إدخال عمود academic_year
    try:
        cursor.execute("ALTER TABLE Grades ADD COLUMN academic_year TEXT NOT NULL DEFAULT '2025 - 2026'")
    except sqlite3.OperationalError:
        pass
    
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
    
    seed_skills(cursor)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("تم تحديث هيكل قاعدة البيانات بنجاح!")