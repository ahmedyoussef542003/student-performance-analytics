import sqlite3
import random

# أسماء وبنى للبيانات الوهمية
FIRST_NAMES = [
    "مريم", "فاطمة", "عائشة", "سارة", "نور", "سلمى", "آية", "خديجة", "زينب", "هاجر",
    "أميرة", "ياسمين", "شهد", "روان", "جنى", "فريدة", "حبيبة", "منة", "هدى", "رقية",
    "منى", "سما", "مي", "ندى", "إيمان", "جهاد", "أسماء", "رضوى", "نوران", "داليا",
    "فرح", "اروى", "ميار", "تقى", "بسان", "ريماس", "جود", "لين", "هنا", "ميرنا"
]

FATHER_NAMES = [
    "أحمد", "محمد", "محمود", "علي", "حسن", "حسين", "إبراهيم", "مصطفى", "عبدالله", "عمر",
    "خالد", "يوسف", "سيد", "طارق", "سامح", "عادل", "جمال", "صلاح", "هشام", "أشرف"
]

FAMILY_NAMES = [
    "الشريف", "المصري", "السيد", "عبدالعزيز", "البكري", "النجار", "الحداد", "العربي",
    "شاهين", "فهمي", "رضوان", "سليمان", "منصور", "زكي", "طه", "خليفة"
]

CLASSES = ["1/1", "1/2", "2/1", "2/2", "3/1", "3/2"]
GRADES = ["الأول الثانوي", "الثاني الثانوي", "الثالث الثانوي"]
SUBJECTS = ["اللغة العربية", "English", "الرياضيات"]
EXAM_TYPES = ["منتصف الفصل", "الاختبار النهائي", "اختبار قصير"]
TEACHERS = ["أ/ نادية", "أ/ أمل", "أ/ فاطمة", "أ/ وفاء"]

# مسار قاعدة البيانات المباشر من الصورة
DB_PATH = r"E:\BI Track of Data Camp\School App\dist\app\_internal\school_system.db"

def generate_random_name(existing_names):
    while True:
        name = f"{random.choice(FIRST_NAMES)} {random.choice(FATHER_NAMES)} {random.choice(FAMILY_NAMES)}"
        if name not in existing_names:
            existing_names.add(name)
            return name

def add_new_students(db_path=DB_PATH, num_students=40):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    existing_names = set()
    cursor.execute("SELECT student_name FROM Students")
    for row in cursor.fetchall():
        existing_names.add(row[0])

    print(f"🔄 جاري إضافة {num_students} طالبة إلى قاعدة البيانات في المسار المطلب...")

    cursor.execute("SELECT skill_id, subject FROM Subject_Skills")
    skills_pool = cursor.fetchall()

    for _ in range(num_students):
        student_name = generate_random_name(existing_names)
        grade_level = random.choice(GRADES)
        class_name = random.choice(CLASSES)
        section = random.choice(["عام", "عام", "تحفيظ"])

        cursor.execute('''
            INSERT INTO Students (student_name, grade_level, class_name, section)
            VALUES (?, ?, ?, ?)
        ''', (student_name, grade_level, class_name, section))
        student_id = cursor.lastrowid

        performance_profile = random.choices(
            ["high", "average", "low"], 
            weights=[0.20, 0.50, 0.30]
        )[0]

        for subject in SUBJECTS:
            for exam_type in EXAM_TYPES:
                max_score = 100.0 if exam_type != "اختبار قصير" else 20.0

                if performance_profile == "high":
                    score = round(random.uniform(max_score * 0.85, max_score), 1)
                elif performance_profile == "average":
                    score = round(random.uniform(max_score * 0.50, max_score * 0.84), 1)
                else:
                    score = round(random.uniform(max_score * 0.20, max_score * 0.49), 1)

                percentage = round((score / max_score) * 100, 2)
                teacher = random.choice(TEACHERS)

                cursor.execute('''
                    INSERT INTO Grades (student_id, academic_year, subject, teacher_name, exam_type, score, max_score, percentage, term)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (student_id, "2025 - 2026", subject, teacher, exam_type, score, max_score, percentage, "الفصل الأول"))

        for skill_id, subject in skills_pool:
            if performance_profile == "high":
                is_mastered = 1 if random.random() < 0.95 else 0
            elif performance_profile == "average":
                is_mastered = 1 if random.random() < 0.65 else 0
            else:
                is_mastered = 1 if random.random() < 0.25 else 0

            cursor.execute('''
                INSERT OR IGNORE INTO Student_Skills_Evaluation (student_id, skill_id, is_mastered)
                VALUES (?, ?, ?)
            ''', (student_id, skill_id, is_mastered))

        months = ["2025-10", "2025-11", "2025-12", "2026-01"]
        for month in months:
            total_days = 22
            if performance_profile == "high":
                attended = random.randint(20, 22)
            elif performance_profile == "average":
                attended = random.randint(16, 21)
            else:
                attended = random.randint(8, 15)

            cursor.execute('''
                INSERT OR IGNORE INTO Attendance (student_id, month_year, total_days, attended_days)
                VALUES (?, ?, ?, ?)
            ''', (student_id, month, total_days, attended))

    conn.commit()
    conn.close()
    print("✅ تم إدخال 40 طالبة بنجاح في قاعدة بيانات التطبيق! اضغط Refresh في Power BI الآن.")

if __name__ == "__main__":
    add_new_students()