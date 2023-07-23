#!/usr/bin/env python3.9

import cgi
import shutil
import os
import json
import asyncio
import subprocess
from prepare_no_img import handle_post_request, generate_tmp_name, create_tmp_dir, fill_tmp_dir, check_whether_compilable


DOCKERFILES_DIR_PATH = '/var/www/html/cgi-bin/references/dockerfiles/'

if os.environ['REQUEST_METHOD'] == 'POST': # Запускает обработку запроса
	input_text, current_extension = handle_post_request()

def read_lang_commands():
        with open('lang-commands.json', 'r') as file:
                command_dict = json.load(file)
        return command_dict


def build_and_open_container(current_extension, tmp_name, tmp_dir_path, command_dict): # Собирает образ и запускаем контейнер
        cmd_open_cont = f'docker run -d -i --name {tmp_name} prebuild-{current_extension} > /dev/null'
        cmd_copy_file = f'docker cp {tmp_dir_path}/main.{current_extension} {tmp_name}:/home/main.{current_extension} > /dev/null'
        lang_command = command_dict.get('current_extension', [])
        exec_command = ['docker', 'exec', '-i', '{}'.format(tmp_name)] + command_dict.get(current_extension, [])
        os.system(cmd_open_cont)
        os.system(cmd_copy_file)
        if current_extension == 'c' or current_extension == 'cpp':
                is_compilable, build_errors = check_whether_compilable(current_extension, tmp_name, command_dict)
                if is_compilable:
                        launch_program(current_extension, tmp_name, tmp_dir_path, command_dict)
                else:
                        with open(f'{tmp_dir_path}/output.txt', 'w') as file:
                                file.write(build_errors)
        else:
                launch_program(current_extension, tmp_name, tmp_dir_path, command_dict)


def launch_program(current_extension, tmp_name, tmp_dir_path, command_dict):
        exec_command = ['docker', 'exec', '-i', '{}'.format(tmp_name)] + command_dict.get(current_extension, [])
        raw_output = subprocess.run(exec_command, capture_output=True, text=True)
        formatted_output =  raw_output.stdout.strip() if raw_output.stdout else raw_output.stderr.strip()
        with open(f'{tmp_dir_path}/output.txt', 'w') as file:
                file.write(formatted_output)


def cleanup(tmp_name): # Чистка
        os.system(f'docker kill {tmp_name} > /dev/null')
        os.system(f'docker rm {tmp_name} > /dev/null')
        #os.system('docker image prune -a -y')



def send_output(tmp_dir_path): # Возвращет содержимое output.txt на сайт
        with open(f'{tmp_dir_path}/output.txt', 'r') as output:
                processed_text = output.read()

        print("Content-type: application/json\n")
        print(json.dumps({'text': processed_text}))


def main():
        tmp_name = generate_tmp_name(current_extension)
        tmp_dir_path = create_tmp_dir(tmp_name)
        fill_tmp_dir(tmp_dir_path, input_text, current_extension)
        command_dict = read_lang_commands()
        try:
                build_and_open_container(current_extension, tmp_name, tmp_dir_path, command_dict)
        finally:
                cleanup(tmp_name)
        send_output(tmp_dir_path)


if __name__ == '__main__':
        main()
