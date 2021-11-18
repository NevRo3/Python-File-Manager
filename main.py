import os
from tabulate import tabulate
import shutil


class FileManager:
    def __init__(self):
        with open('working_dir.txt', mode='r') as f:
            self.root_dir = fr'{f.readline()}'
        os.chdir(self.root_dir)

        self.display_data = []
        self.allowed_files = self.list_dir()[1]

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
                self.move_between_dir()
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

    def move_between_dir(self):
        pass

    def move_up_dir(self):
        pass

    def create_file(self):
        pass

    def write_file(self):
        pass

    def read_file(self):
        pass

    def delete_file(self):
        pass

    def copy_file(self):
        pass

    def move_file(self):
        pass

    def rename_file(self):
        pass

    def zip(self):
        pass

    def unzip(self):
        pass


def main():
    manager = FileManager()
    manager.far()


if __name__ == '__main__':
    main()
