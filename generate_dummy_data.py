import sqlite3
import random

DB_PATH = r"E:\BI Track of Data Camp\School App\dist\app\_internal\school_system.db"

FIRST_NAMES = ["شيماء", "سحر", "مريم", "فاطمة", "عائشة", "سارة", "نور", "سلمى", "آية", "خديجة", "زينب", "هاجر", "أميرة", "ياسمين", "شهد", "روان", "جنى", "فريدة", "حبيبة", "منة"]
FATHER_NAMES = ["محمود", "محمد", "عبدالله", "أحمد", "علي", "حسن", "حسين", "إبراهيم", "مصطفى", "عمر"]
FAMILY_NAMES = ["يوسف", "الشريف", "المصري", "السيد", "عبدالعزيز", "البكري", "النجار", "الحداد"]

GRADES = ["السادس", "الأول الثانوي", "الثاني الثانوي"]
CLASSES = ["6-1", "6-2", "1-1", "1-2"]
SECTIONS = ["عام", "تحفيظ"]

SUBJECTS_TEACHERS = {
    "رياضيات": "الاستاذة سحر",
    "اللغة العربية": "أ/ نادية",
    "English": "أ/ أمل"
}

EXAM_CONFIGS = [
    {"type": "منتصف الفصل", "max": 20.0},
    {"type": "النهائي", "max": 100.0},
    {"type": "كويز", "max": 5.0},
    {"type": "امتحان قبلي", "max": 5.0}
]

SKILLS_BY_SUBJECT = {
    "رياضيات": ["عمليات حسابيه", "حل المشكلات والتفكير الناقد", "الهندسة والقياس"],
    "اللغة العربية": ["القراءة الجهرية", "القواعد النحوية", "التعبير الكتابي"],
    "English": ["Reading Comprehension", "Grammar", "Vocabulary Usage"]
}

def generate_random_name(existing_names):
    while True:
        name = f"{random.choice(FIRST_NAMES)} {random.choice(FATHER_NAMES)} {random.choice(FAMILY_NAMES)}"
        if name not in existing_names:
            existing_names.add(name)
            return name

def seed_database_with_dummy_data(db_path=DB_PATH, num_students=20):
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()

    # 1. جدول الطلاب
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT UNIQUE NOT NULL,
            grade_level TEXT NOT NULL,
            class_name TEXT NOT NULL,
            section TEXT NOT NULL
        )
    ''')

    cursor.execute("PRAGMA table_info(Students)")
    cols_students = [column[1] for column in cursor.fetchall()]
    if "Student Status" not in cols_students:
        cursor.execute('ALTER TABLE Students ADD COLUMN "Student Status" TEXT')

    # 2. جدول الدرجات
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Grades (
            grade_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            subject TEXT NOT NULL,
            teacher_name TEXT NOT NULL,
            exam_type TEXT NOT NULL,
            score REAL NOT NULL,
            max_score REAL NOT NULL,
            percentage REAL,
            term TEXT NOT NULL,
            academic_year TEXT NOT NULL,
            FOREIGN KEY (student_id) REFERENCES Students (student_id) ON DELETE CASCADE
        )
    ''')

    # 3. جدول تقييم المهارات
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Student_Skills_Evaluation (
            skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            subject TEXT,
            skill_name TEXT NOT NULL,
            is_mastered INTEGER NOT NULL CHECK (is_mastered IN (0, 1)),
            FOREIGN KEY (student_id) REFERENCES Students (student_id) ON DELETE CASCADE
        )
    ''')

    cursor.execute("PRAGMA table_info(Student_Skills_Evaluation)")
    cols_skills = [column[1] for column in cursor.fetchall()]
    if "subject" not in cols_skills:
        cursor.execute('ALTER TABLE Student_Skills_Evaluation ADD COLUMN subject TEXT')

    # 4. جدول الحضور
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Attendance (
            attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            month_year TEXT NOT NULL,
            total_days INTEGER NOT NULL,
            attended_days INTEGER NOT NULL,
            FOREIGN KEY (student_id) REFERENCES Students (student_id) ON DELETE CASCADE
        )
    ''')

    existing_names = set()
    cursor.execute("SELECT student_name FROM Students")
    for row in cursor.fetchall():
        existing_names.add(row[0])

    print(f"🔄 جاري إضافة {num_students} طالبة وتحديث البيانات بنجاح...")

    for _ in range(num_students):
        student_name = generate_random_name(existing_names)
        grade_level = random.choice(GRADES)
        class_name = random.choice(CLASSES)
        section = random.choice(SECTIONS)

        status_profile = random.choices(
            ["ممتاز", "جيد جداً", "جيد", "مقبول", "ضعيف"],
            weights=[0.20, 0.30, 0.25, 0.15, 0.10]
        )[0]

        cursor.execute('''
            INSERT INTO Students (student_name, grade_level, class_name, section, "Student Status")
            VALUES (?, ?, ?, ?, ?)
        ''', (student_name, grade_level, class_name, section, status_profile))
        student_id = cursor.lastrowid

        if status_profile == "ممتاز":
            score_ratio_range = (0.88, 1.0)
            mastery_prob = 0.95
            attendance_range = (20, 22)
        elif status_profile == "جيد جداً":
            score_ratio_range = (0.75, 0.87)
            mastery_prob = 0.80
            attendance_range = (18, 21)
        elif status_profile == "جيد":
            score_ratio_range = (0.60, 0.74)
            mastery_prob = 0.60
            attendance_range = (15, 19)
        elif status_profile == "مقبول":
            score_ratio_range = (0.50, 0.59)
            mastery_prob = 0.40
            attendance_range = (12, 16)
        else:
            score_ratio_range = (0.20, 0.49)
            mastery_prob = 0.15
            attendance_range = (8, 13)

        terms = ["الفصل الأول", "الفصل الثاني"]
        for term in terms:
            for subject, teacher in SUBJECTS_TEACHERS.items():
                for exam in EXAM_CONFIGS:
                    max_s = exam["max"]
                    ratio = random.uniform(*score_ratio_range)
                    score = round(max_s * ratio, 1) if max_s > 5 else round(max_s * ratio)
                    percentage = round((score / max_s) * 100, 2)

                    cursor.execute('''
                        INSERT INTO Grades (student_id, subject, teacher_name, exam_type, score, max_score, percentage, term, academic_year)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (student_id, subject, teacher, exam["type"], score, max_s, percentage, term, "2025 - 2026"))

        for subject, skills in SKILLS_BY_SUBJECT.items():
            for skill_name in skills:
                is_mastered = 1 if random.random() < mastery_prob else 0
                cursor.execute('''
                    INSERT INTO Student_Skills_Evaluation (student_id, subject, skill_name, is_mastered)
                    VALUES (?, ?, ?, ?)
                ''', (student_id, subject, skill_name, is_mastered))

        months = ["2025-10", "2025-11", "2025-12", "2026-01"]
        for month in months:
            total_days = 22
            attended_days = random.randint(*attendance_range)
            cursor.execute('''
                INSERT INTO Attendance (student_id, month_year, total_days, attended_days)
                VALUES (?, ?, ?, ?)
            ''', (student_id, month, total_days, attended_days))

    conn.commit()
    conn.close()
    print("✅ تم إضافة البيانات الوهمية بنجاح بنسبة 100%!")

if __name__ == "__main__":
    seed_database_with_dummy_data()