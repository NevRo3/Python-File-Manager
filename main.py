import os
from tabulate import tabulate
import shutil
from distutils.dir_util import copy_tree


class FileManager:
    def __init__(self):
        with open('working_dir.txt', mode='r') as f:
            self.root_dir = fr'{f.readline()}'
        os.chdir(self.root_dir)

        self.display_data = []
        self.allowed_files = self.list_dir()[1]
        self.path_length = len(self.root_dir.split('/'))

    def far(self):
        print(f'{"-"*9}Файловый менеджер{"-"*9}')
        commands = [['0', 'Просмотр папки'], ['1', 'Создать папку'], ['2', 'Удалить папку'],
                    ['3', 'Переход между папками'], ['4', 'Подняться вверх (cd ..)'], ['5', 'Создать пустой файл'],
                    ['6', 'Запись текста в файл'], ['7', 'Просмотр txt файла'], ['8', 'Удалить файл'],
                    ['9', 'Копирование файлов'], ['10', 'Перемещение файлов'], ['11', 'Переименовать файл'],
                    ['12', 'Архив(zip) файл/папку'], ['13', 'Разархивировать файл/папку']]
        help_page = tabulate((i for i in commands), headers=['ID', 'Действие'], tablefmt='presto', stralign='left')
        print(help_page + f'\nРабочая папка: {self.root_dir}')
        while True:
            choose = str(input(
                'help - список действий, exit - выйти из файлового менеджера\nВведите ID команды чтобы продолжить: '))
            print('\n')
            if choose == '0':
                print(self.list_dir()[0])
            if choose == '1':
                self.create_dir()
            if choose == '2':
                self.delete_dir()
            if choose == '3':
                self.move_down_dir()
            if choose == '4':
                self.move_up_dir()
            if choose == '5':
                self.create_file()
            if choose == '6':
                self.write_file()
            if choose == '7':
                self.read_file()
            if choose == '8':
                self.delete_file()
            if choose == '9':
                self.copy_file()
            if choose == '10':
                self.move_file()
            if choose == '11':
                self.rename_file()
            if choose == '12':
                self.zip()
            if choose == '13':
                self.unzip()
            if choose.lower() == 'help':
                print(f'\n{help_page}')
            if choose.lower() == 'exit':
                exit()

    def refresh_dir(self):
        self.allowed_files = self.list_dir()[1]

    def list_dir(self):
        self.display_data = []
        files = os.scandir(path=self.root_dir)
        file_id = 1
        for each in files:
            object_data = f' - Dir - {each.name} - {file_id}' if each.is_dir() else f' - File - {each.name} - {file_id}'
            object_info = object_data.split(' - ')
            object_info.pop(0)
            self.display_data.append(object_info)
            file_id += 1
        data = tabulate((i for i in self.display_data), headers=['Тип', 'Имя', 'ID'], tablefmt='presto',
                        stralign='center')
        return data, self.display_data

    def choice_id(self, object_id):
        ids = [i[2] for i in self.allowed_files]
        names = [i[1] for i in self.allowed_files]
        if str(object_id) in ids:
            return names[object_id - 1]

    def create_dir(self):
        dir_name = str(input("Название новой папки: "))
        if not os.path.exists(f'{self.root_dir}/{dir_name}'):
            os.makedirs(f'{self.root_dir}/{dir_name}')
            print(f'Папка "{dir_name}" успешно создана')
            self.refresh_dir()
        else:
            print("Папка уже существует")

    def delete_dir(self):
        dir_id = int(input('Введите ID папки чтобы удалить: '))
        dir_name = self.choice_id(dir_id)
        try:
            shutil.rmtree(f'{self.root_dir}/{dir_name}')
        except OSError as e:
            print(f'Error: {e.filename} - {e.strerror}')
        else:
            print(f'Папка "{dir_name}" успешно удалена')
            self.refresh_dir()

    def move_down_dir(self):
        chosen_dir = int(input('Введите ID папки чтобы перейти в неё: '))
        location = self.choice_id(chosen_dir)
        move_path = self.root_dir + f'/{location}'
        if os.path.isdir(move_path):
            self.root_dir += f'/{location}'
            os.chdir(self.root_dir)
            self.refresh_dir()
            print(f'Успешный переход в папку {location}\nТекущий путь: {self.root_dir}')
        else:
            print(f'Попытка перехода в файл!\n{location} - файл, а не папка')

    def move_up_dir(self):
        location = self.root_dir.split('/')
        if self.path_length < len(location):
            location.pop()
            up = '/'.join(location)
            self.root_dir = up
            os.chdir(self.root_dir)
            self.refresh_dir()
            print(f'Успешный переход в папку {location[-1]}\nТекущий путь: {self.root_dir}')
        else:
            print('Ошибка доступа!\nНевозможно переместиться выше заданной корневой директории')

    def create_file(self):
        file_name = str(input("Имя файла: "))
        if not os.path.exists(f'{self.root_dir}/{file_name}'):
            new_file = open(f"{self.root_dir}/{file_name}", "w")
            new_file.close()
            print(f'Файл "{file_name}" успешно создан')
            self.refresh_dir()
        else:
            print('Файл с таким названием уже существует')

    def write_file(self):
        file_id = int(input('Введите ID файла для записи: '))
        location = self.choice_id(file_id)
        try:
            with open(f'{self.root_dir}/{location}', mode='w') as f:
                f.write(str(input('Введите текст для записи в файл: ')))
        except FileNotFoundError:
            print(f'Файл с  ID = "{file_id}" не найден')
        except IsADirectoryError:
            print('Это директория')
        else:
            print('Текст успешно записан в файл')

    def read_file(self):
        file_id = int(input('Введите ID файла чтобы прочитать: '))
        file_name = self.choice_id(file_id)
        try:
            file_location = f"{self.root_dir}/{file_name}"
            with open(file_location, "r") as f:
                text = f.read()
            for line in text.splitlines():
                print(line)
        except FileNotFoundError:
            print(f'Файл с ID = "{file_id}" не найден')

    def delete_file(self):
        file_id = int(input('Введите ID файла чтобы удалить: '))
        file_name = self.choice_id(file_id)
        try:
            os.remove(f"{self.root_dir}/{file_name}")
        except OSError as e:
            print(f'Error: {e.filename} - {e.strerror}')
        else:
            print(f'Файл "{file_name}" успешно удалён')
            self.refresh_dir()

    def copy_file(self):
        start_id = int(input('ID директории откуда копируем: '))
        start_dir = f"{self.root_dir}/{self.choice_id(start_id)}"
        end_id = int(input('ID директории куда копируем: '))
        end_dir = f"{self.root_dir}/{self.choice_id(end_id)}"
        try:
            copy_tree(start_dir, end_dir)
        except OSError as e:
            print(f'Error: {e.filename} - {e.strerror}')
        else:
            print('Успешное копирование')

    def move_file(self):
        self.list_dir()
        start_id = int(input('ID Файла для перемещения: '))
        start_location = f"{self.root_dir}/{self.choice_id(start_id)}"
        end_id = int(input('ID директории куда переместить: '))
        end_dir = f"{self.root_dir}/{self.choice_id(end_id)}"
        try:
            shutil.move(start_location, end_dir)
        except OSError as e:
            print(f'Error: {e.filename} - {e.strerror}')
        else:
            print('Успешное перемещение')
            self.refresh_dir()

    def rename_file(self):
        file_id = int(input('Введите ID файла, чтобы переименовать: '))
        file_to_rename = f"{self.root_dir}/{self.choice_id(file_id)}"
        new_name = str(input('Введите новое название файла: '))
        try:
            os.rename(file_to_rename, f'{self.root_dir}/{new_name}')
        except OSError as e:
            print(f'Error: {e.filename} - {e.strerror}')
        else:
            print('Успешное переименование')
            self.refresh_dir()

    def zip(self):
        pass

    def unzip(self):
        pass


def main():
    manager = FileManager()
    manager.far()


if __name__ == '__main__':
    main()
