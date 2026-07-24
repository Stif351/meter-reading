
from tkinter import SUNKEN, W, S
import tkinter as tk
import PyPDF2
import os
from tkinter import ttk, messagebox, filedialog, font
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from io import BytesIO
from send2trash import send2trash
from pathlib import Path

class MyExtraWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)


        pdfmetrics.registerFont(TTFont("DejaVuSans", "DejaVuSans.ttf"))
        self.ft = 'DejaVuSans'



        self.title("Це окреме вікно")
        self.geometry("900x800+500+50")
        self.configure(bg="#2c3e50")

        self.courier_10 = font.Font(family="Courier", size=10, weight=font.BOLD)
        self.courier_14 = font.Font(family="Courier", size=14, weight=font.BOLD)
        self.courier_18 = font.Font(family="Courier", size=18, weight=font.BOLD)
        self.width_frame = 800

        self.report_options = [" ", "Січень", "Лютий", "Березень", "Квітень", "Травень", "Червень", "Липень", "Серпень",
                      "Вересень",
                      "Жовтень", "Листопад", "Грудень"]

        self.report_options_year = [" ", "2025", "2026", "2027", "2028", "2029", "2030", "2031", "2034", "2035", "2036", "2037",
                           "2038"]

        self.size_list = 7
        self.results = [0] * 7

        self.setup_ui()



    def selected(self, event,):

        widget = event.widget
        tag = getattr(widget, "tag", None)
        value = widget.get()
        index = self.report_menu.current()
        if tag == "month":
            # self.label_report(self.lf2, value)
            self.label_report(self.lf2, 2, 2, value)
            self.results[0] = value
            self.results[1] = index
            self.report_menu_year.config(state='normal')
            self.report_menu.config(state='disable')
        if tag == "year":
            # self.label_report(self.lf2, value)
            self.label_report(self.lf2, 3, 2, value)
            self.results[2] = value
            self.dialog_btn_8.config(state='normal')
            self.report_menu_year.config(state='disable')

    def browse_directory(self, a, b, c, i, btn1, btn2):

        self.new_folder_path = filedialog.askdirectory(initialdir=r"D:\комуналка", title="Dialog box")
        self.results[i] = self.new_folder_path

        # self.label_report(self, new_folder_path)
        self.label_report( a, b, c, self.new_folder_path)

        btn2.config(state='normal')
        btn1.config(state='disable')

    def label_report(self, frame, row, column, value):

        report_label = ttk.Label(frame, text=value, font=self.courier_14, foreground='green')
        report_label.grid(row=row, column=column, ipadx=6, ipady=6, padx=55, pady=5)

    def report_end(self, value):

        messagebox.showinfo('Інформація', f'{value}', parent=self)

    def join_file(self):

        # Створюємо об'єкт PdfMerger з бібліотеки PyPDF2
        pdf_merger = PyPDF2.PdfMerger()
        for filename in os.listdir(self.results[3]):
            if filename.endswith(".pdf"):
                full_path = os.path.join(self.results[3], filename)
                pdf_merger.append(full_path)

        # Зберігаємо результат у новий PDF-файл
        output_filename = f"{self.results[5]}/{self.results[0]}-26.pdf"

        with open(output_filename, 'wb') as output_file:
            pdf_merger.write(output_file)

        # Закриваємо об'єкт PdfMerger для звільнення ресурсів
        pdf_merger.close()

        self.add_header(output_filename, output_filename, f'{self.results[0]}-2026', self.lf5, 8)
        self.join_file_kv()

    def join_file_kv(self):

        pdf_merger = PyPDF2.PdfMerger()
        for filename in os.listdir(self.results[4]):
            if filename.endswith(".pdf"):
                full_path = os.path.join(self.results[4], filename)
                pdf_merger.append(full_path)

        # Зберігаємо результат у новий PDF-файл
        output_filename2 = f"{self.results[6]}/Квітнева_30-5_{self.results[1]}-26.pdf"

        with open(output_filename2, 'wb') as output_file:
            pdf_merger.write(output_file)
        # Закриваємо об'єкт PdfMerger для звільнення ресурсів
        pdf_merger.close()

        self.add_header(output_filename2, output_filename2, f'{self.results[0]}-2026', self.lf5, 9)
        self.save_file()

    def save_file(self):

        messagebox.showinfo("Інформація", "Файли оплати успішно створенні.", parent=self)

    def confirm_exit(self):

        try:
            self.remove_files()
            self.destroy()
        except TypeError:
            messagebox.showinfo("Інформація", "Файли відсутні. Додаток буде закрито.", parent=self)
        finally:
            self.destroy()

    def add_header(self, input_pdf, output_pdf, header_text, fr, rw):
        reader = PdfReader(input_pdf)
        writer = PdfWriter()

        for page in reader.pages:
            packet = BytesIO()
            can = canvas.Canvas(packet, pagesize=A4)
            width, height = A4

            # Верхній колонтитул
            can.setFillColorRGB(255, 0, 0)
            can.setFont(self.ft, 32)
            can.drawString(150, height - 45, header_text)
            can.save()

            packet.seek(0)
            overlay = PdfReader(packet)
            page.merge_page(overlay.pages[0])
            writer.add_page(page)

        with open(output_pdf, "wb") as f:
            writer.write(f)

        path_s = f'Файл збережено. Шлях до файлу: {output_pdf}'
        path_save_label1 = ttk.Label(fr, text=path_s, font=self.courier_10, foreground='green')
        path_save_label1.grid(row=rw, column=0, ipadx=6, ipady=6, padx=5, pady=5)


    def remove_files(self):
        response = messagebox.askyesno("Видалення файлу", "Ви впевнені, що хочете вийти і видалити файли?",
                                       parent=self)
        pathK8 = Path(self.results[3])
        pathK30 = Path(self.results[4])
        folders = [
            pathK8,
            pathK30
        ]

        if response:
            for folder in folders:
                 for pdf in folder.glob("*.pdf"):
                    send2trash(pdf)

    #  ----------- MAIN WINDOWS -------------------------

    def setup_ui(self):

        label = tk.Label(self, text="ЄДИНА КВИТАНЦІЯ ПРО ОПЛАТУ КОМУНАЛЬНИХ ПОСЛУГ", fg="BLUE", font=self.courier_18)
        label.grid(row=0, column=0, columnspan=3, ipadx=6, ipady=6, padx=5, pady=15)

        lf3 = ttk.Frame(self, borderwidth=10, relief=SUNKEN)
        lf3.config(width=850, height=670)
        lf3.grid_propagate(False)

        lf3.grid(column=0, row=1, ipadx=6, ipady=6, padx=20, pady=20)

        # =====================  Додаємо  місяць  =========================================
        self.lf2 = ttk.Frame(lf3, borderwidth=10, relief=SUNKEN)
        self.lf2.config(width=self.width_frame, height=130)
        self.lf2.grid_propagate(False)

        label_month = tk.Label(self.lf2, text="Виберіть місяць: ", font=self.courier_14)
        label_month.grid(row=2, column=0, ipadx=6, ipady=6, padx=5, pady=5)

        self.selected_report = tk.StringVar(value=self.report_options[0])
        self.report_menu = ttk.Combobox(self.lf2, textvariable=self.selected_report, values=self.report_options)
        self.report_menu.tag = "month"
        self.report_menu.grid(row=2, column=1, ipadx=6, ipady=6, padx=5, pady=5)
        self.report_menu.bind("<<ComboboxSelected>>", self.selected)

        # =================== Додаємо рік  =======================================================

        label_year = tk.Label(self.lf2, text="Виберіть рік: ", font=self.courier_14)
        label_year.grid(row=3, column=0, ipadx=6, ipady=6, padx=5, pady=5)

        self.selected_report_year = tk.StringVar(value=self.report_options[0])
        self.report_menu_year = ttk.Combobox(self.lf2, textvariable=self.selected_report_year, values=self.report_options_year, state='disable')
        self.report_menu_year.tag = "year"
        self.report_menu_year.grid(row=3, column=1, ipadx=6, ipady=6, padx=5, pady=5)
        self.report_menu_year.bind("<<ComboboxSelected>>", self.selected)

        self.lf2.grid(column=0, row=0, padx=20, pady=10, sticky=W)
        # ========================= Обираємо шлях розтушування файлів  ====================================
        self.lf1 = ttk.Frame(lf3, borderwidth=10, relief=SUNKEN)
        self.lf1.config(width=self.width_frame, height=130)
        self.lf1.grid_propagate(False)

        self.label_path = tk.Label(self.lf1, text="оберіть шлях \n розтушування \n файлів", justify="center", font=self.courier_14)
        self.label_path.grid(row=4, column=0, rowspan=2, ipadx=6, ipady=6, padx=5, pady=5)
        self.dialog_btn_8 = tk.Button(self.lf1, text="КВІТНЕВА-8", font=self.courier_10, width=12, state='disable',
                                 command=lambda: self.browse_directory(self.lf1, 4, 2, 3, self.dialog_btn_8, self.dialog_btn_30))
        self.dialog_btn_8.grid(row=4, column=1, ipadx=6, ipady=6, padx=5, pady=5)
        self.dialog_btn_30 = tk.Button(self.lf1, text="КВІТНЕВА-30-5", font=self.courier_10, width=12, state='disable',
                                  command=lambda: self.browse_directory(self.lf1, 5, 2, 4, self.dialog_btn_30, self.dialog_add_btn_8))
        self.dialog_btn_30.grid(row=5, column=1, ipadx=6, ipady=6, padx=5, pady=5)

        self.lf1.grid(column=0, row=5, padx=20, pady=10, sticky=W)

        # ========================= Обираємо шлях збереження файлів  ====================================

        self.lf4 = ttk.Frame(lf3, borderwidth=10, relief=SUNKEN)
        self.lf4.config(width=self.width_frame, height=130)
        self.lf4.grid_propagate(False)

        self.label_path_add = tk.Label(self.lf4, text="оберіть шлях \n зберігання \n файлів  ", font=self.courier_14, justify='center')
        self.label_path_add.grid(row=4, column=0, rowspan=2, ipadx=6, ipady=6, padx=5, pady=5)
        self.dialog_add_btn_8 = tk.Button(self.lf4, text="КВІТНЕВА-8", font=self.courier_10, width=12, state='disable',
                                     command=lambda: self.browse_directory(self.lf4, 4, 2, 5, self.dialog_add_btn_8, self.dialog_add_btn_30))
        self.dialog_add_btn_8.grid(row=4, column=1, ipadx=6, ipady=6, padx=5, pady=5)
        self.dialog_add_btn_30 = tk.Button(self.lf4, text="КВІТНЕВА-30-5", font=self.courier_10, width=12, state='disable',
                                      command=lambda: self.browse_directory(self.lf4, 5, 2, 6, self.dialog_add_btn_30, self.save_btn))
        self.dialog_add_btn_30.grid(row=5, column=1, ipadx=6, ipady=6, padx=5, pady=5)

        self.lf4.grid(column=0, row=6, padx=20, pady=10, sticky=W)

        # =======================INFO TABLE =========================================

        self.lf5 = ttk.Frame(lf3, borderwidth=10, relief=SUNKEN)
        self.lf5.config(width=self.width_frame, height=100)
        self.lf5.grid_propagate(False)

        self.lf5.grid(column=0, row=7, padx=20, pady=10, sticky=S)

        # =========================== Кнопка зберегти файли  ============================
        self.lf = ttk.Frame(lf3, borderwidth=10, relief=SUNKEN)
        self.lf.config(width=self.width_frame, height=80)
        self.lf.grid_propagate(False)

        self.save_btn = tk.Button(self.lf, text="ЗБЕРЕГТИ ФАЙЛИ", font=self.courier_10, state='disable', command=self.join_file)
        self.save_btn.grid(row=6, column=0, ipadx=6, ipady=6, padx=50, pady=10)

        # =========================== Кнопка EXIT  ============================

        self.exit_btn = tk.Button(self.lf, text="ЗАВЕРШИТИ", font=self.courier_10, foreground='red', command=self.confirm_exit)
        self.exit_btn.grid(row=6, column=2, ipadx=6, ipady=6, padx=400, pady=10)

        self.lf.grid(column=0, row=8, padx=20, pady=10, sticky=S)

        # ================= END ===================================================



