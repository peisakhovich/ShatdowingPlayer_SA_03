import tkinter as tk
from tkinter import filedialog


class FileDialog:

    @staticmethod
    def open_file(
        title="Выберите файл",
        filetypes=None,
        initial_dir=None
    ):
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)

        try:
            return filedialog.askopenfilename(
                parent=root,
                title=title,
                initialdir=initial_dir,
                filetypes=filetypes or [
                    ("Все файлы", "*.*")
                ]
            )
        finally:
            root.destroy()

    @staticmethod
    def save_file(
        title="Сохранить файл",
        filetypes=None,
        initial_dir=None,
        initial_file=None
    ):
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)

        try:
            return filedialog.asksaveasfilename(
                parent=root,
                title=title,
                initialdir=initial_dir,
                initialfile=initial_file,
                filetypes=filetypes or [
                    ("Все файлы", "*.*")
                ]
            )
        finally:
            root.destroy()