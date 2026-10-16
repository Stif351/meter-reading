from tkinter import SUNKEN, W, S
import tkinter as tk
from tkinter.constants import SOLID
import os
from tkinter import ttk, messagebox, filedialog, font
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from io import BytesIO
from send2trash import send2trash
from pathlib import Path
from datetime import datetime


def print_check(root):

        pdfmetrics.registerFont(TTFont("DejaVuSans", "DejaVuSans.ttf"))
        ft = 'DejaVuSans'

        report_options = [" ", "Січень", "Лютий", "Березень", "Квітень", "Травень", "Червень", "Липень", "Серпень", "Вересень", "Жовтень", "Листопад", "Грудень"]

        current_year = datetime.now().year
        report_options_year = [" "] + [str(y) for y in range(current_year - 1, current_year + 5)]

        results = {
            "month_name": "",
            "month_idx": 0,
            "year": "",
            "src_k8": "",
            "src_k30": "",
            "dst_k8": "",
            "dst_k30": ""
        }

        def selected(event):

            widget = event.widget
            tag = getattr(widget, "tag", None)
            value = widget.get()
            # index = report_menu.current()
            if tag == "month":
                label_report(lf2, 2, 2, value)
                results["month_name"] = value
                results["month_idx"]= report_menu.current()
                report_menu_year.config(state='normal')
                report_menu.config(state='disable')
            if tag == "year":
                label_report(lf2, 3, 2, value)
                results["year"] =  value
                dialog_btn_8.config(state='normal')
                report_menu_year.config(state='disable')

        def browse_directory(parent_frame, row, col, key, curr_btn, next_btn):

            init_dir = r" " if os.path.exists(r" ") else os.path.expanduser("~")   # Резервний вибір папки, якщо hardcoded шлях відсутній
            new_path = filedialog.askdirectory(initialdir=init_dir, title="Оберіть папку", parent=about_win)

            if not new_path:
                return              # Якщо користувач скасував вибір

            results[key] = new_path
            label_report(parent_frame, row, col, new_path)

            if next_btn:
                next_btn.config(state='normal')
            curr_btn.config(state='disabled')


        def label_report(frame, row, column, value):

            report_label = ttk.Label(frame, text=value, font=courier_14, foreground='green')
            report_label.grid(row=row, column=column, ipadx=6, ipady=6, padx=55, pady=5)

    # =====================  Універсальна функція об'єднання всіх PDF-файлів у папці. ===================================

        def merge_pdf_folder(src_folder, output_filepath):

            merger = PdfMerger()
            pdf_files = sorted(Path(src_folder).glob("*.pdf"))

            if not pdf_files:
                merger.close()
                raise FileNotFoundError(f"У папці {src_folder} не знайдено PDF-файлів.")

            for pdf_path in pdf_files:
                merger.append(str(pdf_path))

            with open(output_filepath, 'wb') as output_file:
                merger.write(output_file)
            merger.close()
        
        def join_file():
            year = results["year"]
            month_name = results["month_name"]
            month_idx = results["month_idx"]

            try:

                out_k8 = os.path.join(results["dst_k8"], f"{month_name}-{year[-2:]}.pdf")  # 1. Обробка файлів Квітнева-8
                merge_pdf_folder(results["src_k8"], out_k8)
                add_header(out_k8, out_k8, f'{month_name}-{year}', lf5, 8, 0)


                out_k30 = os.path.join(results["dst_k30"], f"Квітнева_30-5_{month_idx}-{year[-2:]}.pdf")     # 2. Обробка файлів Квітнева-30-5
                merge_pdf_folder(results["src_k30"], out_k30)
                add_header(out_k30, out_k30, f'{month_name}-{year}', lf5, 8, 1)

                messagebox.showinfo("Інформація", "Файли оплати успішно створені.", parent=about_win)

            except Exception as e:
                messagebox.showerror("Помилка", f"Виникла помилка під час обробки: {e}", parent=about_win)


        def confirm_exit():

            try:
                remove_files()
                about_win.destroy()
            except TypeError:
                messagebox.showinfo("Інформація", "Файли відсутні. Додаток буде закрито.", parent=about_win)
            finally:
                about_win.destroy()


        def add_header(input_pdf, output_pdf, header_text, fr, row, column):
            reader = PdfReader(input_pdf)
            writer = PdfWriter()

            for page in reader.pages:
                packet = BytesIO()
                can = canvas.Canvas(packet, pagesize=A4)
                width, height = A4

                # Верхній колонтитул
                can.setFillColorRGB(255, 0, 0)
                can.setFont(ft, 32)
                can.drawString(150, height - 45, header_text)
                can.save()

                packet.seek(0)
                overlay = PdfReader(packet)
                page.merge_page(overlay.pages[0])
                writer.add_page(page)

            with open(output_pdf, "wb") as f:
                writer.write(f)

            path_s = f'Файл збережено.\nШлях до файлу: \n{output_pdf}'
            path_save_label1 = ttk.Label(fr, text=path_s, font=courier_10, foreground='green')
            path_save_label1.grid(row=row, column=column, ipadx=6, ipady=6, padx=5, pady=5)


        def remove_files():
            messagebox.askyesno("Видалення файлу", "Ви впевнені, що хочете вийти і видалити файли?", parent=about_win)
            for key in ["src_k8", "src_k30"]:
                folder_path = results.get(key)
                if folder_path and os.path.exists(folder_path):
                    for pdf_file in Path(folder_path).glob("*.pdf"):
                        try:
                            send2trash(pdf_file)
                        except Exception as e:
                            messagebox.showerror("Помилка", f"Виникла помилка під час обробки: {e}", parent=about_win)




