import re
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

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

    def display_table(self, items, status):
        # Создаем окно для отображения таблицы
        viewer_window = tk.Toplevel(self.root)
        viewer_window.title(f"Результаты проверки : {status}")

        # Настраиваем цвет заголовка в зависимости от статуса
        header_text = "Проверка завершена: ПО Соответствует" if status else "Проверка завершена: ПО Несоответствует"
        header_color = "green" if status else "red"

        # Создаем статическую метку для заголовка, чтобы он не прокручивался
        header_label = tk.Label(viewer_window, text=header_text, font=("Helvetica", 16, "bold"), fg=header_color)
        header_label.pack(pady=(10, 5))  # Верхний отступ для отделения от края окна

        # Создаем текстовый виджет с прокруткой для таблицы
        text_area = scrolledtext.ScrolledText(viewer_window, wrap=tk.WORD, width=80, height=30)
        text_area.pack(padx=10, pady=10)

        # Устанавливаем шрифт для таблицы и жирный стиль
        text_area_font = ("Courier", 12)
        text_area.tag_configure("bold", font=("Courier", 12, "bold"))
        text_area.configure(font=text_area_font)

        # Заголовки таблицы
        table_content = f"{'Программа':<40} | {'Дата':<20}\n" + "-" * 65 + "\n"
        text_area.insert(tk.END, table_content, "bold")

        # Обрабатываем и отображаем элементы списка
        for item in items:
            item = re.sub(r'<br>$', '', item)
            if item.startswith('<b>') and item.endswith('</b>'):
                clean_item = item[3:-4]
                program, date = clean_item.split(" | ")
                line = f"{program:<40} | {date:<20}\n"
                text_area.insert(tk.END, line, "bold")
            else:
                program, date = item.split(" | ")
                line = f"{program:<40} | {date:<20}\n"
                text_area.insert(tk.END, line)
            table_content += line

        # Делаем текстовое поле только для чтения
        text_area.configure(state='disabled')

        # Запись итогового содержимого таблицы в файл
        with open("data/result_table.txt", "w", encoding="utf-8") as file:
            file.write(table_content)

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

        if not file_path:
            messagebox.showerror("Ошибка", "Пожалуйста, выберите файл.")
            return
        elif not check_type:
            messagebox.showerror("Ошибка", "Пожалуйста, выберите тип проверки.")
            return

        control = ProgramControl()
        results, status = control.check_program(
            check_type=check_type,
            file_path=file_path
        )

        result_table = control.create_result_table(results)

        self.display_table(result_table, status)


