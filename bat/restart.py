import os
import glob
import shutil
import re
import subprocess



def main():

    # initializing the count
    deleted_files_count = 0

    # specify the path
    path = os.getcwd()

    # checking whether the file is present in path or not
    if os.path.exists(path):

        # iterating over each and every folder and file in the path
        # for base.sqlite3, root, files in glob(path):

        files = glob.glob(path + '/**/*.py', recursive=True)
        base = glob.glob(path + '/**/*.sqlite3', recursive=True)
        for file in base:
            remove_file(file)
            deleted_files_count += 1 # incrementing count


                # checking the current directory files
        for file in files:
            # comparing the days
            if re.findall(r'\d{4}_', file):
                if not re.findall(r'venv', file):
                    # invoking the remove_file function
                    remove_file(file)
                    deleted_files_count += 1 # incrementing count
    print(f"Total files deleted: {deleted_files_count}")

    os.startfile(path+'\\bat\mmigr.bat')
    input('Правила миграций настроены. Нажмите Enter')
    os.startfile(path+'\\bat\migr.bat')
    input('Миграции провели. Нажмите Enter')
    os.startfile(path+'\\bat\\user.bat')
    input('Суперпользователя создали. Нажмите Enter')
    os.startfile(path+'\\bat\mmigr.bat')
    input('Правила миграций настроены. Нажмите Enter')
    os.startfile(path+'\\bat\migr.bat')
    input('Миграции провели. Нажмите Enter')
    os.startfile(path+'\\bat\hubs.bat')
    input('Хабы созданы. Нажмите Enter')
    os.startfile(path+'\\bat\\article.bat')
    input('Сатьи созданы. Нажмите Enter')
    os.startfile(path+'\\bat\draft.bat')
    input('Черновики созданы. Нажмите Enter')
    os.startfile(path+'\\bat\moderat.bat')
    input('Статьи на модерации. Нажмите Enter')
    os.startfile(path+'\\bat\public.bat')
    input('Статьи на публикации. Нажмите Enter')

def remove_file(path):
    # removing the file
    if not os.remove(path):
        # success message
        print(f"{path} is removed successfully")
    else:
        # failure message
        print(f"Unable to delete the {path}")



if __name__ == '__main__':
    main()