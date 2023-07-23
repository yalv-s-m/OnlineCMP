#!/usr/bin/env python3.9

import cgi
import shutil
import os
import json
import datetime
import asyncio

async def main():
        #Генерируем хэш для имени папки
        time_str = datetime.datetime.now().strftime('%m-%d_%H-%M-%S-%f')[:-3]
        hash_str = hex(hash(time_str))[2:12]

        #Получаем расширение и входной код из POST запроса
        form = cgi.FieldStorage()
        current_extension = form.getvalue("progr_lang")
        #current_extension = value_extension.split(".", 1)[-1] #Нужно, если lang_menu.value содержит точку перед расширением
        input_text = form.getvalue("user_text")
        FULLNAME = form.getvalue("file_name")
        dot_index = FULLNAME.rfind(".")
        file_name = FULLNAME[:dot_index]

        #Создаем временную папку для хранения input., Dockerfile и output.txt
        tmp_folder_name = f'{time_str}_{hash_str}{current_extension}'
        tmp_dir_path = f'/var/www/html/cgi-bin/sessions_tmp/{tmp_folder_name}'
        os.mkdir(tmp_dir_path)
        tmp_input_file_path = f'{tmp_dir_path}/{file_name}.{current_extension}'

        #Записываем входной код во временную папку в файл input.
        with open(tmp_input_file_path, 'w') as temporal:
                temporal.write(input_text)

        #Перемещаем нужный Dockerfile во временную папку
        path_to_Dockerfile = f'/var/www/html/cgi-bin/references/{current_extension}_app/Dockerfile'
        shutil.copy2(path_to_Dockerfile, tmp_dir_path)
        os.chdir(tmp_dir_path)

        #Запускаем сборку и выполнение контейнера
        create_cont = f'docker build -t {hash_str}{current_extension} --build-arg FILENAME={FULLNAME} .'
        open_cont = f'docker run --rm --env FILENAME={FULLNAME} {hash_str}{current_extension} > output.txt 2>&1'
        os.system(create_cont)
        os.system(open_cont)

        # Чистка
        os.system('docker rmi $(docker images -f "dangling=true" -q)')
        del_image = f'docker rmi {hash_str}{current_extension}'
        os.system(del_image)

        with open('output.txt', 'r') as file:
                processed_text = file.read()

        print("Content-type: application/json\n")
        print(json.dumps({'text': processed_text}))


if __name__ == '__main__':
        asyncio.run(main())
