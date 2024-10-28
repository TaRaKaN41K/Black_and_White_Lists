import tkinter as tk
from tkinter import filedialog, messagebox

from backend import ProgramControl


class UI:
    def __init__(self, root):
        self.root = root
        self.root.title("Контроль запуска ПО")

        self.frame = tk.Frame(root, padx=10, pady=10)
        self.frame.pack()

        self.entry_file = None
        self.var_check_type = None

        self.setup_ui()

    def setup_ui(self):
        label_file = tk.Label(self.frame, text="Файл со списком программ:")
        label_file.grid(row=0, column=0, sticky="e")

        self.entry_file = tk.Entry(self.frame, width=40)
        self.entry_file.grid(row=0, column=1)

        button_browse = tk.Button(self.frame, text="Обзор", command=self.select_file)
        button_browse.grid(row=0, column=2)

        label_check_type = tk.Label(self.frame, text="Тип проверки:")
        label_check_type.grid(row=1, column=0, sticky="e")

        self.var_check_type = tk.StringVar()

        radio_white = tk.Radiobutton(self.frame,
                                     text="Белый список",
                                     variable=self.var_check_type,
                                     value="w"
                                     )
        radio_white.grid(row=1, column=1, sticky="w")

        radio_black = tk.Radiobutton(self.frame,
                                     text="Черный список",
                                     variable=self.var_check_type,
                                     value="b"
                                     )
        radio_black.grid(row=2, column=1, sticky="w")

        button_check = tk.Button(self.frame, text="Проверить", command=self.run_check)
        button_check.grid(row=3, column=1)

    def select_file(self):
        file_path = filedialog.askopenfilename(title="Выберите файл со списком программ")
        if file_path:
            self.entry_file.delete(0, tk.END)
            self.entry_file.insert(0, file_path)

    def run_check(self):

        file_path = self.entry_file.get()
        check_type = self.var_check_type.get()

        print(check_type)

        if not file_path:
            messagebox.showerror("Ошибка", "Пожалуйста, выберите файл.")
            return
        elif not check_type:
            messagebox.showerror("Ошибка", "Пожалуйста, выберите тип проверки.")
            return

        control = ProgramControl()
        results, status = control.check_program(
            prefetch_dir_path='/Users/feodorkalasov/PTStart/INT-3/Prefetch',
            check_type=check_type,
            file_path=file_path
        )
        print(results)
        messagebox.showinfo("Результат проверки", f"Статус проверки: {status}")
