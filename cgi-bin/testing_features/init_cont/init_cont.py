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
	current_extension = form.getvalue("progr_lang")
	sessionID = form.getvalue("sessionID")
	FULLNAME = form.getvalue("file_name")
	dot_index = FULLNAME.rfind(".")
	file_name = FULLNAME[:dot_index]
	return current_extension, sessionID, FULLNAME, file_name


if os.environ['REQUEST_METHOD'] == 'POST': # Запускает обработку запроса
	current_extension, sessionID, FULLNAME, file_name = handle_post_request()

tmp_name = sessionID + current_extension
tmp_dir_path = f'{SESSION_DIR_PATH}{tmp_name}'

def fill_placeholders(tmp_dir_path, current_extension):
	path_to_Dockerfile = f'{DOCKERFILES_DIR_PATH}{current_extension}_app/Dockerfile'
	shutil.copy2(path_to_Dockerfile, tmp_dir_path)
	placeholder_path = f'{tmp_dir_path}/{file_name}.{current_extension}'
	file = open(placeholder_path, 'w')
	file.close()

def init_cont(tmp_name, tmp_dir_path): # Собирает образ и запускаем контейнер
	cmd_build_cont = f'docker build -t {tmp_name} --build-arg FILENAME={FULLNAME} {tmp_dir_path}'
	os.system(cmd_build_cont)
	cmd_cr_cont = f'docker create --name {tmp_name} {tmp_name}'
	os.system(cmd_cr_cont)

def main():
	try:
		os.mkdir(tmp_dir_path)
	except FileExistsError:
		pass

	fill_placeholders(tmp_dir_path, current_extension)
	init_cont(tmp_name, tmp_dir_path)
	print("Content-Type: text/plain")
	print()


if __name__ == '__main__':
	main()

