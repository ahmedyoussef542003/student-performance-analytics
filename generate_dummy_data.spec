import sqlite3
import random
import os

# مسار قاعدة البيانات
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "school_system.db")

def generate_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    print("⏳ جاري تنظيف البيانات القديمة وإنشاء بيانات تجريبية جديدة...")
    
    # تفريغ الجداول القديمة لإعادة التعبئة (اختياري)
    cursor.execute("DELETE FROM Attendance;")
    cursor.execute("DELETE FROM Student_Skills_Evaluation;")
    cursor.execute("DELETE FROM Grades;")
    cursor.execute("DELETE FROM Students;")
    cursor.execute("DELETE FROM Subject_Skills;")

    # 1. إدخال دليل المهارات المعتمدة للمواد (Subject_Skills)
    skills_data = [
        # اللغة العربية
        ("اللغة العربية", "القراءة الجهرية والمعبرة"),
        ("اللغة العربية", "الفهم الاستيعابي والتحليل"),
        ("اللغة العربية", "التعبير الكتابي والإملاء"),
        ("اللغة العربية", "القواعد النحوية والصرفية"),
        # English
        ("English", "Reading Comprehension"),
        ("English", "Writing & Grammar"),
        ("English", "Listening & Speaking"),
        ("English", "Vocabulary Usage"),
        # الرياضيات
        ("الرياضيات", "العمليات الحسابية الأساسية"),
        ("الرياضيات", "حل المشكلات والتفكير الناقد"),
        ("الرياضيات", "الهندسة والقياس"),
        # العلوم
        ("العلوم", "التفكير العلمي والملاحظة"),
        ("العلوم", "فهم المفاهيم والتجارب")
    ]
    cursor.executemany("INSERT INTO Subject_Skills (subject, skill_name) VALUES (?, ?)", skills_data)

    # جلب جميع المهارات مع id
    cursor.execute("SELECT skill_id, subject FROM Subject_Skills")
    all_skills = cursor.fetchall()

    # 2. توليد 40 طالبة
    first_names = ["سارة", "نورة", "مريم", "فاطمة", "ريم", "شهد", "الجوهرة", "ليان", "جود", "يارا", "حنين", "سلمى", "أسماء", "ريناد", "أميرة"]
    father_names = ["محمد", "أحمد", "عبدالله", "علي", "خالد", "سعود", "عمر", "إبراهيم", "يوسف", "حسن", "سعيد", "فهد"]
    family_names = ["الغامدي", "الزهراني", "الشهري", "القحطاني", "الدوسري", "العتيبي", "المطيري", "العنزي", "الحربي", "السيد"]

    grades_list = ["الصف الأول المتوسط", "الصف الثاني المتوسط", "الصف الثالث المتوسط"]
    classes_list = ["1/1", "1/2", "2/1", "2/2", "3/1"]
    sections = ["عام", "تحفيظ"]

    students = []
    student_ids = []

    for _ in range(40):
        name = f"{random.choice(first_names)} {random.choice(father_names)} {random.choice(family_names)}"
        # تلافي تكرار الأسماء
        while name in [s[0] for s in students]:
            name = f"{random.choice(first_names)} {random.choice(father_names)} {random.choice(family_names)}"
            
        grade = random.choice(grades_list)
        cls = random.choice(classes_list)
        sec = random.choice(sections)
        
        cursor.execute("INSERT INTO Students (student_name, grade_level, class_name, section) VALUES (?, ?, ?, ?)",
                       (name, grade, cls, sec))
        student_ids.append(cursor.lastrowid)

    print(f"✅ تم إنشاء {len(student_ids)} طالبة بنجاح.")

    # 3. توليد درجات الأكاديمية (Grades)
    subjects_teachers = [
        ("اللغة العربية", "أ. أمل العتيبي"),
        ("English", "أ. سارة الغامدي"),
        ("الرياضيات", "أ. نورة الشهري"),
        ("العلوم", "أ. مريم القحطاني"),
        ("الدراسات الإسلامية", "أ. فاطمة الدوسري")
    ]

    exam_types = ["اختبار قصير 1", "اختبار قصير 2", "منتصف الفصل", "النهائي"]
    terms = ["الفصل الدراسي الأول", "الفصل الدراسي الثاني"]

    grades_count = 0
    for st_id in student_ids:
        for subj, teacher in subjects_teachers:
            for exam in exam_types:
                max_sc = 100.0 if "النهائي" in exam else (50.0 if "منتصف" in exam else 20.0)
                # توليد درجات واقعية (تتراوح بين 60% و 100%)
                score = round(random.uniform(max_sc * 0.6, max_sc), 1)
                percentage = round((score / max_sc) * 100, 2)
                term = random.choice(terms)

                cursor.execute('''
                    INSERT INTO Grades (student_id, subject, teacher_name, exam_type, score, max_score, percentage, term)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (st_id, subj, teacher, exam, score, max_sc, percentage, term))
                grades_count += 1

    print(f"✅ تم إضافة {grades_count} سجل درجات.")

    # 4. توليد تقييم المهارات (Student_Skills_Evaluation)
    eval_count = 0
    for st_id in student_ids:
        # تقييم الطالبة في معظم المهارات المتاحة
        for sk_id, subj in all_skills:
            # 85% احتمال أن تكون الطالبة متقنة للمهارة
            is_mastered = 1 if random.random() < 0.85 else 0
            cursor.execute('''
                INSERT OR IGNORE INTO Student_Skills_Evaluation (student_id, skill_id, is_mastered)
                VALUES (?, ?, ?)
            ''', (st_id, sk_id, is_mastered))
            eval_count += 1

    print(f"✅ تم إضافة {eval_count} تقييم مهارة.")

    # 5. توليد سجلات الحضور والغياب الشهري (Attendance)
    months = ["2026-01", "2026-02", "2026-03", "2026-04", "2026-05"]
    att_count = 0
    for st_id in student_ids:
        for month in months:
            total_days = 20
            # أيام الحضور الفعلية بين 16 و 20 يوم
            attended = random.randint(16, 20)
            cursor.execute('''
                INSERT OR IGNORE INTO Attendance (student_id, month_year, total_days, attended_days)
                VALUES (?, ?, ?, ?)
            ''', (st_id, month, total_days, attended))
            att_count += 1

    print(f"✅ تم إضافة {att_count} سجل حضور شهري.")

    conn.commit()
    conn.close()
    print("\n🎉 تم إنشاء قاعدة البيانات المكتملة بنجاح وبها كافة البيانات التجريبية!")

if __name__ == "__main__":
    generate_data()