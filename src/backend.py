from tkinter import messagebox
from typing import List, Dict
import os
import re


class ProgramControl:
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
            print("Указанная директория не найдена.")
            return set()
        except PermissionError:
            print("Нет доступа к указанной директории.")
            return set()

    def check_program(self, prefetch_dir_path: str, check_type: str, file_path: str):
        program_set = set(self.load_program_list(file_path=file_path))
        prefetch_files_set = self.get_services_set(directory=prefetch_dir_path)

        print(program_set)
        print(prefetch_files_set)

        result_set = (program_set & prefetch_files_set) if check_type == 'b' \
            else (prefetch_files_set - program_set) if check_type == 'w' \
            else set()

        status = not bool(result_set)
        return result_set, status






