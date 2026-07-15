import os
from PIL import Image


def change_photos():
    def batch_compress_images(input_folder, output_folder, quality):
        # Створюємо папку для результатів
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            print(f"Створено папку: {output_folder}")

        # Перебираємо всі файли в робочій папці
        for filename in os.listdir(input_folder):
            # Перевіряємо розширення файлу (ігноруємо регістр)
            if filename.lower().endswith(('.jpg', '.jpeg')):
                input_path = os.path.join(input_folder, filename)
                output_path = os.path.join(output_folder, filename)

                try:
                    with Image.open(input_path) as img:

                        img.save(output_path, "JPEG", quality=quality)

                    print(f"Успішно оброблено: {filename}")
                except Exception as e:
                    print(f"Помилка обробки файлу {filename}: {e}")

    source_dir = 'd:/комуналка\Комуналка_Раевка_25/КВІТНЕВА_8/photos'  # папка з фото
    result_dir = 'd:/комуналка\Комуналка_Раевка_25/dir_result'  # папка для готових файлів

    batch_compress_images(source_dir, result_dir, quality=15)