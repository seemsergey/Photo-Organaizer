import os
import shutil
import subprocess
import sys
import tkinter as tk
from tkinter import ttk


def InstallPillow():
    try:
        from PIL import Image
        from PIL.ExifTags import TAGS
        print("Библиотека 'Pillow' уже установлена.")
    except ImportError:
        print("Библиотека 'Pillow' не найдена. Устанавливаю...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow"])
        print("Библиотека 'Pillow' успешно установлена.")


class ProgressWindow(tk.Toplevel):
    def __init__(self, total_files):
        super().__init__()
        self.title("Обработка фото")
        self.geometry("300x100")
        self.total_files = total_files
        self.processed_files = 0

        self.progress = ttk.Progressbar(self, length=250, maximum=total_files, mode='determinate')
        self.progress.pack(pady=10)

    def UpdateProgress(self, processed_count):
        self.processed_files = processed_count
        self.progress['value'] = processed_count
        self.update_idletasks()


class PhotoHandler:
    def __init__(self, FoldPath, SortFolderPath, command):
        InstallPillow()
        from PIL import Image
        from PIL.ExifTags import TAGS

        self.Image = Image
        self.TAGS = TAGS

        self.image_extensions = [
            ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif", ".webp",
            ".heif", ".heic", ".raw", ".svg", ".ico", ".jfif", ".pjpeg", ".pjp",
            ".avif", ".dds", ".exr", ".ras", ".ppm", ".pgm", ".pbm", ".pnm", ".xpm",
        ]
        self.image_extensions += [ext.upper() for ext in self.image_extensions]  # учёт заглавных

        self.months = [
            "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август",
            "Сентябрь", "Октябрь", "Ноябрь", "Декабрь", "Иные"
        ]

        self.pth = FoldPath
        self.sortpth = SortFolderPath
        self.operation = command
        self.MovedFiles = 0
        self.BadFiles = 0
        self.DirsMade = 0

        self.ProgressBar = None

    def GetFiles(self, path="."):
        contents = os.listdir(path)
        files = []
        for item in contents:
            item_path = os.path.join(path, item)
            if os.path.isfile(item_path) and item_path[item_path.rfind('.'):].lower() in self.image_extensions:
                files.append(item_path)
        return files

    def GetImgMetadata(self, image_path):
        try:
            img = self.Image.open(image_path)
            exif_data = img._getexif()
        except Exception as e:
            print(f"Ошибка при чтении {image_path}: {e}")
            return None

        if exif_data:
            metadata = {}
            for tag, value in exif_data.items():
                tag_name = self.TAGS.get(tag, tag)
                metadata[tag_name] = value
            return metadata
        else:
            return None

    def PhotoSort(self, FilePath):
        metadata = self.GetImgMetadata(FilePath)
        if metadata and "DateTimeOriginal" in metadata:
            month = metadata['DateTimeOriginal'][5:7]
            year = metadata['DateTimeOriginal'][:4]

            year_path = os.path.join(self.sortpth, year)
            if not os.path.exists(year_path):
                os.mkdir(year_path)
                self.DirsMade += 1

            month_path = os.path.join(year_path, self.months[int(month) - 1])
            if not os.path.exists(month_path):
                os.mkdir(month_path)
                self.DirsMade += 1

            target_path = os.path.join(month_path, os.path.basename(FilePath))
            self.MovedFiles += 1
        else:
            other_path = os.path.join(self.sortpth, "Иные")
            if not os.path.exists(other_path):
                os.mkdir(other_path)
                self.DirsMade += 1
            target_path = os.path.join(other_path, os.path.basename(FilePath))
            self.BadFiles += 1

        if self.operation == "copy":
            shutil.copy(FilePath, target_path)
        elif self.operation == "move":
            shutil.move(FilePath, target_path)

    def ProcessSort(self):
        files = self.GetFiles(self.pth)
        self.ProgressBar = ProgressWindow(len(files))
        for file in files:
            self.PhotoSort(file)
            self.ProgressBar.UpdateProgress(self.MovedFiles + self.BadFiles)
        self.ProgressBar.destroy()

    def Analysis(self):
        files = self.GetFiles(self.pth)
        self.ProgressBar = ProgressWindow(len(files))
        for file in files:
            metadata = self.GetImgMetadata(file)
            if not (metadata and "DateTimeOriginal" in metadata):
                self.BadFiles += 1
            else:
                self.MovedFiles += 1

            self.ProgressBar.UpdateProgress(self.MovedFiles + self.BadFiles)
        self.ProgressBar.destroy()


if __name__ == "__main__":
    PhotoHandler()
