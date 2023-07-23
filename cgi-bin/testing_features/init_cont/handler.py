#!/usr/bin/env python3.9

import cgi
import shutil
import os
import json
import datetime
import asyncio


DOCKERFILES_DIR_PATH = "/var/www/html/cgi-bin/references/"
SESSION_DIR_PATH = "/var/www/html/cgi-bin/sessions_tmp/"


def handle_post_request(): # Получает  исполняемый код, расширение и имя файла из пост-запроса
	form = cgi.FieldStorage()
	input_text = form.getvalue("user_text")
	current_extension = form.getvalue("progr_lang")
	sessionID = form.getvalue("sessionID")
	FULLNAME = form.getvalue("file_name")
	dot_index = FULLNAME.rfind(".")
	file_name = FULLNAME[:dot_index]
	return input_text, current_extension, sessionID, FULLNAME, file_name


if os.environ['REQUEST_METHOD'] == 'POST': # Запускает обработку запроса
	input_text, current_extension, sessionID, FULLNAME, file_name = handle_post_request()


tmp_name = sessionID + current_extension
tmp_dir_path = f'{SESSION_DIR_PATH}{tmp_name}'

def fill_tmp_dir(tmp_dir_path, input_text, current_extension): # Помещает в tmp_dir файл с кодом и Dockerfile
	tmp_input_file_path = f'{tmp_dir_path}/main.{current_extension}'
	with open (tmp_input_file_path, 'w') as temporal:
		temporal.write(input_text)


def open_container(tmp_name, tmp_dir_path, current_extension): # Собирает образ и запускаем контейнер
	cmd_cp_file = f'docker cp {tmp_dir_path}/main.{current_extension} {tmp_name}:/home/main.py'
	os.system(cmd_cp_file)
	cmd_open_cont = f'docker start -a {tmp_name} > {tmp_dir_path}/output.txt 2>&1'
	os.system(cmd_open_cont)


def cleanup(tmp_name): # Чистка
	os.system('docker rmi $(docker images -f "dangling=true" -q) && docker container prune')
	cmd_delete_image = f'docker rmi {tmp_name}'
	os.system(cmd_delete_image)


def send_output(tmp_dir_path): # Возвращет содержимое output.txt на сайт
	with open(f'{tmp_dir_path}/output.txt', 'r') as output:
		processed_text = output.read()
	
	print("Content-type: application/json\n")
	print(json.dumps({'text': processed_text}))


def main():
	try:
		os.mkdir(tmp_dir_path)
	except FileExistsError:
		pass
	
	fill_tmp_dir(tmp_dir_path, input_text, current_extension)
	open_container(tmp_name, tmp_dir_path, current_extension)
	cleanup(tmp_name)
	send_output(tmp_dir_path)


if __name__ == '__main__':
	main()


