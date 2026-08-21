import sqlite3
import random

# قائمة بأسماء طالبات ومواد ومعلمات للتوليد العشوائي
students_list = [
    ("سارة أحمد", "الثاني المتوسط", "1/2"),
    ("نورة علي", "الثاني المتوسط", "1/2"),
    ("مريم محمد", "الثاني المتوسط", "2/2"),
    ("ريم خالد", "الثاني المتوسط", "2/2"),
    ("شهد عبد الله", "الثالث المتوسط", "1/3"),
    ("أمل يوسف", "الثالث المتوسط", "1/3"),
    ("فاطمة حسن", "الثالث المتوسط", "2/3"),
    ("منى إبراهيم", "الأول المتوسط", "1/1"),
    ("هدى طارق", "الأول المتوسط", "1/1"),
    ("زينب عمر", "الأول المتوسط", "2/1")
]

subjects_teachers = [
    ("رياضيات", "أ. نادية"),
    ("علوم", "أ. حنان"),
    ("لغتي", "أ. وفاء"),
    ("إنجليزي", "أ. سحر")
]

exam_types = ["اختبار قبلي", "اختبار فترة 1", "اختبار فترة 2", "اختبار بعدي"]
skills_list = ["حل المعادلات", "التفكير الناقد", "القراءة السريعة", "التجارب المعملية"]

def populate_data():
    conn = sqlite3.connect("school_system.db")
    cursor = conn.cursor()

    # 1. إدخال الطالبات
    for name, grade, cls in students_list:
        cursor.execute("INSERT INTO Students (student_name, grade_level, class_name) VALUES (?, ?, ?)", (name, grade, cls))

    # 2. إدخال درجات عشوائية
    for name, grade, cls in students_list:
        for subj, teacher in subjects_teachers:
            for exam in exam_types:
                score = round(random.uniform(12, 20), 1)
                max_score = 20.0
                percentage = (score / max_score) * 100
                cursor.execute('''
                    INSERT INTO Grades (student_name, subject, teacher_name, exam_type, score, max_score, percentage, term)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (name, subj, teacher, exam, score, max_score, percentage, "الفصل الأول"))

    # 3. إدخال تقييم مهارات عشوائي
    for name, grade, cls in students_list:
        for subj, teacher in subjects_teachers:
            skill = random.choice(skills_list)
            is_mastered = random.choice([0, 1])
            cursor.execute('''
                INSERT INTO Skills (student_name, subject, skill_name, is_mastered)
                VALUES (?, ?, ?, ?)
            ''', (name, subj, skill, is_mastered))

    conn.commit()
    conn.close()
    print("تم إدخال البيانات التجريبية بنجاح!")

if __name__ == "__main__":
    populate_data()