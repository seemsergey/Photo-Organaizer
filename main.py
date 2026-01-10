import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

from photoHandlerAlgorithm import PhotoHandler


class PhotosorterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Сортировщик фото")
        self.geometry("275x150")
        self.resizable(False, False)
        self.report = None
        self.text = None
        self.SaveButton = None
        self.CloneButton = None
        self.OkButton = None
        self.AnalysButton = ttk.Button(text="Проанализировать файлы", command=lambda: self.AnalysisStart())
        self.SortButton = ttk.Button(text="Отсортировать файлы", command=lambda: self.ChangeButton("sort"))
        self.AnalysButton.grid(column=0, row=1, sticky="nsew", padx=10)
        self.SortButton.grid(column=1, row=1, sticky="nsew", padx=10)

    def AnalysisStart(self):
        FolderPath = filedialog.askdirectory(title="Выберите папку с фото")
        if FolderPath:
            handler = PhotoHandler(FolderPath, None, None)
            handler.Analysis()
            self.AnalysButton.destroy()
            self.SortButton.destroy()
            self.report = {
                'processed': handler.MovedFiles,
                'failed': handler.BadFiles
            }
            report_text = (
                f"✔️ Будет обработано: {self.report['processed']} файлов\n"
                f"❌ Без даты: {self.report['failed']} (в \"Иные\")"
            )
            self.text = tk.Text(self, wrap="word", height=10, width=45, borderwidth=0)
            self.text.insert("1.0", report_text)
            self.text.config(state="disabled", bg=self.cget("bg"))
            self.text.pack(pady=10)
            self.OkButton = ttk.Button(text="Ok", command=lambda : self.ChangeButton("ok"))
            self.OkButton.pack(anchor="nw", pady=100)


    def SortStart(self, button):
        FolderPath = filedialog.askdirectory(title="Выберите папку с фото")
        if FolderPath:

            SortFolderPath = filedialog.askdirectory(title="Выберите папку сортировки фото")

            handler = PhotoHandler(FolderPath, SortFolderPath, button)
            handler.ProcessSort()
            self.report = {
                'processed': handler.MovedFiles,
                'failed': handler.BadFiles,
                'FoldersCreated': handler.DirsMade
            }
            self.ShowReport()
        else:
            self.destroy()

    def ShowReport(self):
        self.SaveButton.destroy()
        self.CloneButton.destroy()
        report_text = (
            f"✔️ Обработано: {self.report['processed']} файлов\n"
            f"❌ Без даты: {self.report['failed']} (в \"Иные\")\n"
            f"📁 Создано папок: {self.report['FoldersCreated']}"
        )
        if self.text:
            self.text.destroy()

        self.text = tk.Text(self, wrap="word", height=10, width=45, borderwidth=0)
        self.text.insert("1.0", report_text)
        self.text.config(state="disabled", bg=self.cget("bg"))
        self.text.pack(pady=20)

    def ChangeButton(self, button):
        if button == "sort":
            self.AnalysButton.destroy()
            self.SortButton.destroy()
            self.SaveButton = ttk.Button(text="Перенести файлы", command=lambda: self.SortStart("move"))
            self.CloneButton = ttk.Button(text="Клонировать файлы", command=lambda: self.SortStart("copy"))
            self.SaveButton.grid(column=0, row=1, sticky="nsew", padx=10)
            self.CloneButton.grid(column=1, row=1, sticky="nsew", padx=10)


# старт
if __name__ == "__main__":
    app = PhotosorterApp()
    app.mainloop()
