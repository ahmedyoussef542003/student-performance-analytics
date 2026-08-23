import sqlite3
import os
import customtkinter as ctk

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ProfessionalSchoolApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("نظام التحليل المدرسي الشامل | Dashboard")
        self.geometry("900x680")
        self.resizable(False, False)

        self.db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "school_system.db")
        self.init_db()

        # قائمة لتخزين صفوف عناصر المهارات الديناميكية
        self.skill_rows = []

        # --- Grid Layout (Sidebar + Main Content) ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 1. Sidebar Frame
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="نظام التحليل\nالمدرسي", font=("Segoe UI", 18, "bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 30))

        self.btn_grades = ctk.CTkButton(self.sidebar_frame, text="إدخال الدرجات", font=("Segoe UI", 14), command=self.show_grades_tab)
        self.btn_grades.grid(row=1, column=0, padx=15, pady=10, sticky="ew")

        self.btn_skills = ctk.CTkButton(self.sidebar_frame, text="تقييم المهارات", font=("Segoe UI", 14), fg_color="transparent", text_color=("gray10", "gray90"), command=self.show_skills_tab)
        self.btn_skills.grid(row=2, column=0, padx=15, pady=10, sticky="ew")

        self.btn_attendance = ctk.CTkButton(self.sidebar_frame, text="الغياب والحضور", font=("Segoe UI", 14), fg_color="transparent", text_color=("gray10", "gray90"), command=self.show_attendance_tab)
        self.btn_attendance.grid(row=3, column=0, padx=15, pady=10, sticky="ew")

        self.btn_db_info = ctk.CTkButton(self.sidebar_frame, text="بيانات الاتصال 🔍", font=("Segoe UI", 14), fg_color="transparent", text_color=("gray10", "gray90"), command=self.show_db_info_tab)
        self.btn_db_info.grid(row=4, column=0, padx=15, pady=10, sticky="ew")

        # 2. Main Container Area
        self.main_container = ctk.CTkFrame(self, corner_radius=15, fg_color="#1E1E1E")
        self.main_container.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        # Views setup
        self.views = {}
        self.setup_views()
        self.show_grades_tab()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def init_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Students (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT UNIQUE NOT NULL,
                grade_level TEXT NOT NULL,
                class_name TEXT NOT NULL,
                section TEXT NOT NULL DEFAULT 'عام'
            )
        ''')
        
        try:
            cursor.execute("ALTER TABLE Students ADD COLUMN section TEXT NOT NULL DEFAULT 'عام'")
        except sqlite3.OperationalError:
            pass

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
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Skills (
                skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                subject TEXT NOT NULL,
                skill_name TEXT NOT NULL,
                is_mastered INTEGER NOT NULL,
                FOREIGN KEY (student_id) REFERENCES Students (student_id) ON DELETE CASCADE
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Attendance (
                attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                status TEXT NOT NULL,
                date_str TEXT NOT NULL,
                FOREIGN KEY (student_id) REFERENCES Students (student_id) ON DELETE CASCADE
            )
        ''')
        conn.commit()
        conn.close()

    def get_or_create_student(self, cursor, name, grade, cls_name, section="عام"):
        cursor.execute("SELECT student_id, section FROM Students WHERE student_name = ?", (name,))
        row = cursor.fetchone()
        if row:
            student_id = row[0]
            if section != "عام" and row[1] != section:
                cursor.execute("UPDATE Students SET section = ? WHERE student_id = ?", (section, student_id))
            return student_id
        
        cursor.execute("INSERT INTO Students (student_name, grade_level, class_name, section) VALUES (?, ?, ?, ?)", 
                       (name, grade, cls_name, section))
        return cursor.lastrowid

    def setup_views(self):
        # ---------------- 1. Grades View ----------------
        v_grades = ctk.CTkFrame(self.main_container, fg_color="transparent")
        ctk.CTkLabel(v_grades, text="رصد درجات الاختبارات", font=("Segoe UI", 22, "bold")).pack(pady=(15, 20))

        scroll = ctk.CTkScrollableFrame(v_grades, width=600, height=520, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        self.g_student = self.create_input(scroll, "اسم الطالبة الثلاثي:")
        
        lbl_sec = ctk.CTkLabel(scroll, text="القسم:", font=("Segoe UI", 13))
        lbl_sec.pack(anchor="e", padx=50, pady=(5, 2))
        self.g_section = ctk.CTkComboBox(scroll, values=["عام", "تحفيظ"], width=500, height=38, justify="right", state="readonly")
        self.g_section.set("عام")
        self.g_section.pack(pady=4)

        self.g_grade = self.create_input(scroll, "الصف الدراسي:")
        self.g_class = self.create_input(scroll, "الفصل:")
        self.g_subject = self.create_input(scroll, "المادة:")
        self.g_teacher = self.create_input(scroll, "اسم المعلمة:")
        self.g_exam = self.create_input(scroll, "نوع الاختبار:")
        self.g_score = self.create_input(scroll, "الدرجة المستحقة:")
        self.g_max = self.create_input(scroll, "الدرجة العظمى:")

        btn = ctk.CTkButton(scroll, text="حفظ الدرجة في قاعدة البيانات", command=self.save_grade, height=42, width=500, font=("Segoe UI", 14, "bold"), fg_color="#2563EB", hover_color="#1D4ED8")
        btn.pack(pady=20)

        self.g_status = ctk.CTkLabel(scroll, text="", font=("Segoe UI", 13))
        self.g_status.pack()

        self.views["grades"] = v_grades

        # ---------------- 2. Dynamic Skills View ----------------
        v_skills = ctk.CTkFrame(self.main_container, fg_color="transparent")
        ctk.CTkLabel(v_skills, text="تقييم المهارات", font=("Segoe UI", 22, "bold")).pack(pady=(10, 10))
        
        scroll_skills = ctk.CTkScrollableFrame(v_skills, width=600, height=520, fg_color="transparent")
        scroll_skills.pack(fill="both", expand=True)

        self.s_student = self.create_input(scroll_skills, "اسم الطالبة:")
        self.s_subject = self.create_input(scroll_skills, "المادة:")

        # منطقة المهارات الديناميكية
        ctk.CTkLabel(scroll_skills, text="المهارات والتقييم:", font=("Segoe UI", 14, "bold")).pack(anchor="e", padx=50, pady=(15, 5))
        
        self.skills_container = ctk.CTkFrame(scroll_skills, fg_color="transparent")
        self.skills_container.pack(fill="x", padx=50, pady=5)

        # زر إضافة مهارة جديدة (+)
        btn_add_skill = ctk.CTkButton(
            scroll_skills, 
            text="+ إضافة مهارة أخرى", 
            command=self.add_skill_row, 
            height=32, 
            width=200, 
            font=("Segoe UI", 12, "bold"), 
            fg_color="#374151", 
            hover_color="#4B5563"
        )
        btn_add_skill.pack(anchor="e", padx=50, pady=5)

        btn_s = ctk.CTkButton(scroll_skills, text="حفظ جميع المهارات", command=self.save_skill, height=42, width=500, font=("Segoe UI", 14, "bold"), fg_color="#10B981", hover_color="#059669")
        btn_s.pack(pady=20)
        
        self.s_status = ctk.CTkLabel(scroll_skills, text="", font=("Segoe UI", 13))
        self.s_status.pack()

        self.views["skills"] = v_skills
        
        # إدراج صف المهارة الأول تلقائياً عند تشغيل الواجهة
        self.add_skill_row()

        # ---------------- 3. Attendance View ----------------
        v_att = ctk.CTkFrame(self.main_container, fg_color="transparent")
        ctk.CTkLabel(v_att, text="تسجيل الغياب والحضور", font=("Segoe UI", 22, "bold")).pack(pady=(15, 20))
        self.a_student = self.create_input(v_att, "اسم الطالبة:")

        lbl3 = ctk.CTkLabel(v_att, text="الحالة:", font=("Segoe UI", 13))
        lbl3.pack(anchor="e", padx=50, pady=(5, 2))
        self.a_status_combo = ctk.CTkComboBox(v_att, values=["حاضر", "غائب بعذر", "غائب بدون عذر", "تأخير"], width=500, height=38, justify="right", state="readonly")
        self.a_status_combo.set("حاضر")
        self.a_status_combo.pack(pady=5)

        self.a_date = self.create_input(v_att, "التاريخ (YYYY-MM-DD):")

        btn_a = ctk.CTkButton(v_att, text="حفظ حالة الحضور", command=self.save_attendance, height=42, width=500, font=("Segoe UI", 14, "bold"), fg_color="#EF4444", hover_color="#DC2626")
        btn_a.pack(pady=20)
        self.a_status = ctk.CTkLabel(v_att, text="", font=("Segoe UI", 13))
        self.a_status.pack()

        self.views["attendance"] = v_att

        # ---------------- 4. Database Info View ----------------
        v_db_info = ctk.CTkFrame(self.main_container, fg_color="transparent")
        ctk.CTkLabel(v_db_info, text="بيانات وقاعدة الاتصال", font=("Segoe UI", 22, "bold")).pack(pady=(15, 10))

        ctk.CTkLabel(v_db_info, text=":مسار قاعدة البيانات الحالي", font=("Segoe UI", 13, "bold")).pack(anchor="e", padx=30, pady=(10, 2))
        self.entry_db_path = ctk.CTkEntry(v_db_info, width=550, height=35, font=("Consolas", 11), justify="left")
        self.entry_db_path.pack(pady=5)
        self.entry_db_path.insert(0, self.db_path)
        self.entry_db_path.configure(state="readonly")

        self.scroll_db_info = ctk.CTkScrollableFrame(v_db_info, width=550, height=320, fg_color="#2B2B2B")
        self.scroll_db_info.pack(fill="both", expand=True, padx=20, pady=10)

        btn_refresh_db = ctk.CTkButton(v_db_info, text="تحديث فحص الاتصال 🔄", command=self.refresh_db_info, height=38, width=250, font=("Segoe UI", 13, "bold"))
        btn_refresh_db.pack(pady=10)

        self.views["db_info"] = v_db_info

    def add_skill_row(self):
        row_frame = ctk.CTkFrame(self.skills_container, fg_color="transparent")
        row_frame.pack(fill="x", pady=4)

        # زر حذف الصف
        btn_remove = ctk.CTkButton(
            row_frame, text="✕", width=30, height=36, 
            fg_color="#EF4444", hover_color="#B91C1C",
            command=lambda: self.remove_skill_row(row_frame)
        )
        btn_remove.pack(side="left", padx=(0, 5))

        # ComboBox حالة المهارة
        combo_status = ctk.CTkComboBox(
            row_frame, values=["متقن", "غير متقن"], 
            width=130, height=36, justify="right", state="readonly"
        )
        combo_status.set("متقن")
        combo_status.pack(side="left", padx=5)

        # Entry اسم المهارة
        entry_skill = ctk.CTkEntry(
            row_frame, placeholder_text="اسم المهارة", 
            width=320, height=36, justify="right", font=("Segoe UI", 13)
        )
        entry_skill.pack(side="right", fill="x", expand=True)

        self.skill_rows.append({
            "frame": row_frame,
            "entry": entry_skill,
            "combo": combo_status
        })

    def remove_skill_row(self, row_frame):
        if len(self.skill_rows) <= 1:
            return  # الإبقاء على صف واحد على الأقل
        
        self.skill_rows = [r for r in self.skill_rows if r["frame"] != row_frame]
        row_frame.destroy()

    def refresh_db_info(self):
        for widget in self.scroll_db_info.winfo_children():
            widget.destroy()

        tables = ["Students", "Grades", "Skills", "Attendance"]
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            ctk.CTkLabel(self.scroll_db_info, text="حالة الاتصال: متصل بنجاح ✅", font=("Segoe UI", 14, "bold"), text_color="#10B981").pack(pady=10)

            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                frame_row = ctk.CTkFrame(self.scroll_db_info, fg_color="#1E1E1E")
                frame_row.pack(fill="x", padx=10, pady=5)
                
                ctk.CTkLabel(frame_row, text=f"جدول {table}", font=("Segoe UI", 13, "bold")).pack(side="right", padx=15, pady=8)
                ctk.CTkLabel(frame_row, text=f"عدد السجلات: {count}", font=("Segoe UI", 13), text_color="#3B82F6").pack(side="left", padx=15, pady=8)

            conn.close()
        except Exception as e:
            ctk.CTkLabel(self.scroll_db_info, text=f"خطأ في الاتصال: {e} ❌", font=("Segoe UI", 13), text_color="#EF4444").pack(pady=10)

    def create_input(self, parent, label_text):
        lbl = ctk.CTkLabel(parent, text=label_text, font=("Segoe UI", 13))
        lbl.pack(anchor="e", padx=50, pady=(6, 2))
        entry = ctk.CTkEntry(parent, width=500, height=38, justify="right", font=("Segoe UI", 13))
        entry.pack(pady=4)
        return entry

    def switch_view(self, active_key):
        for key, view in self.views.items():
            if key == active_key:
                view.pack(fill="both", expand=True, padx=20, pady=20)
            else:
                view.pack_forget()

    def show_grades_tab(self):
        self.switch_view("grades")
        self.reset_sidebar_colors()
        self.btn_grades.configure(fg_color=("#3B82F6", "#1D4ED8"), text_color="white")

    def show_skills_tab(self):
        self.switch_view("skills")
        self.reset_sidebar_colors()
        self.btn_skills.configure(fg_color=("#3B82F6", "#1D4ED8"), text_color="white")

    def show_attendance_tab(self):
        self.switch_view("attendance")
        self.reset_sidebar_colors()
        self.btn_attendance.configure(fg_color=("#3B82F6", "#1D4ED8"), text_color="white")

    def show_db_info_tab(self):
        self.switch_view("db_info")
        self.reset_sidebar_colors()
        self.btn_db_info.configure(fg_color=("#3B82F6", "#1D4ED8"), text_color="white")
        self.refresh_db_info()

    def reset_sidebar_colors(self):
        for btn in [self.btn_grades, self.btn_skills, self.btn_attendance, self.btn_db_info]:
            btn.configure(fg_color="transparent", text_color=("gray10", "gray90"))

    def save_grade(self):
        student = self.g_student.get().strip()
        section = self.g_section.get()
        grade_lvl = self.g_grade.get().strip()
        cls_name = self.g_class.get().strip()
        subject = self.g_subject.get().strip()
        teacher = self.g_teacher.get().strip()
        exam = self.g_exam.get().strip()
        score_str = self.g_score.get().strip()
        max_str = self.g_max.get().strip()

        if not all([student, grade_lvl, cls_name, subject, teacher, exam, score_str, max_str]):
            self.g_status.configure(text="يرجى تعبئة جميع الحقول!", text_color="#EF4444")
            return

        try:
            score = float(score_str)
            max_score = float(max_str)
            percentage = (score / max_score) * 100

            conn = self.get_connection()
            cursor = conn.cursor()

            student_id = self.get_or_create_student(cursor, student, grade_lvl, cls_name, section)

            cursor.execute('''
                INSERT INTO Grades (student_id, subject, teacher_name, exam_type, score, max_score, percentage, term)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (student_id, subject, teacher, exam, score, max_score, percentage, "الفصل الأول"))

            conn.commit()
            conn.close()

            self.g_status.configure(text="تم حفظ الدرجة بنجاح!", text_color="#10B981")
            self.g_score.delete(0, 'end')
        except ValueError:
            self.g_status.configure(text="خطأ: يرجى كتابة أرقام فقط في الدرجات!", text_color="#EF4444")
        except Exception as e:
            self.g_status.configure(text=f"خطأ: {e}", text_color="#EF4444")

    def save_skill(self):
        student = self.s_student.get().strip()
        subject = self.s_subject.get().strip()

        if not student or not subject:
            self.s_status.configure(text="يرجى كتابة اسم الطالبة والمادة!", text_color="#EF4444")
            return

        valid_entries = []
        for r in self.skill_rows:
            sk_name = r["entry"].get().strip()
            is_m = 1 if r["combo"].get() == "متقن" else 0
            if sk_name:
                valid_entries.append((sk_name, is_m))

        if not valid_entries:
            self.s_status.configure(text="يرجى كتابة مهارة واحدة على الأقل!", text_color="#EF4444")
            return

        conn = self.get_connection()
        cursor = conn.cursor()
        student_id = self.get_or_create_student(cursor, student, "غير محدد", "غير محدد", "عام")

        for sk_name, is_m in valid_entries:
            cursor.execute("INSERT INTO Skills (student_id, subject, skill_name, is_mastered) VALUES (?, ?, ?, ?)",
                           (student_id, subject, sk_name, is_m))
        
        conn.commit()
        conn.close()

        self.s_status.configure(text=f"تم حفظ ({len(valid_entries)}) مهارة بنجاح!", text_color="#10B981")

        # إعادة ضبط خيارات المهارات إلى صف فارغ واحد
        for item in self.skill_rows:
            item["frame"].destroy()
        self.skill_rows.clear()
        self.add_skill_row()

    def save_attendance(self):
        student = self.a_student.get().strip()
        status = self.a_status_combo.get()
        date_str = self.a_date.get().strip()

        if not all([student, date_str]):
            self.a_status.configure(text="يرجى إدخال البيانات كاملة!", text_color="#EF4444")
            return

        conn = self.get_connection()
        cursor = conn.cursor()
        student_id = self.get_or_create_student(cursor, student, "غير محدد", "غير محدد", "عام")

        cursor.execute("INSERT INTO Attendance (student_id, status, date_str) VALUES (?, ?, ?)",
                       (student_id, status, date_str))
        conn.commit()
        conn.close()

        self.a_status.configure(text="تم حفظ حالة الحضور بنجاح!", text_color="#10B981")
        self.a_date.delete(0, 'end')

if __name__ == "__main__":
    app = ProfessionalSchoolApp()
    app.mainloop()