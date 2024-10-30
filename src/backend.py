from tkinter import messagebox
from typing import List
import os
import re
import datetime
import shutil


class ProgramControl:

    def __init__(self):
        self.prefetch_dir = os.path.join(os.environ.get('WINDIR'), 'Prefetch')
        os.makedirs("data", exist_ok=True)

    @staticmethod
    def load_program_list(file_path: str) -> List[str]:
        try:
            with open(file_path, 'r') as file:
                program_list = [line.strip().upper()
                                for line in file if line.strip().endswith(".EXE") or line.strip().endswith(".exe")]
                if not program_list:
                    messagebox.showerror("Ошибка", "Список программ пуст.")
                    return []

            return program_list
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить список программ:\n{e}")
            return []

    @staticmethod
    def get_services_set(directory: str) -> set:
        try:

            services_set = set()

            for filename in os.listdir(directory):

                if os.path.isfile(os.path.join(directory, filename)):
                    match = re.match(r"^([A-Za-z0-9_.]+)-[A-Za-z0-9]+\.pf$", filename)
                    if match:
                        services_set.add(match.group(1))
            return services_set
        except FileNotFoundError:
            raise FileNotFoundError("Указанная директория не найдена.")
        except PermissionError:
            raise PermissionError("Нет доступа к указанной директории. Запустите от имени администратора")

    def check_program(self,check_type: str, file_path: str):
        prefetch_dir_path = self.prefetch_dir
        program_set = set(self.load_program_list(file_path=file_path))
        prefetch_files_set = self.get_services_set(directory=prefetch_dir_path)

        result_set = (program_set & prefetch_files_set) if check_type == 'b' \
            else (prefetch_files_set - program_set) if check_type == 'w' \
            else set()

        status = not bool(result_set)
        return result_set, status

    def create_result_table(self, result: set):

        formatted_lines = []

        for filename in os.listdir(self.prefetch_dir):
            file_path = os.path.join(self.prefetch_dir, filename)

            if os.path.isfile(file_path) and '.EXE' in filename:
                mod_time = os.path.getmtime(file_path)
                mod_time_readable = datetime.datetime.fromtimestamp(mod_time)

                if any(service in filename for service in result):
                    formatted_line = f"<b>{filename} | {mod_time_readable.strftime('%Y-%m-%d %H:%M:%S')}</b><br>"
                else:
                    formatted_line = f"{filename} | {mod_time_readable.strftime('%Y-%m-%d %H:%M:%S')}<br>"

                formatted_lines.append(formatted_line)

                formatted_lines.sort(key=lambda x: x.replace('<b>', '').strip().split(' | ')[0])

                output_file_path = 'data/result_table_with_bold_tags.txt'
                with open(output_file_path, 'w') as file:
                    for line in formatted_lines:
                        name, date = line.split(' | ')
                        formatted_line = f"{name:<100} | {date}"
                        file.write(formatted_line + '\n')

                html_file_path = output_file_path.replace(".txt", ".html")

                # Копируем файл
                shutil.copy(output_file_path, html_file_path)
        return formatted_lines
