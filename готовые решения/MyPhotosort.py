import os
import shutil
import subprocess
import sys


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


def get_files_and_folders(path="."):
    contents = os.listdir(path)
    folders = []
    files = []
    for item in contents:
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            folders.append(item_path)
        else:
            print(str(os.path)[str(os.path).rfind('.'):])
        if os.path.isfile(item_path) and item_path[item_path.rfind('.'):] in image_extensions:
            files.append(item_path)
    return folders, files


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


def sort_to_month(folder_path):
    months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь",
              "Декабрь", "Иные"]
    folders, files = get_files_and_folders(folder_path)
    for file in files:
        metadata = get_image_metadata(file)
        if metadata:
            print(file)
            try:
                month = metadata['DateTimeOriginal'][5:7]
                month_path = os.path.join(folder_path, months[int(month) - 1])
                if not os.path.exists(month_path):
                    os.mkdir(month_path)
                shutil.move(file, month_path)
            except:
                month_path = os.path.join(folder_path, "Иные")
                if not os.path.exists(month_path):
                    os.mkdir(month_path)
                shutil.move(file, os.path.join(folder_path, "Иные"))
        else:
            shutil.move(file, os.path.join(folder_path, "Иные"))


pth = input()
# Получение раздельных списков
folders, files = get_files_and_folders(pth)
# print("Папки:", folders)
# print("Файлы:", files)

for folder in folders:
    if folder[-4:-2] == "20":
        sort_to_month(folder)
