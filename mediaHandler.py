import os
import shutil
import subprocess
import sys
import tkinter as tk
from tkinter import ttk
from datetime import datetime


def install_dependencies():
    for lib, package in [("PIL", "pillow"), ("hachoir", "hachoir")]:
        try:
            __import__(lib)
        except ImportError:
            print(f"Установка {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])


class ProgressWindow(tk.Toplevel):
    def __init__(self, total_files):
        super().__init__()
        self.title("Обработка файлов")
        self.geometry("300x100")
        self.progress = ttk.Progressbar(self, length=250, maximum=total_files, mode='determinate')
        self.progress.pack(pady=20)

    def update(self, count):
        self.progress['value'] = count
        self.update_idletasks()


class MediaHandler:
    def __init__(self, source_path, dest_path, operation, process_photos, process_videos):
        install_dependencies()
        from PIL import Image
        from PIL.ExifTags import TAGS
        from hachoir.parser import createParser
        from hachoir.metadata import extractMetadata

        self.Image = Image
        self.TAGS = TAGS
        self.createParser = createParser
        self.extractMetadata = extractMetadata

        self.src = source_path
        self.dst = dest_path
        self.op = operation  # "move" или "copy"
        self.do_photo = process_photos
        self.do_video = process_videos

        self.photo_exts = [".jpg", ".jpeg", ".png", ".tiff", ".heic", ".webp"]
        self.video_exts = [".mp4", ".mov", ".avi", ".mkv", ".wmv", ".3gp", ".mpg"]

        # Расширяем список заглавными буквами
        self.photo_exts += [e.upper() for e in self.photo_exts]
        self.video_exts += [e.upper() for e in self.video_exts]

        self.months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
                       "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]

        self.count_ok = 0
        self.count_bad = 0
        self.dirs_made = 0

    def get_all_files(self):
        valid_files = []
        for root, _, files in os.walk(self.src):
            for f in files:
                _, ext = os.path.splitext(f)
                if self.do_photo and ext in self.photo_exts:
                    valid_files.append(os.path.join(root, f))
                elif self.do_video and ext in self.video_exts:
                    valid_files.append(os.path.join(root, f))
        return valid_files

    def get_date(self, file_path):
        _, ext = os.path.splitext(file_path)

        # Логика для ФОТО
        if ext in self.photo_exts:
            try:
                img = self.Image.open(file_path)
                exif = img._getexif()
                if exif:
                    for tag, value in exif.items():
                        if self.TAGS.get(tag) == 'DateTimeOriginal':
                            return datetime.strptime(value[:10], '%Y:%m:%d')
            except:
                pass

        # Логика для ВИДЕО
        elif ext in self.video_exts:
            try:
                parser = self.createParser(file_path)
                if parser:
                    with parser:
                        meta = self.extractMetadata(parser)
                        if meta and meta.has('creation_date'):
                            return meta.get('creation_date')
            except:
                pass

        return None

    def process(self, is_analysis=False):
        files = self.get_all_files()
        if not files: return

        progress = ProgressWindow(len(files))

        for f_path in files:
            date = self.get_date(f_path)

            if not is_analysis:
                if date:
                    year, month = str(date.year), self.months[date.month - 1]
                    target_dir = os.path.join(self.dst, year, month)
                    self.count_ok += 1
                else:
                    target_dir = os.path.join(self.dst, "Неизвестная_дата")
                    self.count_bad += 1

                os.makedirs(target_dir, exist_ok=True)
                target_path = os.path.join(target_dir, os.path.basename(f_path))

                # Избегаем перезаписи если файл с таким именем уже есть
                if os.path.exists(target_path):
                    name, ext = os.path.splitext(target_path)
                    target_path = f"{name}_{datetime.now().strftime('%H%M%S')}{ext}"

                if self.op == "copy":
                    shutil.copy2(f_path, target_path)
                else:
                    shutil.move(f_path, target_path)
            else:
                if date:
                    self.count_ok += 1
                else:
                    self.count_bad += 1

            progress.update(self.count_ok + self.count_bad)

        progress.destroy()