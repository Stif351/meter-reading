import os
import tkinter as tk
from tkinter import ttk, font, messagebox, filedialog, SUNKEN
from tkinter.constants import SOLID
from PIL import Image, ImageOps


def change_photos(root):

    def batch_compress_images():

        input_folder = filedialog.askdirectory(initialdir=r" ", title="ОБРАТИ ПАПКУ З ФАЙЛАМИ")  # папка з фото
        output_folder = filedialog.askdirectory(initialdir=r" ", title="ОБРАТИ ПАПУ ДЛЯ ЗБЕРІГАННЯ ФАЙЛІВ")  # папка для готових файлів

        # прогрес бар
        # рахуємо кількість файлів у папці
        files_to_process = [
            f
            for f in os.listdir(input_folder)
            if os.path.isfile(os.path.join(input_folder, f)) and f.lower().endswith(('.jpeg', 'jpg'))
        ]

        total_files = len(files_to_process)
        progress_bar["maximum"] = total_files
        progress_bar["value"] = 0

        count = 0
        quality = 15
        # Перебираємо всі файли в робочій папці
        for filename in os.listdir(input_folder):
            # Перевіряємо розширення файлу (ігноруємо регістр)
            if filename.lower().endswith(('.jpg', '.jpeg')):
                input_path = os.path.join(input_folder, filename)
                output_path = os.path.join(output_folder, filename)

                try:
                    with Image.open(input_path) as img:

                        img = ImageOps.exif_transpose(img)
                        img.save(output_path, "JPEG", quality=quality)

                    count += 1
                    progress_bar["value"] = count
                    root.update_idletasks()
                except Exception as e:
                    print(f"Помилка обробки файлу {filename}: {e}")
                    messagebox.showerror("ПОМИЛКА ОБРОБКИ", f"Помилка обробки файлу {filename}", parent=about_win)

        messagebox.showinfo('ОБРОБКА ФАЙЛІВ ', f'Успішно оброблено файлів: {count}. \nШлях до файлів: {output_folder}', parent=about_win)

    def confirm_exit():

        about_win.destroy()

    # =/////////////////===================  MAIN ==========================////////////////////////////////

    about_win = tk.Toplevel(root)
    about_win.title("ОБРОБКА ФОТО ЛІЧИЛЬНИКІВ")

    window_width, window_height = 600, 400
    screen_width = about_win.winfo_screenwidth()
    screen_height = about_win.winfo_screenheight()
    center_x = int((screen_width / 2) - (window_width / 2))
    center_y = int((screen_height / 2) - (window_height / 2))

    about_win.geometry(f'{window_width}x{window_height}+{center_x}+{center_y - 100}')
    about_win.configure(bg="#2c3e50")  # Власний колір фону

    courier_10 = font.Font(family="Courier", size=10, weight=font.BOLD)
    courier_18 = font.Font(family="Courier", size=18, weight=font.BOLD)

    label = tk.Label(about_win, text="ОБРОБКА ФОТО ЛІЧИЛЬНИКІВ", fg="BLUE", font=courier_18)
    label.grid(row=0, column=0, columnspan=3, ipadx=6, ipady=6, padx=15, pady=10)

    progress_bar = ttk.Progressbar(about_win, orient=tk.HORIZONTAL, length=300, mode="determinate")
    progress_bar.grid(row=1, column=0, ipadx=6, ipady=6, padx=5, pady=5)

    lf_MF = ttk.Frame(about_win, borderwidth=10, relief=SUNKEN)
    lf_MF.config(width=850, height=600)

    save_btn = tk.Button(lf_MF, text="ОБРОБИТИ ФОТО", font=courier_10, state='normal', command=batch_compress_images)
    save_btn.grid(row=0, column=0, ipadx=6, ipady=6, padx=50, pady=20)

    exit_btn = tk.Button(lf_MF, text=" ЗАВЕРШИТИ ", font=courier_10, foreground='red', relief=SOLID, command=confirm_exit)
    exit_btn.grid(row=1, column=0, ipadx=6, ipady=6, padx=50, pady=20)

    lf_MF.grid(column=0, row=2, ipadx=6, ipady=6, padx=150, pady=50)

    about_win.grab_set()