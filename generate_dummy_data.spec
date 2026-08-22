import sqlite3
import random
from datetime import datetime, timedelta
import os

# المسار الظاهر بالضبط في شاشة التطبيق لديك
db_path = r"E:\BI Track of Data Camp\School App\dist\app\_internal\school_system.db"

# التأكد من وجود الملف في المسار
if not os.path.exists(db_path):
    print(f"❌ الملف غير موجود في: {db_path}")
else:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 1. إضافة الطالبات
    students_data = [
        ("سارة أحمد محمد", "الصف الأول الثانوي", "1/1"),
        ("مريم محمود علي", "الصف الأول الثانوي", "1/1"),
        ("فاطمة عمر حسن", "الصف الأول الثانوي", "1/2"),
        ("نور خالد إبراهيم", "الصف الأول الثانوي", "1/2"),
        ("آية يوسف مصطفى", "الصف الثاني الثانوي", "2/1"),
        ("شهد طارق السيد", "الصف الثاني الثانوي", "2/1"),
        ("ريم عادل عبد الرحمن", "الصف الثاني الثانوي", "2/2"),
        ("هنا عمرو عبد الله", "الصف الثالث الثانوي", "3/1"),
        ("سلمى محمد فتحي", "الصف الثالث الثانوي", "3/1"),
        ("لجين أحمد سعيد", "الصف الثالث الثانوي", "3/2")
    ]

    student_ids = []
    for name, grade, cls in students_data:
        cursor.execute("INSERT OR IGNORE INTO Students (student_name, grade_level, class_name) VALUES (?, ?, ?)", (name, grade, cls))
        cursor.execute("SELECT student_id FROM Students WHERE student_name = ?", (name,))
        student_ids.append(cursor.fetchone()[0])

    # 2. إضافة الدرجات
    subjects = ["الرياضيات", "الفيزياء", "الكيمياء", "اللغة العربية", "اللغة الإنجليزية"]
    teachers = ["أ/ نادية", "أ/ إيمان", "أ/ سحر", "أ/ منى"]
    exam_types = ["اختبار قبلي", "كويز 1", "اختبار فترة 1", "اختبار فترة 2", "اختبار بعدي"]

    for s_id in student_ids:
        for subj in subjects:
            for exam in exam_types:
                max_score = 100.0 if "اختبار" in exam else 20.0
                score = round(random.uniform(max_score * 0.5, max_score), 1)
                percentage = round((score / max_score) * 100, 2)
                
                cursor.execute('''
                    INSERT INTO Grades (student_id, subject, teacher_name, exam_type, score, max_score, percentage, term)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (s_id, subj, random.choice(teachers), exam, score, max_score, percentage, "الفصل الأول"))

    # 3. إضافة المهارات
    skills_list = ["التفكير الناقد", "حل المشكلات", "التواصل الفعال", "العمل الجماعي", "التحليل البياني"]
    for s_id in student_ids:
        for subj in random.sample(subjects, 3):
            for skill in random.sample(skills_list, 2):
                is_m = random.choice([1, 1, 1, 0])
                cursor.execute('''
                    INSERT INTO Skills (student_id, subject, skill_name, is_mastered)
                    VALUES (?, ?, ?, ?)
                ''', (s_id, subj, skill, is_m))

    # 4. إضافة الحضور والغياب
    start_date = datetime.now() - timedelta(days=20)
    attendance_statuses = ["حاضر", "حاضر", "حاضر", "حاضر", "غائب بعذر", "غائب بدون عذر", "تأخير"]

    for day in range(15):
        current_date = (start_date + timedelta(days=day)).strftime('%Y-%m-%d')
        for s_id in student_ids:
            status = random.choice(attendance_statuses)
            cursor.execute('''
                INSERT INTO Attendance (student_id, status, date_str)
                VALUES (?, ?, ?)
            ''', (s_id, status, current_date))

    # حفظ وإغلاق الاتصال نهائياً
    conn.commit()
    conn.close()

    print("✅Data inserted successfully! Please click refresh in the app.")