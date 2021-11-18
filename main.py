import os


class FileManager:
    def __init__(self):
        with open('working_dir.txt', mode='r') as f:
            self.root_dir = fr'{f.readline()}'
        os.chdir(self.root_dir)

    def far(self):
        pass

    def refresh_dir(self):
        pass

    def list_dir(self):
        pass

    def choice_id(self):
        pass

    def create_dir(self):
        pass

    def delete_fir(self):
        pass

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
