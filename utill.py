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
#from send2trash import send2trash
from pathlib import Path


def print_check(root):


        pdfmetrics.registerFont(TTFont("DejaVuSans", "DejaVuSans.ttf"))
        ft = 'DejaVuSans'
        report_options = [" ", "Січень", "Лютий", "Березень", "Квітень", "Травень", "Червень", "Липень", "Серпень", "Вересень",
                          "Жовтень", "Листопад", "Грудень"]

        report_options_year = [" ", "2025", "2026", "2027", "2028", "2029", "2030", "2031", "2034", "2035", "2036", "2037",
                               "2038"]

        size_list = 7
        results = [0]*7


        def selected(event):

            widget = event.widget
            tag = getattr(widget, "tag", None)
            value = widget.get()
            index = report_menu.current()
            if tag == "month":
                label_report(lf2, 2, 2, value)
                results[0] = value
                results[1]= index
                report_menu_year.config(state='normal')
                report_menu.config(state='disable')
            if tag == "year":
                label_report(lf2, 3, 2, value)
                results[2] =  value
                dialog_btn_8.config(state='normal')
                report_menu_year.config(state='disable')


        def browse_directory(a, b, c, i, btn1, btn2):

            new_folder_path = filedialog.askdirectory(initialdir=r"D:\комуналка", title="Dialog box")
            results[i] =  new_folder_path

            label_report(a, b, c, new_folder_path)

            btn2.config(state='normal')
            btn1.config(state='disable')


        def label_report(frame, row, column, value):

            report_label = ttk.Label(frame, text=value, font=courier_14, foreground='green')
            report_label.grid(row=row, column=column, ipadx=6, ipady=6, padx=55, pady=5)


        def join_file():

            # Створюємо об'єкт PdfMerger з бібліотеки PyPDF2
            pdf_merger = PyPDF2.PdfMerger()
            for filename in os.listdir(results[3]):
                if filename.endswith(".pdf"):
                    full_path = os.path.join(results[3], filename)
                    pdf_merger.append(full_path)

            # Зберігаємо результат у новий PDF-файл
            output_filename = f"{results[5]}/{results[0]}-26.pdf"

            with open(output_filename, 'wb') as output_file:
                pdf_merger.write(output_file)

            # Закриваємо об'єкт PdfMerger для звільнення ресурсів
            pdf_merger.close()

            add_header(output_filename, output_filename, f'{results[0]}-2026', lf5, 8)
            join_file_kv()

        def join_file_kv():

            pdf_merger = PyPDF2.PdfMerger()
            for filename in os.listdir(results[4]):
                if filename.endswith(".pdf"):
                    full_path = os.path.join(results[4], filename)
                    pdf_merger.append(full_path)

            # Зберігаємо результат у новий PDF-файл
            output_filename2 = f"{results[6]}/Квітнева_30-5_{results[1]}-26.pdf"

            with open(output_filename2, 'wb') as output_file:
                pdf_merger.write(output_file)
            # Закриваємо об'єкт PdfMerger для звільнення ресурсів
            pdf_merger.close()

            add_header(output_filename2, output_filename2, f'{results[0]}-2026', lf5, 9)
            save_file()


        def save_file():

            messagebox.showinfo("Інформація", "Файли оплати успішно створенні.", parent=about_win)


        def confirm_exit():

            try:
                remove_files()
                about_win.destroy()
            except TypeError:
                messagebox.showinfo("Інформація", "Файли відсутні. Додаток буде закрито.", parent=about_win)
            finally:
                about_win.destroy()





        def add_header(input_pdf, output_pdf, header_text, fr, rw):
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

            path_s = f'Файл збережено.\n Шлях до файлу: {output_pdf}'
            path_save_label1 = ttk.Label(fr, text=path_s, font=courier_10, foreground='green')
            path_save_label1.grid(row=rw, column=0, ipadx=6, ipady=6, padx=5, pady=5)
            # print(path_s)
            # path_save_label1.config(text=path_s)
            # path_save_label2.config(text=path_s)

        def remove_files():

            pass

            # response = messagebox.askyesno("Видалення файлу", "Ви впевнені, що хочете вийти і видалити файли?",
            #                                parent=about_win)
            # pathK8 = Path(results[3])
            # pathK30 = Path(results[4])
            # folders =[
            #     pathK8,
            #     pathK30
            # ]
            #
            # if response:
            #     for folder in folders:
            #         for pdf in folder.glob("*.pdf"):
            #             send2trash(pdf)




        #  ----------- MAIN WINDOWS -------------------------

        # root = tk.Tk()
        # root.title("MAIN WINDOW")
        # root.geometry("900x1000")
        # root.resizable(False, False)
        # root.iconbitmap('smart.ico')

        about_win = tk.Toplevel(root)
        about_win.title("Внесення показників")
        about_win.geometry("900x800")
        about_win.configure(bg="#2c3e50")  # Власний колір фону

        courier_10 = font.Font(family="Courier", size=10, weight=font.BOLD)
        courier_14 = font.Font(family="Courier", size=14, weight=font.BOLD)
        courier_18 = font.Font(family="Courier", size=18, weight=font.BOLD)
        width_frame = 800

        label = tk.Label(about_win, text="ЄДИНА КВИТАНЦІЯ ПРО ОПЛАТУ КОМУНАЛЬНИХ ПОСЛУГ", fg="BLACK", font=courier_18)
        label.grid(row=0, column=0, columnspan=3, ipadx=6, ipady=6, padx=5, pady=15)

        lf3 = ttk.Frame(about_win, borderwidth=10, relief=SUNKEN)
        lf3.config(width=850, height=900)
        lf3.grid_propagate(False)

        # =====================  Додаємо  місяць  =========================================
        lf2 = ttk.Frame(lf3, borderwidth=10, relief=SUNKEN)
        lf2.config(width=width_frame, height=130)
        lf2.grid_propagate(False)

        label_month = tk.Label(lf2, text="Виберіть місяць: ", font=courier_14, foreground='red')
        label_month.grid(row=2, column=0, ipadx=6, ipady=6, padx=5, pady=5)

        selected_report = tk.StringVar(value=report_options[0])
        report_menu = ttk.Combobox(lf2, textvariable=selected_report, values=report_options)
        report_menu.tag = "month"
        report_menu.grid(row=2, column=1, ipadx=6, ipady=6, padx=5, pady=5)
        report_menu.bind("<<ComboboxSelected>>", selected)

        # =================== Додаємо рік  =======================================================

        label_year = tk.Label(lf2, text="Виберіть рік: ", font=courier_14, foreground='red')
        label_year.grid(row=3, column=0, ipadx=6, ipady=6, padx=5, pady=5)

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
                              foreground='red')
        label_path.grid(row=4, column=0, rowspan=2, ipadx=6, ipady=6, padx=5, pady=5)
        dialog_btn_8 = tk.Button(lf1, text="КВІТНЕВА-8", font=courier_10, width=12, state='disable',
                                 command=lambda: browse_directory( lf1, 4, 2, 3, dialog_btn_8, dialog_btn_30))
        dialog_btn_8.grid(row=4, column=1, ipadx=6, ipady=6, padx=5, pady=5)
        dialog_btn_30 = tk.Button(lf1, text="КВІТНЕВА-30-5", font=courier_10, width=12, state='disable',
                                  command=lambda: browse_directory(lf1, 5, 2, 4, dialog_btn_30, dialog_add_btn_8))
        dialog_btn_30.grid(row=5, column=1, ipadx=6, ipady=6, padx=5, pady=5)

        lf1.grid(column=0, row=5, padx=20, pady=10, sticky=W)

        # ========================= Обираємо шлях збереження файлів  ====================================

        lf4 = ttk.Frame(lf3, borderwidth=10, relief=SUNKEN)
        lf4.config(width=width_frame, height=130)
        lf4.grid_propagate(False)

        label_path_add = tk.Label(lf4, text="оберіть шлях \n зберігання \n файлів  ", font=courier_14, justify='center',
                                  foreground='red')
        label_path_add.grid(row=4, column=0, rowspan=2, ipadx=6, ipady=6, padx=5, pady=5)
        dialog_add_btn_8 = tk.Button(lf4, text="КВІТНЕВА-8", font=courier_10, width=12, state='disable',
                                     command=lambda: browse_directory( lf4, 4, 2, 5, dialog_add_btn_8, dialog_add_btn_30))
        dialog_add_btn_8.grid(row=4, column=1, ipadx=6, ipady=6, padx=5, pady=5)
        dialog_add_btn_30 = tk.Button(lf4, text="КВІТНЕВА-30-5", font=courier_10, width=12, state='disable',
                                      command=lambda: browse_directory( lf4, 5, 2, 6, dialog_add_btn_30, save_btn))
        dialog_add_btn_30.grid(row=5, column=1, ipadx=6, ipady=6, padx=5, pady=5)

        lf4.grid(column=0, row=6, padx=20, pady=10, sticky=W)

        # =======================INFO TABLE =========================================

        lf5 = ttk.Frame(lf3, borderwidth=10, relief=SUNKEN)
        lf5.config(width=width_frame, height=150)
        lf5.grid_propagate(False)

        lf5.grid(column=0, row=7, padx=20, pady=10, sticky=S)

        # =========================== Кнопка зберегти файли  ============================
        lf = ttk.Frame(lf3, borderwidth=10, relief=SUNKEN)
        lf.config(width=width_frame, height=80)
        lf.grid_propagate(False)

        save_btn = tk.Button(lf, text="ЗБЕРЕГТИ ФАЙЛИ", font=courier_10, state='disable', command=join_file)
        save_btn.grid(row=6, column=0, ipadx=6, ipady=6, padx=50, pady=10)

        # =========================== Кнопка EXIT  ============================

        exit_btn = tk.Button(lf, text="ЗАВЕРШИТИ", font=courier_10, command=confirm_exit)
        exit_btn.grid(row=6, column=2, ipadx=6, ipady=6, padx=400, pady=10)

        lf.grid(column=0, row=8, padx=20, pady=10, sticky=S)


        # ================= END ===================================================

        lf3.grid(column=0, row=1, ipadx=6, ipady=6, padx=20, pady=20)

        # root.mainloop()
        about_win.grab_set()
