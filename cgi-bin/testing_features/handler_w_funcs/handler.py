
import cgi
import shutil
import os
import json
import datetime
import asyncio

DOCKERFILES_DIR_PATH = "/var/www/html/cgi-bin/references/"
SESSION_DIR_PATH = "/var/www/html/cgi-bin/testing_features/handler_w_funcs/sessions_tmp/"

input_text = "print('hahahaha')"
current_extension = "py"
FULLNAME = "main.py"
file_name = "main"

def tmp_name(current_extension):
        time_str = datetime.datetime.now().strftime('%m-%d_%H-%M-%S-%f')[:-3]
        hash_str = hex(hash(time_str))[2:12]
        return f'{time_str}_{hash_str}{current_extension}'

tmp_name = tmp_name(current_extension)

def create_tmp_dir(tmp_name):
        tmp_dir_path = f'{SESSION_DIR_PATH}{tmp_name}'
        os.mkdir(tmp_dir_path)
        return tmp_dir_path

def fill_tmp_dir(tmp_dir_path, input_text, current_extension, file_name):
	tmp_input_file_path = f'{tmp_dir_path}/{file_name}.{current_extension}'
	with open (tmp_input_file_path, 'w') as temporal:
		temporal.write(input_text)

	path_to_Dockerfile = f'{DOCKERFILES_DIR_PATH}{current_extension}_app/Dockerfile'
	shutil.copy2(path_to_Dockerfile, tmp_dir_path)

def build_and_open_container(tmp_name, FULLNAME):
	cmd_build_cont = f'docker build -t {tmp_name} --build-arg FILENAME={FULLNAME} .'
	cmd_open_cont = f'docker run --rm --env FILENAME={FULLNAME} {tmp_name} > output.txt 2>&1'
	os.system(cmd_build_cont)
	os.system(cmd_open_cont)

def cleanup(tmp_name):
	os.system('docker rmi $(docker images -f "dangling=true" -q)')
	cmd_delete_image = f'docker rmi {tmp_name}'
	os.system(cmd_delete_image)

def main():
	tmp_dir_path = create_tmp_dir(tmp_name)
	fill_tmp_dir(tmp_dir_path, input_text, current_extension, file_name)
	os.chdir(tmp_dir_path)
	build_and_open_container(tmp_name, FULLNAME)
	cleanup(tmp_name)

if __name__ == '__main__':
	main()

'''
async def main():
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
'''
