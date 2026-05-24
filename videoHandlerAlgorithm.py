import os
import shutil
import subprocess
import sys
import tkinter as tk
from tkinter import ttk
from datetime import datetime


def InstallHachoir():
    try:
        import hachoir
    except ImportError:
        print("Библиотека 'hachoir' не найдена. Устанавливаю...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "hachoir"])
        print("Библиотека 'hachoir' успешно установлена.")


class ProgressWindow(tk.Toplevel):
    def __init__(self, total_files):
        super().__init__()
        self.title("Обработка видео")
        self.geometry("300x100")
        self.total_files = total_files
        self.processed_files = 0
        self.progress = ttk.Progressbar(self, length=250, maximum=total_files, mode='determinate')
        self.progress.pack(pady=20)

    def UpdateProgress(self, processed_count):
        self.processed_files = processed_count
        self.progress['value'] = processed_count
        self.update_idletasks()


class VideoHandler:
    def __init__(self, FoldPath, SortFolderPath, command):
        InstallHachoir()
        from hachoir.parser import createParser
        from hachoir.metadata import extractMetadata

        self.createParser = createParser
        self.extractMetadata = extractMetadata

        self.video_extensions = [
            ".mp4", ".mov", ".avi", ".mkv", ".wmv", ".3gp", ".flv", ".mpg", ".mpeg", ".m4v"
        ]
        self.video_extensions += [ext.upper() for ext in self.video_extensions]

        self.months = [
            "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август",
            "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
        ]

        self.pth = FoldPath
        self.sortPth = SortFolderPath
        self.operation = command
        self.MovedFiles = 0
        self.BadFiles = 0
        self.DirsMade = 0
        self.ProgressBar = None

    def GetFiles(self, path="."):
        videoFiles = []
        for root, dirs, files in os.walk(path):
            for file in files:
                _, ext = os.path.splitext(file)
                if ext.lower() in self.video_extensions:
                    videoFiles.append(os.path.join(root, file))
        return videoFiles

    def GetVideoDate(self, video_path):
        """Пытается достать дату создания из метаданных видео."""
        try:
            parser = self.createParser(video_path)
            if not parser:
                return None

            with parser:
                metadata = self.extractMetadata(parser)
                if metadata and metadata.has('creation_date'):
                    return metadata.get('creation_date')
        except Exception as e:
            print(f"Ошибка метаданных для {video_path}: {e}")
        return None

    def VideoSort(self, FilePath):
        creation_date = self.GetVideoDate(FilePath)

        if creation_date:
            # creation_date обычно объект datetime
            year = str(creation_date.year)
            month_idx = creation_date.month - 1

            year_path = os.path.join(self.sortPth, year)
            if not os.path.exists(year_path):
                os.makedirs(year_path, exist_ok=True)
                self.DirsMade += 1

            month_path = os.path.join(year_path, self.months[month_idx])
            if not os.path.exists(month_path):
                os.makedirs(month_path, exist_ok=True)
                self.DirsMade += 1

            target_path = os.path.join(month_path, os.path.basename(FilePath))
            self.MovedFiles += 1
        else:
            # Если метаданных нет
            other_path = os.path.join(self.sortPth, "Иные_видео")
            if not os.path.exists(other_path):
                os.makedirs(other_path, exist_ok=True)
                self.DirsMade += 1
            target_path = os.path.join(other_path, os.path.basename(FilePath))
            self.BadFiles += 1

        # Обработка конфликтов имен (если файл уже существует)
        if os.path.exists(target_path):
            name, ext = os.path.splitext(target_path)
            target_path = f"{name}_{datetime.now().strftime('%H%M%S')}{ext}"

        if self.operation == "copy":
            shutil.copy2(FilePath, target_path)
        elif self.operation == "move":
            shutil.move(FilePath, target_path)

    def ProcessSort(self):
        files = self.GetFiles(self.pth)
        if not files: return
        self.ProgressBar = ProgressWindow(len(files))
        for file in files:
            self.VideoSort(file)
            self.ProgressBar.UpdateProgress(self.MovedFiles + self.BadFiles)
        self.ProgressBar.destroy()

    def Analysis(self):
        files = self.GetFiles(self.pth)
        if not files: return
        self.ProgressBar = ProgressWindow(len(files))
        for file in files:
            date = self.GetVideoDate(file)
            if not date:
                self.BadFiles += 1
            else:
                self.MovedFiles += 1
            self.ProgressBar.UpdateProgress(self.MovedFiles + self.BadFiles)
        self.ProgressBar.destroy()