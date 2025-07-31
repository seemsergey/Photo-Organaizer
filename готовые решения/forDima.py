import os
import shutil
import subprocess
import sys
import tkinter as tk

def install_pillow():
    try:
        from PIL import Image
        from PIL.ExifTags import TAGS
        print("Библиотека 'Pillow' уже установлена.")
    except ImportError:
        print("Библиотека 'Pillow' не найдена. Устанавливаю...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow"])
        print("Библиотека 'Pillow' успешно установлена.")

        # Пробуем импортировать снова
        try:
            from PIL import Image
            from PIL.ExifTags import TAGS
            print("Импорт прошёл успешно.")
        except ImportError:
            print("Ошибка при повторном импорте библиотеки!")


install_pillow()
from PIL import Image
from PIL.ExifTags import TAGS

image_extensions = [
    ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif", ".webp",
    ".heif", ".heic", ".raw", ".svg", ".ico", ".jfif", ".pjpeg", ".pjp",
    ".avif", ".dds", ".exr", ".ras", ".ppm", ".pgm", ".pbm", ".pnm", ".xpm",
    ".JPG", ".JPEG", ".PNG", ".GIF", ".BMP", ".TIFF", ".TIF", ".WEBP",
    ".HEIF", ".HEIC", ".RAW", ".SVG", ".ICO", ".JFIF", ".PJPEG", ".PJP",
    ".AVIF", ".DDS", ".EXR", ".RAS", ".PPM", ".PGM", ".PBM", ".PNM", ".XPM"
]
months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь",
          "Декабрь", "Иные"]


def get_files(path="."):
    contents = os.listdir(path)
    files = []
    for item in contents:
        item_path = os.path.join(path, item)
        if os.path.isfile(item_path) and item_path[item_path.rfind('.'):] in image_extensions:
            files.append(item_path)
    return files


def get_image_metadata(image_path):
    img = Image.open(image_path)
    exif_data = img._getexif()

    if exif_data:
        metadata = {}
        for tag, value in exif_data.items():
            tag_name = TAGS.get(tag, tag)
            metadata[tag_name] = value
        return metadata
    else:
        return None


def sort_to_date(path):
    metadata = get_image_metadata(path)
    if metadata:
        print(path)
        month = metadata['DateTimeOriginal'][5:7]
        year = metadata['DateTimeOriginal'][:4]

        year_path = os.path.join(pth, year)
        if not os.path.exists(year_path):
            os.mkdir(year_path)

        month_path = os.path.join(year_path, months[int(month) - 1])
        if not os.path.exists(month_path):
            os.mkdir(month_path)

        shutil.move(path, month_path)
    else:
        shutil.move(path, os.path.join(pth, "Иные"))


pth = input()
files = get_files(pth)
print("Файлы:", files)
if not os.path.exists(os.path.join(pth, "Иные")):
    os.mkdir(os.path.join(pth, "Иные"))

for file in files: sort_to_date(file)
