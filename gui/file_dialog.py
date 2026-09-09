"""
Sound Language Studio
---------------------

Module:
    gui.file_dialog

Purpose:
    Provides simple file open and save dialogs for the application.

ru:
    Предоставляет простые диалоги открытия и сохранения файлов
    для приложения.
"""
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
        initial_file=None,
        defaultextension=None,

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
                defaultextension=defaultextension,
                filetypes=filetypes or [
                    ("Все файлы", "*.*")
                ]
            )
        finally:
            root.destroy()