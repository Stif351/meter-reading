from tkinter import SUNKEN, W, END
import search_data
import tkinter as tk
from tkinter import font, messagebox, filedialog
from tkinter import ttk


def add_app(root):

        # ================== DATES ==============================================

        months = [" ", "січень", "лютий", "березень", "квітень", "травень", "червень", "липень", "серпень", "вересень",
                          "жовтень", "листопад", "грудень"]

        energy = ['газу', 'електроенергії', 'води']

        entries = []
        address = [' ', 'КВІТНЕВА-8', 'КВІТНЕВА-30-5']

        text = ''
        text2 = ''
        year = 2026
        table_name = f'year{year}'
        # ================================== FUNCTIONS   ============================================

        def selected(event):
            # global text, text2
            nonlocal text, text2
            widget = event.widget
            tag = getattr(widget, "tag", None)
            text1 = widget.get()

            if tag == "month":
                text = text1
                label_report(lf_H1, 2, 0, text)

            if tag == "address":
                text2 = text1
                label_report(lf_H1, 2, 1, text2)

        def add_date():

            data_gas_num = entries[0].get()
            data_light_num = entries[1].get()
            data_water_num = entries[2].get()

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
                text,
                data_gas_num,
                data_light_num,
                data_water_num
            )

            clear_fields()

        def clear_fields():

            for field in entries:

                field.delete(0, END)

            selected_report.set('')
            selected_a.set('')

            messagebox.showinfo("Успіх", "Дані успішно збережено!", parent=about_win)



        def label_report(frame, row, column, value):

            report_label = ttk.Label(frame, text=f'Ви вибрали:{value}', font=courier_14, foreground='green')
            report_label.grid(row=row, column=column, ipadx=6, ipady=6, padx=55, pady=5)
            print('l>>>>>')

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
        about_win.geometry("900x600+500+50")
        about_win.configure(bg="#2c3e50")  # Власний колір фону

        courier_10 = font.Font(family="Courier", size=10, weight=font.BOLD)
        courier_14 = font.Font(family="Courier", size=14, weight=font.BOLD)
        courier_18 = font.Font(family="Courier", size=18, weight=font.BOLD)
        width_frame = 800

        label = tk.Label(about_win, text="ДОДАВАННЯ ПОКАЗНИКІВ ЛІЧИЛЬНИКІВ У ФАЙЛ", fg="BLUE", font=courier_18)
        label.grid(row=0, column=0, columnspan=3, ipadx=6, ipady=6, padx=5, pady=5)

        # ========================  main frame  =======================================

        lf_MF = ttk.Frame(about_win, borderwidth=10, relief=SUNKEN)
        lf_MF.config(width=850, height=600)


        lf_H1 = ttk.Frame(lf_MF, borderwidth=10, relief=SUNKEN)
        lf_H1.config(width=width_frame, height=110)
        lf_H1.grid_propagate(False)

        label_month = tk.Label(lf_H1, text="Виберіть місяць: ", font=courier_14, foreground='red')
        label_month.grid(row=0, column=0, ipadx=6, ipady=6, padx=5, pady=5, sticky=W)

        selected_report = tk.StringVar(value=months[0])
        report_menu = ttk.Combobox(lf_H1, textvariable=selected_report, values=months)
        report_menu.tag = "month"
        report_menu.grid(row=0, column=1,padx=5, pady=5, sticky=W)
        report_menu.bind("<<ComboboxSelected>>", selected)

        label_a = tk.Label(lf_H1, text="Виберіть адресу: ", font=courier_14, foreground='red')
        label_a.grid(row=1, column=0, ipadx=6, ipady=6, padx=5, pady=5, sticky=W)

        selected_a = tk.StringVar(value=address[0])
        address_t = ttk.Combobox(lf_H1, textvariable=selected_a, values=address)
        address_t.tag = 'address'
        address_t.grid(row=1, column=1,padx=5, pady=5 )
        address_t.bind("<<ComboboxSelected>>", selected)


        # ========================  end main frame  =======================================

        # ***************************** frame date count 8  **********************************

        lf_H8 = ttk.Frame(lf_MF, borderwidth=10, relief=SUNKEN)
        lf_H8.config(width=width_frame, height=320)
        lf_H8.grid_propagate(False)

        vcmd = (lf_H8.register(validate_input), "%P")


        for i, d in enumerate(energy):  # створюємо 3 поля


            label = tk.Label(lf_H8, text=f"Введіть показники лічильника {d}: ",  font=courier_14, foreground='red')
            label.grid(row=i, column=0, ipadx=6, ipady=6, padx=5, pady=5)

            entry = tk.Entry(lf_H8, validate="key", validatecommand=vcmd)
            entry.grid(row=i, column=1, ipadx=6, ipady=6)

            entries.append(entry)


        # ************************************ КНОПКА ДОБАВИТИ  ***********************************************************

        save_btn = tk.Button(lf_H8, text="ЗБЕРЕГТИ ПОКАЗНИКИ", font=courier_10, state='normal', command=add_date)
        save_btn.grid(row=3, column=0, ipadx=6, ipady=6, padx=50, pady=30)

        exit_btn = tk.Button(lf_H8, text="ЗАВЕРШИТИ", font=courier_10, foreground='red', command=confirm_exit)
        exit_btn.grid(row=4, column=0, ipadx=6, ipady=6, padx=50, pady=1)

        lf_H1.grid(column=0, row=2, padx=20, pady=10, sticky=W)
        lf_H8.grid(column=0, row=5, padx=20, pady=10, sticky=W)


        lf_MF.grid(column=0, row=1, ipadx=6, ipady=6, padx=20, pady=20, sticky=W)


        about_win.grab_set()

