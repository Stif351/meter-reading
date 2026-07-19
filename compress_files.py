import os
import tkinter as tk
from tkinter import ttk, font, messagebox, filedialog, SUNKEN

from PIL import Image


def change_photos(root):



    # def batch_compress_images(input_folder, output_folder, quality):
    def batch_compress_images():

        input_folder = 'd:/комуналка\Комуналка_Раевка_25/КВІТНЕВА_8/photos'  # папка з фото
        output_folder = 'd:/комуналка/dir_result'  # папка для готових файлів
        quality = 15

        # Створюємо папку для результатів
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            print(f"Створено папку: {output_folder}")

        count = 0
        # Перебираємо всі файли в робочій папці
        for filename in os.listdir(input_folder):
            # Перевіряємо розширення файлу (ігноруємо регістр)
            if filename.lower().endswith(('.jpg', '.jpeg')):
                input_path = os.path.join(input_folder, filename)
                output_path = os.path.join(output_folder, filename)

                try:
                    with Image.open(input_path) as img:

                        img.save(output_path, "JPEG", quality=quality)

                    # print(f"Успішно оброблено: {filename}")
                    count += 1
                except Exception as e:
                    print(f"Помилка обробки файлу {filename}: {e}")
                    messagebox.showerror("ПОМИЛКА ОБРОБКИ", f"Помилка обробки файлу {filename}", parent=about_win)

        messagebox.showinfo('ОБРОБКА ФАЙЛІВ ', f'Успішно оброблено файлів {count}', parent=about_win)
        # print('FILES = ', count)
    # source_dir = 'd:/комуналка\Комуналка_Раевка_25/КВІТНЕВА_8/photos'  # папка з фото
    # result_dir = 'd:/комуналка\Комуналка_Раевка_25/dir_result'  # папка для готових файлів

    # batch_compress_images(source_dir, result_dir, quality=15)

    def confirm_exit():

        about_win.destroy()

    # =/////////////////===================  MAIN ==========================////////////////////////////////

    about_win = tk.Toplevel(root)
    about_win.title("ОБРОБКА ФОТО ЛІЧИЛЬНИКІВ")
    about_win.geometry("600x400+300+50")
    about_win.configure(bg="#2c3e50")  # Власний колір фону

    courier_10 = font.Font(family="Courier", size=10, weight=font.BOLD)
    # courier_14 = font.Font(family="Courier", size=14, weight=font.BOLD)
    courier_18 = font.Font(family="Courier", size=18, weight=font.BOLD)
    # width_frame = 800



    label = tk.Label(about_win, text="ОБРОБКА ФОТО ЛІЧИЛЬНИКІВ", fg="BLUE", font=courier_18)
    label.grid(row=0, column=0, columnspan=3, ipadx=6, ipady=6, padx=5, pady=5)

    lf_MF = ttk.Frame(about_win, borderwidth=10, relief=SUNKEN)
    lf_MF.config(width=850, height=600)

    save_btn = tk.Button(lf_MF, text="ОБРОБИТИ ФОТО", font=courier_10, state='normal', command=batch_compress_images)
    save_btn.grid(row=0, column=0, ipadx=6, ipady=6, padx=50, pady=30)

    exit_btn = tk.Button(lf_MF, text=" ЗАВЕРШИТИ ", font=courier_10, foreground='red', command=confirm_exit)
    exit_btn.grid(row=1, column=0, ipadx=6, ipady=6, padx=50, pady=30)

    lf_MF.grid(column=0, row=2, ipadx=6, ipady=6, padx=120, pady=50)

    about_win.grab_set()