#  ----------- MAIN WINDOWS -------------------------

        about_win = tk.Toplevel(root)
        about_win.title("Внесення показників")

        window_width, window_height = 900, 800
        screen_width = about_win.winfo_screenwidth()
        screen_height = about_win.winfo_screenheight()
        center_x = int((screen_width / 2) - (window_width / 2))
        center_y = int((screen_height / 2) - (window_height / 2))

        about_win.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        about_win.configure(bg="#2c3e50")  # Власний колір фону

        courier_10 = font.Font(family="Courier", size=10, weight="bold")
        courier_14 = font.Font(family="Courier", size=14, weight="bold")
        courier_18 = font.Font(family="Courier", size=18, weight="bold")
        width_frame = 800

        label = tk.Label(about_win, text="ЄДИНА КВИТАНЦІЯ ПРО ОПЛАТУ КОМУНАЛЬНИХ ПОСЛУГ", fg="BLUE", font=courier_18)
        label.grid(row=0, column=0, columnspan=3, ipadx=6, ipady=6, padx=5, pady=15)

        lf3 = ttk.Frame(about_win, borderwidth=10, relief=SUNKEN)
        lf3.config(width=850, height=650)
        lf3.grid_propagate(False)

        # =====================  Додаємо  місяць  =========================================

        lf2 = ttk.Frame(lf3, borderwidth=10, relief=SUNKEN)
        lf2.config(width=width_frame, height=130)
        lf2.grid_propagate(False)

        label_month = tk.Label(lf2, text="Виберіть місяць: ", font=courier_14, foreground='black')
        label_month.grid(row=2, column=0, ipadx=6, ipady=6, padx=5, pady=5, sticky=W)

        selected_report = tk.StringVar(value=report_options[0])
        report_menu = ttk.Combobox(lf2, textvariable=selected_report, values=report_options)
        report_menu.tag = "month"
        report_menu.grid(row=2, column=1, ipadx=6, ipady=6, padx=5, pady=5)
        report_menu.bind("<<ComboboxSelected>>", selected)

        # =================== Додаємо рік  =======================================================

        label_year = tk.Label(lf2, text="Виберіть рік: ", font=courier_14, foreground='black')
        label_year.grid(row=3, column=0, ipadx=6, ipady=6, padx=5, pady=5, sticky=W)

        selected_report_year = tk.StringVar(value=report_options[0])
        report_menu_year = ttk.Combobox(lf2, textvariable=selected_report_year, values=report_options_year, state='disable')
        report_menu_year.tag = "year"
        report_menu_year.grid(row=3, column=1, ipadx=6, ipady=6, padx=5, pady=5)
        report_menu_year.bind("<<ComboboxSelected>>", selected)

        lf2.grid(column=0, row=0, padx=20, pady=10, sticky=W)
        # ========================= Обираємо шлях розтушування файлів  ====================================
        lf1 = ttk.Frame(lf3, borderwidth=10, relief=SUNKEN)
        lf1.config(width=width_frame, height=130)
        lf1.grid_propagate(False)

        label_path = tk.Label(lf1, text="оберіть шлях \n розтушування \n файлів", justify="center", font=courier_14,
                              foreground='black')
        label_path.grid(row=4, column=0, rowspan=2, ipadx=6, ipady=6, padx=5, pady=5, sticky=W)
        dialog_btn_8 = tk.Button(lf1, text="КВІТНЕВА-8", font=courier_10, width=12, state='disable',
                                 command=lambda: browse_directory( lf1, 4, 2, "src_k8", dialog_btn_8, dialog_btn_30))
        dialog_btn_8.grid(row=4, column=1, ipadx=6, ipady=6, padx=5, pady=5)
        dialog_btn_30 = tk.Button(lf1, text="КВІТНЕВА-30-5", font=courier_10, width=12, state='disable',
                                  command=lambda: browse_directory(lf1, 5, 2, "src_k30", dialog_btn_30, dialog_add_btn_8))
        dialog_btn_30.grid(row=5, column=1, ipadx=6, ipady=6, padx=5, pady=5)

        lf1.grid(column=0, row=5, padx=20, pady=10, sticky=W)

        # ========================= Обираємо шлях збереження файлів  ====================================

        lf4 = ttk.Frame(lf3, borderwidth=10, relief=SUNKEN)
        lf4.config(width=width_frame, height=130)
        lf4.grid_propagate(False)

        label_path_add = tk.Label(lf4, text="оберіть шлях \n зберігання \n файлів  ", font=courier_14, justify='center',
                                  foreground='black')
        label_path_add.grid(row=4, column=0, rowspan=2, ipadx=6, ipady=6, padx=5, pady=5)
        dialog_add_btn_8 = tk.Button(lf4, text="КВІТНЕВА-8", font=courier_10, width=12, state='disable',
                                     command=lambda: browse_directory( lf4, 4, 2, "dst_k8", dialog_add_btn_8, dialog_add_btn_30))
        dialog_add_btn_8.grid(row=4, column=1, ipadx=6, ipady=6, padx=5, pady=5)
        dialog_add_btn_30 = tk.Button(lf4, text="КВІТНЕВА-30-5", font=courier_10, width=12, state='disable',
                                      command=lambda: browse_directory( lf4, 5, 2, "dst_k30", dialog_add_btn_30, save_btn))
        dialog_add_btn_30.grid(row=5, column=1, ipadx=6, ipady=6, padx=5, pady=5)

        lf4.grid(column=0, row=6, padx=20, pady=10, sticky=W)

        # =======================INFO TABLE =========================================

        lf5 = ttk.Frame(lf3, borderwidth=10, relief=SUNKEN)
        lf5.config(width=width_frame, height=75)
        lf5.grid_propagate(False)

        lf5.grid(column=0, row=7, padx=20, pady=10, sticky=S)

        # =========================== Кнопка зберегти файли  ============================
        lf = ttk.Frame(lf3, borderwidth=10, relief=SUNKEN)
        lf.config(width=width_frame, height=80)
        lf.grid_propagate(False)

        save_btn = tk.Button(lf, text="ЗБЕРЕГТИ ФАЙЛИ", font=courier_10, foreground='green', state='disable', command=join_file)
        save_btn.grid(row=6, column=0, ipadx=6, ipady=6, padx=50, pady=10)

        # =========================== Кнопка EXIT  ============================

        exit_btn = tk.Button(lf, text="ЗАВЕРШИТИ", font=courier_10, foreground='red', relief=SOLID, command=confirm_exit)
        exit_btn.grid(row=6, column=2, ipadx=6, ipady=6, padx=400, pady=10)

        lf.grid(column=0, row=8, padx=20, pady=10, sticky=S)

        # ================= END ===================================================

        lf3.grid(column=0, row=1, ipadx=6, ipady=6, padx=20, pady=20)

        about_win.grab_set()
