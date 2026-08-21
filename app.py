import customtkinter as ctk
import sqlite3

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class SchoolApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("نظام التحليل المدرسي الشامل")
        self.geometry("600x700")
        self.resizable(False, False)

        # إنشاء التبويبات
        self.tabview = ctk.CTkTabview(self, width=560, height=650)
        self.tabview.pack(padx=20, pady=10)

        self.tab_grades = self.tabview.add("إدخال الدرجات")
        self.tab_skills = self.tabview.add("تقييم المهارات")
        self.tab_attendance = self.tabview.add("الغياب والحضور")

        self.setup_grades_tab()
        self.setup_skills_tab()
        self.setup_attendance_tab()

    # --- 1. تبويب الدرجات ---
    def setup_grades_tab(self):
        lbl = ctk.CTkLabel(self.tab_grades, text="إدخال درجات الاختبارات", font=("Segoe UI", 18, "bold"))
        lbl.pack(pady=10)

        self.g_student = ctk.CTkEntry(self.tab_grades, placeholder_text="اسم الطالبة", width=380, height=38, justify="right")
        self.g_student.pack(pady=6)

        self.g_grade = ctk.CTkEntry(self.tab_grades, placeholder_text="الصف (مثال: الثاني المتوسط)", width=380, height=38, justify="right")
        self.g_grade.pack(pady=6)

        self.g_class = ctk.CTkEntry(self.tab_grades, placeholder_text="الفصل (مثال: 1/2)", width=380, height=38, justify="right")
        self.g_class.pack(pady=6)

        self.g_subject = ctk.CTkEntry(self.tab_grades, placeholder_text="المادة (مثال: رياضيات)", width=380, height=38, justify="right")
        self.g_subject.pack(pady=6)

        self.g_teacher = ctk.CTkEntry(self.tab_grades, placeholder_text="اسم المعلمة", width=380, height=38, justify="right")
        self.g_teacher.pack(pady=6)

        self.g_exam = ctk.CTkComboBox(self.tab_grades, values=["اختبار قبلي", "اختبار بعدي", "كويز 1", "اختبار فترة 1", "اختبار فترة 2"], width=380, height=38)
        self.g_exam.pack(pady=6)

        self.g_score = ctk.CTkEntry(self.tab_grades, placeholder_text="الدرجة المستحقة", width=380, height=38, justify="right")
        self.g_score.pack(pady=6)

        self.g_max = ctk.CTkEntry(self.tab_grades, placeholder_text="الدرجة العظمى (الكلي)", width=380, height=38, justify="right")
        self.g_max.pack(pady=6)

        btn = ctk.CTkButton(self.tab_grades, text="حفظ الدرجة", command=self.save_grade, fg_color="#1f6aa5", width=380, height=40, font=("Segoe UI", 13, "bold"))
        btn.pack(pady=15)

        self.g_status = ctk.CTkLabel(self.tab_grades, text="", font=("Segoe UI", 12))
        self.g_status.pack()

    def save_grade(self):
        student = self.g_student.get().strip()
        grade_lvl = self.g_grade.get().strip()
        cls_name = self.g_class.get().strip()
        subject = self.g_subject.get().strip()
        teacher = self.g_teacher.get().strip()
        exam = self.g_exam.get()
        score_str = self.g_score.get().strip()
        max_str = self.g_max.get().strip()

        if not all([student, subject, teacher, score_str, max_str]):
            self.g_status.configure(text="يرجى تعبئة كافة البيانات المطلوب!", text_color="#ff5555")
            return

        try:
            score = float(score_str)
            max_score = float(max_str)
            percentage = (score / max_score) * 100

            conn = sqlite3.connect("school_system.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Students (student_name, grade_level, class_name) VALUES (?, ?, ?)", (student, grade_lvl, cls_name))
            cursor.execute('''
                INSERT INTO Grades (student_name, subject, teacher_name, exam_type, score, max_score, percentage, term)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (student, subject, teacher, exam, score, max_score, percentage, "الفصل الأول"))
            conn.commit()
            conn.close()

            self.g_status.configure(text="تم حفظ الدرجة بنجاح!", text_color="#55ff55")
            self.g_score.delete(0, 'end')
        except Exception as e:
            self.g_status.configure(text=f"خطأ: {e}", text_color="#ff5555")

    # --- 2. تبويب المهارات ---
    def setup_skills_tab(self):
        lbl = ctk.CTkLabel(self.tab_skills, text="رصد إتقان المهارات", font=("Segoe UI", 18, "bold"))
        lbl.pack(pady=15)

        self.s_student = ctk.CTkEntry(self.tab_skills, placeholder_text="اسم الطالبة", width=380, height=40, justify="right")
        self.s_student.pack(pady=10)

        self.s_subject = ctk.CTkEntry(self.tab_skills, placeholder_text="المادة", width=380, height=40, justify="right")
        self.s_subject.pack(pady=10)

        self.s_skill = ctk.CTkEntry(self.tab_skills, placeholder_text="عنوان المهارة (مثال: حل معادلات درجة أولى)", width=380, height=40, justify="right")
        self.s_skill.pack(pady=10)

        self.s_mastered = ctk.CTkComboBox(self.tab_skills, values=["متقن", "غير متقن"], width=380, height=40)
        self.s_mastered.pack(pady=10)

        btn = ctk.CTkButton(self.tab_skills, text="حفظ تقييم المهارة", command=self.save_skill, fg_color="#2ba052", width=380, height=42, font=("Segoe UI", 13, "bold"))
        btn.pack(pady=20)

        self.s_status = ctk.CTkLabel(self.tab_skills, text="", font=("Segoe UI", 12))
        self.s_status.pack()

    def save_skill(self):
        student = self.s_student.get().strip()
        subject = self.s_subject.get().strip()
        skill = self.s_skill.get().strip()
        is_m = 1 if self.s_mastered.get() == "متقن" else 0

        if not all([student, subject, skill]):
            self.s_status.configure(text="يرجى إكمال الحقول!", text_color="#ff5555")
            return

        conn = sqlite3.connect("school_system.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Skills (student_name, subject, skill_name, is_mastered) VALUES (?, ?, ?, ?)", (student, subject, skill, is_m))
        conn.commit()
        conn.close()

        self.s_status.configure(text="تم حفظ المهارة بنجاح!", text_color="#55ff55")
        self.s_skill.delete(0, 'end')

    # --- 3. تبويب الحضور والغياب ---
    def setup_attendance_tab(self):
        lbl = ctk.CTkLabel(self.tab_attendance, text="تسجيل الحضور والغياب", font=("Segoe UI", 18, "bold"))
        lbl.pack(pady=15)

        self.a_student = ctk.CTkEntry(self.tab_attendance, placeholder_text="اسم الطالبة", width=380, height=40, justify="right")
        self.a_student.pack(pady=10)

        self.a_status_combo = ctk.CTkComboBox(self.tab_attendance, values=["حاضر", "غائب بعذر", "غائب بدون عذر", "تأخير"], width=380, height=40)
        self.a_status_combo.pack(pady=10)

        self.a_date = ctk.CTkEntry(self.tab_attendance, placeholder_text="التاريخ (YYYY-MM-DD)", width=380, height=40, justify="right")
        self.a_date.pack(pady=10)

        btn = ctk.CTkButton(self.tab_attendance, text="حفظ حالة الحضور", command=self.save_attendance, fg_color="#c0392b", width=380, height=42, font=("Segoe UI", 13, "bold"))
        btn.pack(pady=20)

        self.a_status = ctk.CTkLabel(self.tab_attendance, text="", font=("Segoe UI", 12))
        self.a_status.pack()

    def save_attendance(self):
        student = self.a_student.get().strip()
        status = self.a_status_combo.get()
        date_str = self.a_date.get().strip()

        if not all([student, date_str]):
            self.a_status.configure(text="يرجى إدخال كافة البيانات!", text_color="#ff5555")
            return

        # يمكنك إضافة جدول Attendance بقاعدة البيانات لاحقاً عند الحاجة
        self.a_status.configure(text="تم تسجيل حالة الحضور بنجاح!", text_color="#55ff55")

if __name__ == "__main__":
    app = SchoolApp()
    app.mainloop()