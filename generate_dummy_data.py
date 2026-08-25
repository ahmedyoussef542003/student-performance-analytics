import os
import random
import sqlite3

# المسار الفعلي لقاعدة البيانات
DB_PATH = (
    r"E:\BI Track of Data Camp\School App\dist\app\_internal\school_system.db"
)


def append_new_data(num_new_students=10):
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    print(
        f"🚀 جاري إضافة {num_new_students} طالبات جُدد مع بياناتهم إلى قاعدة البيانات..."
    )

    # 1. التأكد من وجود الجداول الهيكلية
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT UNIQUE NOT NULL,
            grade_level TEXT NOT NULL,
            class_name TEXT NOT NULL,
            section TEXT NOT NULL DEFAULT 'عام'
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Skills (
            skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            subject TEXT NOT NULL,
            skill_name TEXT NOT NULL,
            is_mastered INTEGER NOT NULL CHECK (is_mastered IN (0, 1)),
            FOREIGN KEY (student_id) REFERENCES Students (student_id) ON DELETE CASCADE
        )
    """)

    cursor.execute("""
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
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Attendance (
            attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            month_year TEXT NOT NULL,
            total_days INTEGER NOT NULL,
            attended_days INTEGER NOT NULL,
            FOREIGN KEY (student_id) REFERENCES Students (student_id) ON DELETE CASCADE,
            UNIQUE(student_id, month_year)
        )
    """)

    # جلب الأسماء الموجودة سابقاً لمنع التكرار
    cursor.execute("SELECT student_name FROM Students;")
    existing_names = set(row[0] for row in cursor.fetchall())

    # 2. توليد الطالبات الجدد
    first_names = [
        "سارة",
        "نورة",
        "مريم",
        "فاطمة",
        "ريم",
        "شهد",
        "الجوهرة",
        "ليان",
        "جود",
        "يارا",
    ]
    father_names = [
        "محمد",
        "أحمد",
        "عبدالله",
        "علي",
        "خالد",
        "سعود",
        "عمر",
        "إبراهيم",
    ]
    family_names = [
        "الغامدي",
        "الزهراني",
        "الشهري",
        "القحطاني",
        "الدوسري",
        "العتيبي",
    ]

    grades_list = [
        "الصف الأول المتوسط",
        "الصف الثاني المتوسط",
        "الصف الثالث المتوسط",
    ]
    classes_list = ["1/1", "1/2", "2/1", "2/2", "3/1"]
    sections = ["عام", "تحفيظ"]

    new_student_ids = []

    while len(new_student_ids) < num_new_students:
        name = f"{random.choice(first_names)} {random.choice(father_names)} {random.choice(family_names)}"
        if name in existing_names:
            name += f" {random.randint(1, 99)}"

        existing_names.add(name)
        grade = random.choice(grades_list)
        cls = random.choice(classes_list)
        sec = random.choice(sections)

        cursor.execute(
            "INSERT INTO Students (student_name, grade_level, class_name, section) VALUES (?, ?, ?, ?)",
            (name, grade, cls, sec),
        )
        new_student_ids.append(cursor.lastrowid)

    # 3. إدخال المهارات للطلبة الجدد (مع تضمين حالات تعثر لتجربة Power BI)
    skills_pool = [
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
        ("الرياضيات", "الهندسة والقياس"),
        ("العلوم", "التفكير العلمي والملاحظة"),
        ("العلوم", "فهم المفاهيم والتجارب"),
    ]

    for st_id in new_student_ids:
        for subj, sk_name in skills_pool:
            is_mastered = 1 if random.random() < 0.75 else 0
            cursor.execute(
                """
                INSERT INTO Skills (student_id, subject, skill_name, is_mastered)
                VALUES (?, ?, ?, ?)
            """,
                (st_id, subj, sk_name, is_mastered),
            )

    # 4. إدخال الدرجات للطلبة الجدد
    subjects_teachers = [
        ("اللغة العربية", "أ. أمل العتيبي"),
        ("English", "أ. سارة الغامدي"),
        ("الرياضيات", "أ. نورة الشهري"),
        ("العلوم", "أ. مريم القحطاني"),
    ]
    exam_types = ["اختبار قصير 1", "اختبار قصير 2", "منتصف الفصل", "النهائي"]

    for st_id in new_student_ids:
        for subj, teacher in subjects_teachers:
            for exam in exam_types:
                max_sc = (
                    100.0
                    if "النهائي" in exam
                    else (50.0 if "منتصف" in exam else 20.0)
                )
                # توليد درجات تتضمن نسب تعثر (أقل من 60%) لبعض الحالات
                min_ratio = 0.35 if random.random() < 0.20 else 0.60
                score = round(random.uniform(max_sc * min_ratio, max_sc), 1)
                percentage = round((score / max_sc) * 100, 2)

                cursor.execute(
                    """
                    INSERT INTO Grades (student_id, subject, teacher_name, exam_type, score, max_score, percentage, term)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        st_id,
                        subj,
                        teacher,
                        exam,
                        score,
                        max_sc,
                        percentage,
                        "الفصل الدراسي الأول",
                    ),
                )

    # 5. إدخال الحضور للطلبة الجدد
    months = ["2026-01", "2026-02", "2026-03", "2026-04", "2026-05"]
    for st_id in new_student_ids:
        for month in months:
            total_days = 20
            attended = random.randint(14, 20)
            cursor.execute(
                """
                INSERT OR IGNORE INTO Attendance (student_id, month_year, total_days, attended_days)
                VALUES (?, ?, ?, ?)
            """,
                (st_id, month, total_days, attended),
            )

    conn.commit()
    conn.close()
    print(
        f"✅ تم إضافة {num_new_students} طالبات بجميع بياناتهن بنجاح دون مسح البيانات القديمة!"
    )


if __name__ == "__main__":
    # يمكنك تغيير هذا الرقم لإضافة العدد المطلوب
    append_new_data(num_new_students=10)