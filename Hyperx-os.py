import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
import shutil
import os
import platform
from PIL import Image, ImageTk
import threading
import time
from datetime import datetime


class ZUOperatingSystem:
    def __init__(self, root):
        """تهيئة نظام التشغيل ZU"""
        self.root = root
        self.setup_main_window()
        self.setup_styles()
        self.copied_file = None
        self.current_opened_windows = []
        self.create_taskbar()
        self.create_desktop()
        self.create_start_menu()

    def setup_main_window(self):
        """إعداد النافذة الرئيسية"""
        self.root.title("ZU Operating System")
        self.root.geometry("1024x768")
        self.root.minsize(800, 600)
        
        # تحميل صورة الخلفية بطريقة آمنة
        try:
            self.background_image = tk.PhotoImage(file='''v.png''')
            self.background_label = tk.Label(self.root, image=self.background_image)
            self.background_label.place(relwidth=1, relheight=1)
        except Exception as e:
            print(f"تعذر تحميل صورة الخلفية: {e}")
            self.root.configure(bg="#005080")  # لون خلفية بديل

    def setup_styles(self):
        """إعداد الأنماط للواجهة"""
        self.style = ttk.Style()
        self.style.configure("TButton", padding=6, relief="flat", background="#E1E1E1")
        self.style.configure("TFrame", background="#F0F0F0")
        self.style.configure("Treeview", font=('Arial', 10))
        self.style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))

    def create_taskbar(self):
        """إنشاء شريط المهام"""
        self.taskbar = tk.Frame(self.root, bg="#333333", height=50)
        self.taskbar.pack(side=tk.BOTTOM, fill=tk.X)

        # زر القائمة ابدأ
        self.start_button = tk.Button(
            self.taskbar, text="ابدأ", font=("Arial", 11, "bold"),
            bg="#0078D7", fg="white", relief="flat", width=8, height=1,
            command=self.toggle_start_menu
        )
        self.start_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # زر متصفح الملفات
        self.file_explorer_button = tk.Button(
            self.taskbar, text="متصفح الملفات", font=("Arial", 10),
            bg="#555555", fg="white", relief="flat",
            command=self.open_file_explorer
        )
        self.file_explorer_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # زر المحرر النصي
        self.text_editor_button = tk.Button(
            self.taskbar, text="المحرر النصي", font=("Arial", 10),
            bg="#555555", fg="white", relief="flat",
            command=lambda: self.open_text_editor()
        )
        self.text_editor_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # عرض الساعة
        self.clock_label = tk.Label(
            self.taskbar, font=("Arial", 10), bg="#333333", fg="white"
        )
        self.clock_label.pack(side=tk.RIGHT, padx=10)
        self.update_clock()

    def create_desktop(self):
        """إنشاء سطح المكتب"""
        self.desktop_icons_frame = tk.Frame(self.root, bg="#F0F0F0", width=200)
        self.desktop_icons_frame.pack(side=tk.LEFT, fill=tk.Y, anchor="nw", padx=10, pady=10)
        
        # إنشاء أيقونات سطح المكتب
        self.create_desktop_icon("متصفح الملفات", "📁", self.open_file_explorer)
        self.create_desktop_icon("المحرر النصي", "📝", lambda: self.open_text_editor())
        self.create_desktop_icon("عارض الصور", "🖼️", lambda: messagebox.showinfo("عارض الصور", "قم بفتح صورة من متصفح الملفات"))
        self.create_desktop_icon("حول", "ℹ️", self.show_about)

    def create_desktop_icon(self, text, icon, command):
        """إنشاء أيقونة على سطح المكتب"""
        icon_frame = tk.Frame(self.desktop_icons_frame, bg="#F0F0F0")
        icon_frame.pack(side=tk.TOP, pady=10)
        
        icon_button = tk.Button(
            icon_frame, text=icon, font=("Arial", 24), 
            bg="#F0F0F0", relief="flat", command=command
        )
        icon_button.pack()
        
        icon_label = tk.Label(
            icon_frame, text=text, font=("Arial", 9),
            bg="#F0F0F0"
        )
        icon_label.pack()

    def create_start_menu(self):
        """إنشاء قائمة ابدأ"""
        self.start_menu = tk.Frame(self.root, bg="#222222", width=250, height=400)
        self.start_menu_visible = False
        
        # معلومات المستخدم
        user_frame = tk.Frame(self.start_menu, bg="#333333", height=50)
        user_frame.pack(fill=tk.X)
        
        username = os.getlogin() if hasattr(os, 'getlogin') else "المستخدم"
        user_label = tk.Label(
            user_frame, text=f"👤 {username}", font=("Arial", 12, "bold"),
            bg="#333333", fg="white", anchor="w", padx=10, pady=5
        )
        user_label.pack(fill=tk.X)
        
        # العناصر في القائمة
        menu_items = [
            ("متصفح الملفات", self.open_file_explorer),
            ("المحرر النصي", lambda: self.open_text_editor()),
            ("حول النظام", self.show_about),
            ("إعدادات النظام", lambda: messagebox.showinfo("إعدادات", "إعدادات النظام غير متاحة حاليًا")),
            ("إيقاف التشغيل", self.shutdown)
        ]
        
        for text, command in menu_items:
            menu_button = tk.Button(
                self.start_menu, text=text, font=("Arial", 11),
                bg="#222222", fg="white", relief="flat", anchor="w",
                padx=15, pady=10, width=25, command=command
            )
            menu_button.pack(fill=tk.X)
            # تغيير لون الزر عند تمرير الماوس
            menu_button.bind("<Enter>", lambda e, b=menu_button: b.configure(bg="#444444"))
            menu_button.bind("<Leave>", lambda e, b=menu_button: b.configure(bg="#222222"))

    def toggle_start_menu(self):
        """عرض أو إخفاء قائمة ابدأ"""
        if self.start_menu_visible:
            self.start_menu.place_forget()
            self.start_menu_visible = False
        else:
            self.start_menu.place(x=0, y=self.root.winfo_height() - 450)
            self.start_menu_visible = True
            # إخفاء القائمة عند النقر في أي مكان آخر
            self.root.bind("<Button-1>", self.hide_start_menu)

    def hide_start_menu(self, event):
        """إخفاء قائمة ابدأ عند النقر في مكان آخر"""
        if self.start_menu_visible:
            # تحقق إذا كان النقر خارج حدود القائمة وخارج زر البدء
            x, y = event.x, event.y
            start_menu_coords = (
                self.start_menu.winfo_x(), self.start_menu.winfo_y(),
                self.start_menu.winfo_x() + self.start_menu.winfo_width(),
                self.start_menu.winfo_y() + self.start_menu.winfo_height()
            )
            start_button_coords = (
                self.start_button.winfo_rootx() - self.root.winfo_rootx(),
                self.start_button.winfo_rooty() - self.root.winfo_rooty(),
                self.start_button.winfo_rootx() - self.root.winfo_rootx() + self.start_button.winfo_width(),
                self.start_button.winfo_rooty() - self.root.winfo_rooty() + self.start_button.winfo_height()
            )
            
            in_start_menu = (start_menu_coords[0] <= x <= start_menu_coords[2] and 
                             start_menu_coords[1] <= y <= start_menu_coords[3])
                             
            in_start_button = (start_button_coords[0] <= x <= start_button_coords[2] and 
                               start_button_coords[1] <= y <= start_button_coords[3])
                               
            if not (in_start_menu or in_start_button):
                self.start_menu.place_forget()
                self.start_menu_visible = False
                self.root.unbind("<Button-1>")

    def update_clock(self):
        """تحديث الساعة في شريط المهام"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.clock_label.config(text=current_time)
        self.root.after(1000, self.update_clock)

    def open_file_explorer(self):
        """فتح متصفح الملفات"""
        explorer_window = tk.Toplevel(self.root)
        explorer_window.title("متصفح الملفات")
        explorer_window.geometry("800x600")
        explorer_window.minsize(600, 400)
        self.current_opened_windows.append(explorer_window)
        
        # شريط الأدوات
        toolbar = tk.Frame(explorer_window, bg="#F0F0F0")
        toolbar.pack(fill=tk.X)
        
        # زر العودة للمجلد الأب
        back_button = tk.Button(toolbar, text="⬆️ للأعلى", command=lambda: self.go_up_directory())
        back_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # زر تحديث
        refresh_button = tk.Button(toolbar, text="🔄 تحديث", command=lambda: self.refresh_directory())
        refresh_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # شريط المسار
        self.path_var = tk.StringVar()
        path_entry = tk.Entry(toolbar, textvariable=self.path_var, width=50)
        path_entry.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
        path_entry.bind("<Return>", lambda e: self.navigate_to_path())
        
        # زر الانتقال
        go_button = tk.Button(toolbar, text="انتقال", command=self.navigate_to_path)
        go_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # الإطار الرئيسي
        main_frame = tk.Frame(explorer_window)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # شريط جانبي للأماكن المفضلة
        sidebar = tk.Frame(main_frame, width=150, bg="#EEEEEE")
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)
        
        # عناوين المفضلة
        favorites_label = tk.Label(sidebar, text="الأماكن المفضلة", bg="#EEEEEE", font=("Arial", 10, "bold"))
        favorites_label.pack(fill=tk.X, padx=5, pady=5)
        
        # أزرار الاختصارات
        shortcuts = [
            ("المستندات", os.path.join(os.path.expanduser("~"), "Documents")),
            ("التنزيلات", os.path.join(os.path.expanduser("~"), "Downloads")),
            ("الصور", os.path.join(os.path.expanduser("~"), "Pictures")),
            ("سطح المكتب", os.path.join(os.path.expanduser("~"), "Desktop")),
            ("المجلد الرئيسي", os.path.expanduser("~"))
        ]
        
        for name, path in shortcuts:
            if os.path.exists(path):
                shortcut_button = tk.Button(
                    sidebar, text=name, relief="flat", anchor="w",
                    bg="#EEEEEE", padx=10,
                    command=lambda p=path: self.load_directory(p)
                )
                shortcut_button.pack(fill=tk.X, pady=2)
        
        # إطار العرض الرئيسي
        content_frame = tk.Frame(main_frame)
        content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # شريط التمرير
        scrollbar = tk.Scrollbar(content_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # شجرة العرض مع أعمدة
        self.tree = ttk.Treeview(content_frame, columns=("size", "type", "modified"), show="headings", yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)
        
        # تهيئة الأعمدة
        self.tree.heading("size", text="الحجم")
        self.tree.heading("type", text="النوع")
        self.tree.heading("modified", text="تاريخ التعديل")
        
        # ضبط عرض الأعمدة
        self.tree.column("size", width=100, anchor="e")
        self.tree.column("type", width=100)
        self.tree.column("modified", width=150)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # ربط الحدث بالنقر المزدوج وزر الفأرة الأيمن
        self.tree.bind("<Double-1>", self.open_selected_item)
        self.tree.bind("<Button-3>", self.show_context_menu)
        
        # قائمة السياق
        self.context_menu = tk.Menu(explorer_window, tearoff=0)
        self.context_menu.add_command(label="فتح", command=lambda: self.open_selected_item(None))
        self.context_menu.add_separator()
        self.context_menu.add_command(label="نسخ", command=self.copy_file)
        self.context_menu.add_command(label="لصق", command=self.paste_file)
        self.context_menu.add_command(label="إعادة تسمية", command=self.rename_file)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="حذف", command=self.delete_file)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="إنشاء مجلد", command=self.create_new_folder)
        self.context_menu.add_command(label="إنشاء ملف نصي", command=self.create_new_text_file)
        
        # حفظ مرجع للنافذة والشجرة
        self.explorer_window = explorer_window
        
        # تحميل المجلد الحالي
        self.current_dir = os.getcwd()
        self.load_directory(self.current_dir)
        
        # تحديث عنوان النافذة عند إغلاقها
        explorer_window.protocol("WM_DELETE_WINDOW", lambda: self.close_window(explorer_window))

    def load_directory(self, path):
        """تحميل محتويات المجلد"""
        if not os.path.exists(path):
            messagebox.showerror("خطأ", f"المسار غير موجود: {path}")
            return
            
        try:
            # مسح المحتويات الحالية للشجرة
            self.tree.delete(*self.tree.get_children())
            
            # تحديث المتغيرات
            self.current_dir = path
            self.path_var.set(path)
            self.explorer_window.title(f"متصفح الملفات - {path}")
            
            # إضافة المجلدات أولاً ثم الملفات
            folders = []
            files = []
            
            for entry in os.scandir(path):
                modified_time = datetime.fromtimestamp(os.path.getmtime(entry.path)).strftime("%Y-%m-%d %H:%M")
                
                if entry.is_dir():
                    folders.append((entry.name, "", "مجلد", modified_time))
                else:
                    size = self.get_human_readable_size(os.path.getsize(entry.path))
                    file_type = self.get_file_type(entry.name)
                    files.append((entry.name, size, file_type, modified_time))
            
            # إضافة المجلدات بترتيب أبجدي
            for name, size, file_type, modified in sorted(folders, key=lambda x: x[0].lower()):
                self.tree.insert("", "end", values=("📁 " + name, size, file_type, modified))
                
            # إضافة الملفات بترتيب أبجدي
            for name, size, file_type, modified in sorted(files, key=lambda x: x[0].lower()):
                icon = self.get_file_icon(name)
                self.tree.insert("", "end", values=(icon + " " + name, size, file_type, modified))
                
        except PermissionError:
            messagebox.showerror("خطأ", f"ليس لديك صلاحية الوصول إلى المجلد: {path}")
        except Exception as e:
            messagebox.showerror("خطأ", f"تعذر تحميل المجلد: {e}")

    def get_human_readable_size(self, size_bytes):
        """تحويل حجم الملف إلى صيغة مقروءة"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024
            i += 1
            
        return f"{size_bytes:.2f} {size_names[i]}"

    def get_file_type(self, filename):
        """الحصول على نوع الملف من امتداده"""
        extension = os.path.splitext(filename)[1].lower()
        
        file_types = {
            ".txt": "ملف نصي",
            ".py": "ملف بايثون",
            ".jpg": "صورة JPEG",
            ".jpeg": "صورة JPEG",
            ".png": "صورة PNG",
            ".gif": "صورة GIF",
            ".pdf": "مستند PDF",
            ".doc": "مستند Word",
            ".docx": "مستند Word",
            ".xls": "جدول Excel",
            ".xlsx": "جدول Excel",
            ".ppt": "عرض تقديمي",
            ".pptx": "عرض تقديمي",
            ".mp3": "ملف صوتي",
            ".mp4": "ملف فيديو",
            ".zip": "ملف مضغوط",
            ".rar": "ملف مضغوط"
        }
        
        return file_types.get(extension, f"ملف {extension}" if extension else "ملف")

    def get_file_icon(self, filename):
        """تحديد رمز مناسب للملف حسب نوعه"""
        extension = os.path.splitext(filename)[1].lower()
        
        icons = {
            ".txt": "📄",
            ".py": "🐍",
            ".jpg": "🖼️",
            ".jpeg": "🖼️",
            ".png": "🖼️",
            ".gif": "🖼️",
            ".pdf": "📕",
            ".doc": "📘",
            ".docx": "📘",
            ".xls": "📊",
            ".xlsx": "📊",
            ".ppt": "📺",
            ".pptx": "📺",
            ".mp3": "🎵",
            ".mp4": "🎬",
            ".zip": "🗜️",
            ".rar": "🗜️"
        }
        
        return icons.get(extension, "📄")

    def open_selected_item(self, event):
        """فتح العنصر المحدد"""
        selected_items = self.tree.selection()
        if not selected_items:
            return
            
        selected_item = selected_items[0]
        item_data = self.tree.item(selected_item, "values")
        item_name = item_data[0].split(" ", 1)[1]  # إزالة الأيقونة من الاسم
        
        file_path = os.path.join(self.current_dir, item_name)
        
        if "📁" in item_data[0]:  # إذا كان مجلد
            self.load_directory(file_path)
        elif os.path.exists(file_path):  # إذا كان ملف
            if file_path.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
                self.open_image_viewer(file_path)
            elif file_path.lower().endswith((".txt", ".py", ".html", ".css", ".js")):
                self.open_text_editor(file_path)
            else:
                try:
                    # محاولة فتح الملف بالبرنامج الافتراضي
                    if platform.system() == "Windows":
                        os.startfile(file_path)
                    elif platform.system() == "Darwin":  # macOS
                        os.system(f"open '{file_path}'")
                    else:  # Linux
                        os.system(f"xdg-open '{file_path}'")
                except:
                    messagebox.showinfo("معلومات", f"لا يمكن فتح الملف: {item_name}")

    def navigate_to_path(self):
        """الانتقال إلى المسار المدخل"""
        path = self.path_var.get()
        if os.path.exists(path) and os.path.isdir(path):
            self.load_directory(path)
        else:
            messagebox.showerror("خطأ", f"المسار غير صالح: {path}")

    def go_up_directory(self):
        """الانتقال إلى المجلد الأب"""
        parent_dir = os.path.dirname(self.current_dir)
        self.load_directory(parent_dir)

    def refresh_directory(self):
        """إعادة تحميل المجلد الحالي"""
        self.load_directory(self.current_dir)

    def show_context_menu(self, event):
        """عرض قائمة السياق"""
        # تحديد العنصر تحت المؤشر
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

    def copy_file(self):
        """نسخ الملف المحدد"""
        selected_items = self.tree.selection()
        if not selected_items:
            return
            
        selected_item = selected_items[0]
        item_data = self.tree.item(selected_item, "values")
        item_name = item_data[0].split(" ", 1)[1]  # إزالة الأيقونة من الاسم
        
        self.copied_file = os.path.join(self.current_dir, item_name)
        messagebox.showinfo("نسخ", f"تم نسخ: {item_name}")

    def paste_file(self):
        """لصق الملف المنسوخ"""
        if not self.copied_file or not os.path.exists(self.copied_file):
            messagebox.showwarning("تحذير", "لا يوجد ملف منسوخ أو الملف لم يعد موجودًا")
            return
            
        file_name = os.path.basename(self.copied_file)
        destination = os.path.join(self.current_dir, file_name)
        
        # التحقق من وجود الملف بنفس الاسم
        if os.path.exists(destination):
            response = messagebox.askyesno(
                "تأكيد", 
                f"الملف {file_name} موجود بالفعل. هل تريد استبداله؟"
            )
            if not response:
                return
                
        try:
            if os.path.isdir(self.copied_file):
                # نسخ المجلد مع محتوياته
                shutil.copytree(self.copied_file, destination, dirs_exist_ok=True)
            else:
                # نسخ الملف
                shutil.copy2(self.copied_file, destination)
                
            self.load_directory(self.current_dir)
            messagebox.showinfo("لصق", f"تم لصق: {file_name}")
        except Exception as e:
            messagebox.showerror("خطأ", f"تعذر لصق الملف: {e}")

    def delete_file(self):
        """حذف الملف أو المجلد المحدد"""
        selected_items = self.tree.selection()
        if not selected_items:
            return
            
        selected_item = selected_items[0]
        item_data = self.tree.item(selected_item, "values")
        item_name = item_data[0].split(" ", 1)[1]  # إزالة الأيقونة من الاسم
        
        file_path = os.path.join(self.current_dir, item_name)
        
        # طلب تأكيد الحذف
        response = messagebox.askyesno(
            "تأكيد الحذف", 
            f"هل أنت متأكد من أنك تريد حذف '{item_name}'؟"
        )
        
        if response:
            try:
                if os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                else:
                    os.remove(file_path)
                    
                self.load_directory(self.current_dir)
                messagebox.showinfo("حذف", f"تم حذف: {item_name}")
            except Exception as e:
                messagebox.showerror("خطأ", f"تعذر حذف الملف: {e}")

    def rename_file(self):
        """إعادة تسمية الملف أو المجلد المحدد"""
        selected_items = self.tree.selection()
        if not selected_items:
            return
            
        selected_item = selected_items[0]
        item_data = self.tree.item(selected_item, "values")
        item_name = item_data[0].split(" ", 1)[1]  # إزالة الأيقونة من الاسم
        
        file_path = os.path.join(self.current_dir, item_name)
        
        # نافذة لإدخال الاسم الجديد
        rename_window = tk.Toplevel(self.explorer_window)
        rename_window.title("إعادة تسمية")
        rename_window.geometry("400x100")
        rename_window.resizable(False, False)
        rename_window.transient(self.explorer_window)
        rename_window.grab_set()
        
        tk.Label(rename_window, text="أدخل الاسم الجديد:").pack(pady=5)
        
        new_name_var = tk.StringVar(value=item_name)
        entry = tk.Entry(rename_window, textvariable=new_name_var, width=40)
        entry.pack(pady=5)
        entry.select_range(0, len(item_name))
        entry.focus_set()
        
        def do_rename():
            new_name = new_name_var.get()
            if not new_name:
                messagebox.showwarning("تحذير", "الاسم الجديد لا يمكن أن يكون فارغًا")
                return
                
            new_path = os.path.join(self.current_dir, new_name)
            
            if os.path.exists(new_path):
                messagebox.showwarning("تحذير", f"يوجد بالفعل ملف أو مجلد باسم '{new_name}'")
                return
                
            try:
                os.rename(file_path, new_path)
                self.load_directory(self.current_dir)
                rename_window.destroy()
            except Exception as e:
                messagebox.showerror("خطأ", f"تعذر إعادة التسمية: {e}")
        
        button_frame = tk.Frame(rename_window)
        button_frame.pack(pady=5)
        
        tk.Button(button_frame, text="إعادة تسمية", command=do_rename).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="إلغاء", command=rename_window.destroy).pack(side=tk.LEFT, padx=5)
        
    def create_new_folder(self):
        """إنشاء مجلد جديد"""
        # نافذة لإدخال اسم المجلد
        folder_window = tk.Toplevel(self.explorer_window)
        folder_window.title("إنشاء مجلد جديد")
        folder_window.geometry("400x100")
        folder_window.resizable(False, False)
        folder_window.transient(self.explorer_window)
        folder_window.grab_set()
        
        tk.Label(folder_window, text="أدخل اسم المجلد الجديد:").pack(pady=5)
        
        folder_name_var = tk.StringVar(value="مجلد جديد")
        entry = tk.Entry(folder_window, textvariable=folder_name_var, width=40)
        entry.pack(pady=5)
        entry.select_range(0, len("مجلد جديد"))
        entry.focus_set()
        
        def create_folder():
            folder_name = folder_name_var.get()
            if not folder_name:
                messagebox.showwarning("تحذير", "اسم المجلد لا يمكن أن يكون فارغًا")
                return
                
            folder_path = os.path.join(self.current_dir, folder_name)
            
            if os.path.exists(folder_path):
                messagebox.showwarning("تحذير", f"يوجد بالفعل مجلد باسم '{folder_name}'")
                return
                
            try:
                os.mkdir(folder_path)
                self.load_directory(self.current_dir)
                folder_window.destroy()
            except Exception as e:
                messagebox.showerror("خطأ", f"تعذر إنشاء المجلد: {e}")
        
        button_frame = tk.Frame(folder_window)
        button_frame.pack(pady=5)
        
        tk.Button(button_frame, text="إنشاء", command=create_folder).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="إلغاء", command=folder_window.destroy).pack(side=tk.LEFT, padx=5)
    
    def create_new_text_file(self):
        """إنشاء ملف نصي جديد"""
        # نافذة لإدخال اسم الملف
        file_window = tk.Toplevel(self.explorer_window)
        file_window.title("إنشاء ملف نصي جديد")
        file_window.geometry("400x100")
        file_window.resizable(False, False)
        file_window.transient(self.explorer_window)
        file_window.grab_set()
        
        tk.Label(file_window, text="أدخل اسم الملف الجديد:").pack(pady=5)
        
        file_name_var = tk.StringVar(value="ملف جديد.txt")
        entry = tk.Entry(file_window, textvariable=file_name_var, width=40)
        entry.pack(pady=5)
        entry.select_range(0, len("ملف جديد"))
        entry.focus_set()
        
        def create_file():
            file_name = file_name_var.get()
            if not file_name:
                messagebox.showwarning("تحذير", "اسم الملف لا يمكن أن يكون فارغًا")
                return
                
            # إضافة امتداد .txt إذا لم يكن موجوداً
            if not file_name.endswith('.txt'):
                file_name += '.txt'
                
            file_path = os.path.join(self.current_dir, file_name)
            
            if os.path.exists(file_path):
                messagebox.showwarning("تحذير", f"يوجد بالفعل ملف باسم '{file_name}'")
                return
                
            try:
                # إنشاء الملف فارغ
                with open(file_path, 'w', encoding='utf-8') as f:
                    pass
                    
                self.load_directory(self.current_dir)
                file_window.destroy()
                
                # فتح الملف في المحرر النصي
                self.open_text_editor(file_path)
            except Exception as e:
                messagebox.showerror("خطأ", f"تعذر إنشاء الملف: {e}")
        
        button_frame = tk.Frame(file_window)
        button_frame.pack(pady=5)
        
        tk.Button(button_frame, text="إنشاء", command=create_file).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="إلغاء", command=file_window.destroy).pack(side=tk.LEFT, padx=5)

    def open_image_viewer(self, file_path):
        """فتح عارض الصور"""
        image_window = tk.Toplevel(self.root)
        image_window.title(f"عارض الصور - {os.path.basename(file_path)}")
        image_window.geometry("800x600")
        image_window.minsize(400, 300)
        self.current_opened_windows.append(image_window)
        
        # الإطار الرئيسي
        main_frame = tk.Frame(image_window)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # شريط الأدوات
        toolbar = tk.Frame(main_frame, bg="#F0F0F0")
        toolbar.pack(fill=tk.X)
        
        zoom_label = tk.Label(toolbar, text="التكبير:")
        zoom_label.pack(side=tk.LEFT, padx=5, pady=5)
        
        zoom_scale = tk.Scale(toolbar, from_=10, to=200, orient=tk.HORIZONTAL, length=200)
        zoom_scale.set(100)
        zoom_scale.pack(side=tk.LEFT, padx=5, pady=5)
        
        # متغير لتخزين معلومات الصورة الأصلية
        self.original_image = Image.open(file_path)
        self.current_image = self.original_image.copy()
        
        # إطار الصورة مع شريط تمرير
        image_frame = tk.Frame(main_frame)
        image_frame.pack(fill=tk.BOTH, expand=True)
        
        h_scrollbar = tk.Scrollbar(image_frame, orient=tk.HORIZONTAL)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        v_scrollbar = tk.Scrollbar(image_frame)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # كانفاس لعرض الصورة
        canvas = tk.Canvas(
            image_frame, 
            xscrollcommand=h_scrollbar.set, 
            yscrollcommand=v_scrollbar.set
        )
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        h_scrollbar.config(command=canvas.xview)
        v_scrollbar.config(command=canvas.yview)
        
        # وظيفة لتحديث الصورة عند تغيير التكبير
        def update_image(val):
            zoom = int(zoom_scale.get())
            width = int(self.original_image.width * zoom / 100)
            height = int(self.original_image.height * zoom / 100)
            
            # إعادة تحجيم الصورة
            resized_image = self.original_image.resize((width, height), Image.Resampling.LANCZOS)
            self.current_image = resized_image
            
            # تحويل الصورة إلى صيغة مناسبة لـ tkinter
            photo = ImageTk.PhotoImage(resized_image)
            
            # عرض الصورة في الكانفاس
            canvas.delete("all")
            canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            canvas.image = photo  # الاحتفاظ بمرجع لمنع التخلص من الصورة
            
            # تحديث منطقة التمرير للصورة
            canvas.config(scrollregion=(0, 0, width, height))
            
            # تحديث عنوان النافذة بمعلومات الصورة
            image_window.title(f"عارض الصور - {os.path.basename(file_path)} - {width}x{height}")
        
        zoom_scale.config(command=update_image)
        update_image(100)  # عرض الصورة بالحجم الأصلي
        
        # إضافة شريط معلومات
        status_bar = tk.Label(
            image_window, 
            text=f"الحجم الأصلي: {self.original_image.width}x{self.original_image.height}",
            bd=1, relief=tk.SUNKEN, anchor=tk.W
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def open_text_editor(self, file_path=None):
        """فتح محرر النصوص"""
        editor_window = tk.Toplevel(self.root)
        editor_window.title("المحرر النصي")
        editor_window.geometry("800x600")
        editor_window.minsize(400, 300)
        self.current_opened_windows.append(editor_window)
        
        # متغير لتخزين مسار الملف الحالي
        current_file_path = tk.StringVar(value=file_path if file_path else "")
        
        # دالة تحديث العنوان
        def update_title():
            if current_file_path.get():
                editor_window.title(f"المحرر النصي - {os.path.basename(current_file_path.get())}")
            else:
                editor_window.title("المحرر النصي - ملف جديد")
                
        update_title()
        
        # شريط القوائم
        menu_bar = tk.Menu(editor_window)
        editor_window.config(menu=menu_bar)
        
        # قائمة الملف
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="ملف", menu=file_menu)
        
        # دوال قائمة الملف
        def new_file():
            if text_area.edit_modified():
                response = messagebox.askyesnocancel("تنبيه", "هل تريد حفظ التغييرات قبل فتح ملف جديد؟")
                if response is None:  # إلغاء
                    return
                if response:  # نعم
                    save_file()
                    
            text_area.delete(1.0, tk.END)
            current_file_path.set("")
            text_area.edit_modified(False)
            update_title()
            
        def open_file():
            if text_area.edit_modified():
                response = messagebox.askyesnocancel("تنبيه", "هل تريد حفظ التغييرات قبل فتح ملف آخر؟")
                if response is None:  # إلغاء
                    return
                if response:  # نعم
                    save_file()
                    
            file = filedialog.askopenfilename(
                filetypes=[
                    ("ملفات نصية", "*.txt"), 
                    ("ملفات بايثون", "*.py"),
                    ("ملفات HTML", "*.html"),
                    ("جميع الملفات", "*.*")
                ]
            )
            
            if file:
                try:
                    with open(file, "r", encoding="utf-8") as f:
                        text_area.delete(1.0, tk.END)
                        text_area.insert(1.0, f.read())
                        current_file_path.set(file)
                        text_area.edit_modified(False)
                        update_title()
                except Exception as e:
                    messagebox.showerror("خطأ", f"حدث خطأ أثناء قراءة الملف: {e}")
                    
        def save_file():
            if current_file_path.get():
                try:
                    with open(current_file_path.get(), "w", encoding="utf-8") as f:
                        f.write(text_area.get(1.0, tk.END))
                        text_area.edit_modified(False)
                except Exception as e:
                    messagebox.showerror("خطأ", f"حدث خطأ أثناء حفظ الملف: {e}")
            else:
                save_file_as()
                
        def save_file_as():
            file = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[
                    ("ملفات نصية", "*.txt"), 
                    ("ملفات بايثون", "*.py"),
                    ("ملفات HTML", "*.html"),
                    ("جميع الملفات", "*.*")
                ]
            )
            
            if file:
                current_file_path.set(file)
                save_file()
                update_title()
                
        # إضافة العناصر لقائمة الملف
        file_menu.add_command(label="جديد", command=new_file)
        file_menu.add_command(label="فتح", command=open_file)
        file_menu.add_command(label="حفظ", command=save_file)
        file_menu.add_command(label="حفظ باسم", command=save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="خروج", command=lambda: self.close_window(editor_window))
        
        # قائمة التحرير
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="تحرير", menu=edit_menu)
        
        # دوال قائمة التحرير
        def cut():
            editor_window.focus_get().event_generate("<<Cut>>")
            
        def copy():
            editor_window.focus_get().event_generate("<<Copy>>")
            
        def paste():
            editor_window.focus_get().event_generate("<<Paste>>")
            
        def select_all():
            text_area.tag_add(tk.SEL, "1.0", tk.END)
            text_area.mark_set(tk.INSERT, "1.0")
            text_area.see(tk.INSERT)
            
        # إضافة العناصر لقائمة التحرير
        edit_menu.add_command(label="قص", command=cut)
        edit_menu.add_command(label="نسخ", command=copy)
        edit_menu.add_command(label="لصق", command=paste)
        edit_menu.add_separator()
        edit_menu.add_command(label="تحديد الكل", command=select_all)
        
        # شريط الأدوات
        toolbar = tk.Frame(editor_window, bg="#F0F0F0")
        toolbar.pack(fill=tk.X)
        
        # أزرار شريط الأدوات
        tk.Button(toolbar, text="جديد", command=new_file).pack(side=tk.LEFT, padx=2, pady=2)
        tk.Button(toolbar, text="فتح", command=open_file).pack(side=tk.LEFT, padx=2, pady=2)
        tk.Button(toolbar, text="حفظ", command=save_file).pack(side=tk.LEFT, padx=2, pady=2)
        
        # إطار النص
        text_frame = tk.Frame(editor_window)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        # شريط رقم السطر
        line_numbers = tk.Text(text_frame, width=4, padx=4, pady=4, takefocus=0, 
                            bg='#F0F0F0', relief=tk.RIDGE, state='disabled')
        line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        
        # منطقة النص مع شريط تمرير
        text_area = scrolledtext.ScrolledText(
            text_frame, wrap=tk.WORD, font=("Courier New", 12),
            undo=True, maxundo=-1
        )
        text_area.pack(fill=tk.BOTH, expand=True)
        
        # دالة تحديث أرقام الأسطر
        def update_line_numbers(event=None):
            line_numbers.config(state='normal')
            line_numbers.delete(1.0, tk.END)
            
            # عد الأسطر في منطقة النص
            num_lines = text_area.get(1.0, tk.END).count('\n')
            line_text = ''
            for i in range(1, num_lines + 1):
                line_text += f"{i}\n"
                
            line_numbers.insert(1.0, line_text)
            line_numbers.config(state='disabled')
        
        # ربط تحديث أرقام الأسطر بالتمرير والتغيير
        text_area.bind("<KeyPress>", update_line_numbers)
        text_area.bind("<KeyRelease>", update_line_numbers)
        text_area.bind("<MouseWheel>", update_line_numbers)
        
        # شريط الحالة
        status_bar = tk.Label(editor_window, anchor=tk.W, bd=1, relief=tk.SUNKEN)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # تحديث شريط الحالة
        def update_status(event=None):
            cursor_position = text_area.index(tk.INSERT)
            line, column = cursor_position.split('.')
            
            char_count = len(text_area.get(1.0, tk.END)) - 1  # -1 للمحرف الأخير
            status_text = f"السطر: {line} | العمود: {column} | عدد الأحرف: {char_count}"
            
            if text_area.edit_modified():
                status_text += " | [غير محفوظ]"
                
            status_bar.config(text=status_text)
            
        # ربط تحديث الحالة بأحداث المحرر
        text_area.bind("<KeyPress>", update_status)
        text_area.bind("<KeyRelease>", update_status)
        text_area.bind("<ButtonRelease-1>", update_status)
        
        # فتح الملف إذا تم تحديده
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    text_area.delete(1.0, tk.END)
                    text_area.insert(1.0, f.read())
                    text_area.edit_modified(False)
            except Exception as e:
                messagebox.showerror("خطأ", f"حدث خطأ أثناء قراءة الملف: {e}")
                
        # التهيئة الأولية
        update_line_numbers()
        update_status()
        
        # تسجيل وظيفة الإغلاق
        editor_window.protocol("WM_DELETE_WINDOW", lambda: self.close_window(editor_window))

    def show_about(self):
        """عرض معلومات حول النظام"""
        about_window = tk.Toplevel(self.root)
        about_window.title("حول ZU Operating System")
        about_window.geometry("400x300")
        about_window.resizable(False, False)
        
        # شعار النظام
        tk.Label(about_window, text="ZU OS", font=("Arial", 24, "bold")).pack(pady=10)
        
        # معلومات النظام
        info_frame = tk.Frame(about_window)
        info_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        system_info = f"""
        نظام ZU التشغيلي - نسخة 1.0
        
        نظام تشغيل محاكي مبني على Python و Tkinter
        
        معلومات النظام:
        - نظام التشغيل: {platform.system()}
        - إصدار النظام: {platform.version()}
        - المنصة: {platform.platform()}
        - المعالج: {platform.processor()}
        """
        
        tk.Label(info_frame, text=system_info, justify=tk.LEFT).pack()
        
        # زر الإغلاق
        tk.Button(
            about_window, text="إغلاق", 
            command=about_window.destroy
        ).pack(pady=10)

    def shutdown(self):
        """إيقاف تشغيل النظام"""
        response = messagebox.askyesno(
            "إيقاف التشغيل",
            "هل أنت متأكد أنك تريد إيقاف تشغيل النظام؟"
        )
        
        if response:
            self.root.destroy()

    def close_window(self, window):
        """إغلاق نافذة مع إزالتها من قائمة النوافذ المفتوحة"""
        if window in self.current_opened_windows:
            self.current_opened_windows.remove(window)
        window.destroy()


# تشغيل النظام
if __name__ == "__main__":
    root = tk.Tk()
    zu_os = ZUOperatingSystem(root)
    root.mainloop()