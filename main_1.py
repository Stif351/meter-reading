from tkinter import SUNKEN, W, END
import search_data
import tkinter as tk
from tkinter import ttk, font, messagebox, filedialog
from tkinter.constants import SOLID
from datetime import datetime

def add_app(root):

        # ================== DATES ==============================================

        months = [" ", "січень", "лютий", "березень", "квітень", "травень", "червень", "липень", "серпень", "вересень",
                          "жовтень", "листопад", "грудень"]

        energy = ['газу', 'електроенергії', 'води']

        entries = []
        address = [' ', 'КВІТНЕВА-8', 'КВІТНЕВА-30-5']

        date_result = {
            "month_name": "",
            "year": "",
            "address": ""
        }

        current_year = datetime.now().year
        report_options_year = [str(current_year), str(current_year - 1)]


        # ================================== FUNCTIONS   ============================================


        def selected(event):

            widget = event.widget
            tag = getattr(widget, "tag", None)
            value = widget.get()

            if tag == "month":
                label_report(lf_H1, 1, 3, value)
                date_result["month_name"] = value

            elif tag == "year":
                label_report(lf_H1, 0, 3, value)
                date_result["year"] =  value

            elif tag == "address":
                label_report(lf_H1, 2, 3,value)
                date_result["address"] = value



        def add_date():

            data_gas_num = entries[0].get()
            data_light_num = entries[1].get()
            data_water_num = entries[2].get()
            table_name = f'year{date_result["year"]}'
            month =  date_result["month_name"]

            new_folder_path = filedialog.asksaveasfilename(

                title="Виберіть файл для запису",
                defaultextension=".xlsx",
                filetypes=[("Exel файли", "*.xlsx"), ("Усі файли", "*.*")],
                confirmoverwrite=False
            )

            search_data.find_in_excel_table(
                new_folder_path,
                'A1',
                table_name,
                'Дата',
                month,
                data_gas_num,
                data_light_num,
                data_water_num
            )

            clear_fields()

        def clear_fields():

            for field in entries:

                field.delete(0, END)

            selected_year.set('')
            selected_report.set('')
            selected_a.set('')

            messagebox.showinfo("Успіх", "Дані успішно збережено!", parent=about_win)


        def label_report(*args):
            report_label = ttk.Label(args[0], text=f'Ви вибрали:  {args[3]}', font=courier_10, foreground='green')
            report_label.grid(row=args[1], column=args[2], ipadx=6, ipady=6, padx=55, pady=5)


        def validate_input(new_value):
            if new_value == "":  # дозволяємо очищення поля
                return True
            if not new_value.isdigit():
                messagebox.showerror("Помилка вводу", "Дозволені тільки цифри!", parent=about_win)
                return False
            if len(new_value) > 5:
                messagebox.showerror("Помилка вводу", "Максимум 5 цифр!", parent=about_win)
                return False
            return True

        def confirm_exit():

            about_win.destroy()


        # =/////////////////===================  MAIN ==========================////////////////////////////////


        about_win = tk.Toplevel(root)
        about_win.title("Внесення показників")

        window_width, window_height = 900, 600
        screen_width = about_win.winfo_screenwidth()
        screen_height = about_win.winfo_screenheight()
        center_x = int((screen_width / 2) - (window_width / 2))
        center_y = int((screen_height / 2) - (window_height / 2))

        about_win.geometry(f'{window_width}x{window_height}+{center_x}+{center_y - 100}')
        about_win.configure(bg="#2c3e50")  # Власний колір фону


        courier_10 = font.Font(family="Courier", size=10, weight="bold")
        courier_14 = font.Font(family="Courier", size=14, weight="bold")
        courier_18 = font.Font(family="Courier", size=18, weight="bold")
        width_frame = 800

        label = tk.Label(about_win, text="ДОДАВАННЯ ПОКАЗНИКІВ ЛІЧИЛЬНИКІВ У ФАЙЛ", fg="BLUE", font=courier_18)
        label.grid(row=0, column=0, columnspan=3, ipadx=6, ipady=6, padx=5, pady=5)

        # ========================  main frame  =======================================

        lf_MF = ttk.Frame(about_win, borderwidth=10, relief=SUNKEN)
        lf_MF.config(width=850, height=500)


        lf_H1 = ttk.Frame(lf_MF, borderwidth=10, relief=SUNKEN)
        lf_H1.config(width=width_frame, height=160)
        lf_H1.grid_propagate(False)

        label_year = tk.Label(lf_H1, text="Виберіть рік: ", font=courier_14)
        label_year.grid(row=0, column=0, ipadx=6, ipady=6, padx=5, pady=5, sticky=W)

        selected_year = tk.StringVar(value=report_options_year[0])
        year_select = ttk.Combobox(lf_H1, textvariable=selected_year, values=report_options_year)
        year_select.tag = "year"
        year_select.grid(row=0, column=1, padx=5, pady=5, sticky=W)
        year_select.bind("<<ComboboxSelected>>", selected)

        label_month = tk.Label(lf_H1, text="Виберіть місяць: ", font=courier_14)
        label_month.grid(row=1, column=0, ipadx=6, ipady=6, padx=5, pady=5, sticky=W)

        selected_report = tk.StringVar(value=months[0])
        report_menu = ttk.Combobox(lf_H1, textvariable=selected_report, values=months)
        report_menu.tag = "month"
        report_menu.grid(row=1, column=1,padx=5, pady=5, sticky=W)
        report_menu.bind("<<ComboboxSelected>>", selected)

        label_a = tk.Label(lf_H1, text="Виберіть адресу: ", font=courier_14)
        label_a.grid(row=2, column=0, ipadx=6, ipady=6, padx=5, pady=5, sticky=W)

        selected_a = tk.StringVar(value=address[0])
        address_t = ttk.Combobox(lf_H1, textvariable=selected_a, values=address)
        address_t.tag = 'address'
        address_t.grid(row=2, column=1,padx=5, pady=5 )
        address_t.bind("<<ComboboxSelected>>", selected)


        # ========================  end main frame  =======================================

        # ***************************** frame date count 8  **********************************

        lf_H8 = ttk.Frame(lf_MF, borderwidth=10, relief=SUNKEN)
        lf_H8.config(width=width_frame, height=250)
        lf_H8.grid_propagate(False)

        vcmd = (lf_H8.register(validate_input), "%P")


        for i, d in enumerate(energy):  # створюємо 3 поля


            label = tk.Label(lf_H8, text=f"Введіть показники лічильника {d}: ",  font=courier_14)
            label.grid(row=i, column=0, ipadx=6, ipady=6, padx=5, pady=5, sticky=W)

            entry = tk.Entry(lf_H8, validate="key", validatecommand=vcmd)
            entry.grid(row=i, column=1, ipadx=6, ipady=6)

            entries.append(entry)


        # ************************************ КНОПКА ДОБАВИТИ  ***********************************************************

        save_btn = tk.Button(lf_H8, text="ЗБЕРЕГТИ ПОКАЗНИКИ", font=courier_10, foreground='green', state='normal', command=add_date)
        save_btn.grid(row=3, column=1, ipadx=6, ipady=6, padx=50, pady=30)

        exit_btn = tk.Button(lf_H8, text="ЗАВЕРШИТИ", font=courier_10, foreground='red', relief=SOLID, command=confirm_exit)
        exit_btn.grid(row=3, column=0, ipadx=6, ipady=6, padx=50, pady=1)

        lf_H1.grid(column=0, row=2, padx=20, pady=10, sticky=W)
        lf_H8.grid(column=0, row=5, padx=20, pady=10, sticky=W)


        lf_MF.grid(column=0, row=1, ipadx=6, ipady=6, padx=20, pady=20, sticky=W)


        about_win.grab_set()

