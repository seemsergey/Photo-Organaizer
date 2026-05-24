import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from mediaHandler import MediaHandler


class UniversalSorterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Сортировщик Медиа")
        self.geometry("400x250")

        # Переменные для галочек
        self.use_photo = tk.BooleanVar(value=True)
        self.use_video = tk.BooleanVar(value=True)

        self.create_widgets()

    def create_widgets(self):
        # Очистка окна
        for widget in self.winfo_children():
            widget.destroy()

        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(expand=True, fill="both")

        ttk.Label(main_frame, text="Что сортируем?", font=("Arial", 12, "bold")).pack(pady=5)

        # Чекбоксы
        ttk.Checkbutton(main_frame, text="Фотографии", variable=self.use_photo).pack(anchor="w")
        ttk.Checkbutton(main_frame, text="Видеофайлы", variable=self.use_video).pack(anchor="w")

        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=20)

        self.btn_analys = ttk.Button(btn_frame, text="Анализ", command=self.start_analysis)
        self.btn_analys.grid(row=0, column=0, padx=5)

        self.btn_sort = ttk.Button(btn_frame, text="Сортировка", command=self.show_sort_options)
        self.btn_sort.grid(row=0, column=1, padx=5)

    def start_analysis(self):
        if not (self.use_photo.get() or self.use_video.get()):
            messagebox.showwarning("Внимание", "Выберите хотя бы один тип файлов!")
            return

        path = filedialog.askdirectory(title="Выберите папку для анализа")
        if path:
            handler = MediaHandler(path, None, None, self.use_photo.get(), self.use_video.get())
            handler.process(is_analysis=True)

            res_text = (f"Найдено файлов: {handler.count_ok + handler.count_bad}\n"
                        f"С датой: {handler.count_ok}\n"
                        f"Без даты: {handler.count_bad}")
            messagebox.showinfo("Результат анализа", res_text)

    def show_sort_options(self):
        if not (self.use_photo.get() or self.use_video.get()):
            messagebox.showwarning("Внимание", "Выберите хотя бы один тип файлов!")
            return

        self.btn_analys.destroy()
        self.btn_sort.destroy()

        ttk.Label(text="Выберите действие:").pack()
        ttk.Button(text="Копировать файлы", command=lambda: self.run_sort("copy")).pack(pady=5)
        ttk.Button(text="Перенести (вырезать)", command=lambda: self.run_sort("move")).pack(pady=5)
        ttk.Button(text="Назад", command=self.create_widgets).pack(pady=5)

    def run_sort(self, mode):
        src = filedialog.askdirectory(title="Откуда брать файлы?")
        if not src: return
        dst = filedialog.askdirectory(title="Куда складывать?")
        if not dst: return

        handler = MediaHandler(src, dst, mode, self.use_photo.get(), self.use_video.get())
        handler.process(is_analysis=False)

        messagebox.showinfo("Готово", f"Успешно обработано: {handler.count_ok}\nВ 'Неизвестные': {handler.count_bad}")
        self.create_widgets()


if __name__ == "__main__":
    app = UniversalSorterApp()
    app.mainloop()