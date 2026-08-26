import sqlite3
import customtkinter as ctk


class StudentReportPage(ctk.CTkFrame):

    def __init__(self, parent, db_path):
        super().__init__(parent, fg_color="transparent")
        self.db_path = db_path
        self.setup_ui()

    def setup_ui(self):
        title = ctk.CTkLabel(
            self,
            text="تقرير طالبة مفصل",
            font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
        )
        title.pack(pady=(10, 15))

        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.pack(fill="x", padx=20, pady=5)

        search_btn = ctk.CTkButton(
            search_frame, text="🔍 عرض التقرير", command=self.load_report
        )
        search_btn.pack(side="left", padx=10)

        self.student_entry = ctk.CTkEntry(
            search_frame,
            width=280,
            placeholder_text="ادخل اسم الطالبة...",
            justify="right",
        )
        self.student_entry.pack(side="right", padx=10)

        search_label = ctk.CTkLabel(
            search_frame,
            text=":اسم الطالبة للبحث",
            font=ctk.CTkFont(size=14),
        )
        search_label.pack(side="right", padx=10)

        self.container = ctk.CTkScrollableFrame(
            self, fg_color="#1e1e1e", corner_radius=10
        )
        self.container.pack(fill="both", expand=True, padx=20, pady=10)

    def render_table(self, title, headers, rows):
        table_frame = ctk.CTkFrame(
            self.container, fg_color="#2b2b2b", corner_radius=8
        )
        table_frame.pack(fill="x", expand=True, padx=10, pady=10)

        lbl_title = ctk.CTkLabel(
            table_frame,
            text=title,
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#60A5FA",
        )
        lbl_title.pack(anchor="e", padx=12, pady=(8, 4))

        h_frame = ctk.CTkFrame(table_frame, fg_color="#334155", height=30)
        h_frame.pack(fill="x", padx=8, pady=2)

        for idx, h in enumerate(headers):
            l = ctk.CTkLabel(
                h_frame,
                text=h,
                font=ctk.CTkFont(weight="bold"),
                text_color="white",
            )
            l.grid(row=0, column=idx, sticky="nsew", padx=4, pady=4)
            h_frame.grid_columnconfigure(idx, weight=1)

        if not rows:
            ctk.CTkLabel(
                table_frame, text="لا توجد بيانات متاحة", text_color="gray"
            ).pack(pady=8)
            return

        for r_idx, row in enumerate(rows):
            bg = "#1e293b" if r_idx % 2 == 0 else "#0f172a"
            r_frame = ctk.CTkFrame(table_frame, fg_color=bg)
            r_frame.pack(fill="x", padx=8, pady=1)

            for c_idx, val in enumerate(row):
                l = ctk.CTkLabel(
                    r_frame, text=str(val), font=ctk.CTkFont(size=12)
                )
                l.grid(row=0, column=c_idx, sticky="nsew", padx=4, pady=3)
                r_frame.grid_columnconfigure(c_idx, weight=1)

    def load_report(self):
        for child in self.container.winfo_children():
            child.destroy()

        name = self.student_entry.get().strip()
        if not name:
            return

        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        # تم تصحيح أسماء الأعمدة لتطابق الجدول الأصلي
        cur.execute(
            "SELECT student_id, student_name, grade_level, class_name, section"
            " FROM Students WHERE student_name LIKE ?",
            (f"%{name}%",),
        )
        student = cur.fetchone()

        if not student:
            ctk.CTkLabel(
                self.container,
                text="!لم يتم العثور على الطالبة",
                text_color="#EF4444",
                font=ctk.CTkFont(size=16),
            ).pack(pady=20)
            conn.close()
            return

        st_id, st_name, st_grade, st_class, st_section = student
        info = f"الاسم: {st_name} | الصف: {st_grade} | الفصل: {st_class} | القسم: {st_section}"
        ctk.CTkLabel(
            self.container,
            text=info,
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#38BDF8",
        ).pack(pady=10)

        # 1. الدرجات
        cur.execute(
            "SELECT subject, exam_type, score, max_score FROM Grades WHERE"
            " student_id = ?",
            (st_id,),
        )
        grades = [[g[0], g[1], f"{g[2]} / {g[3]}"] for g in cur.fetchall()]
        self.render_table(
            "سجل الدرجات والتقييمات",
            ["المادة", "نوع الاختبار", "الدرجة"],
            grades,
        )

        # 2. الحضور
        cur.execute(
            "SELECT month_year, total_days, attended_days FROM Attendance WHERE"
            " student_id = ?",
            (st_id,),
        )
        att = []
        for a in cur.fetchall():
            absent = a[1] - a[2]
            att.append([a[0], a[1], a[2], absent])
        self.render_table(
            "سجل الحضور والغياب الشهري",
            ["الشهر", "إجمالي الأيام", "أيام الحضور", "أيام الغياب"],
            att,
        )

        # 3. المهارات
        cur.execute(
            "SELECT subject, skill_name, is_mastered FROM Skills WHERE"
            " student_id = ?",
            (st_id,),
        )
        skills = [
            [s[0], s[1], "متقن ✅" if s[2] == 1 else "غير متقن ❌"]
            for s in cur.fetchall()
        ]
        self.render_table(
            "تقييم المهارات الأكاديمية",
            ["المادة", "المهارة", "الحالة"],
            skills,
        )

        conn.close()