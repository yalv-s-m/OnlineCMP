import datetime
from os import mkdir
from shutil import copy2
from cgi import FieldStorage
from subprocess import run

SESSION_DIR_PATH = "/var/www/html/cgi-bin/sessions_tmp/"

# gets source code and lang extension
def handle_post_request():
        form = FieldStorage()
        input_text = form.getvalue("user_text")
        current_extension = form.getvalue("progr_lang")
        return input_text, current_extension



# this "tmp_name" will be used as a name for sub_tmp_dir inside SESSION_DIR_PATH,
# and as a name for a container
def generate_tmp_name(current_extension):
        time_str = datetime.datetime.now().strftime('%m-%d_%H-%M-%S-%f')[:-3]
        hash_str = hex(hash(time_str))[2:12]
        return f'{time_str}_{hash_str}{current_extension}'


def create_tmp_dir(tmp_name):
        tmp_dir_path = f'{SESSION_DIR_PATH}{tmp_name}'
        mkdir(tmp_dir_path)
        return tmp_dir_path


def fill_tmp_dir(tmp_dir_path, input_text, current_extension): # Помещает в tmp_dir файл с кодом и Dockerfile
        tmp_input_file_path = f'{tmp_dir_path}/main.{current_extension}'
        with open (tmp_input_file_path, 'w') as temporal:
                temporal.write(input_text)



def check_whether_compilable(current_extension, tmp_name, command_dict):
        compile_command = ['docker', 'exec', '-i', '{}'.format(tmp_name)] + command_dict.get('{}-compile'.format(current_extension), [])
        compile_output = run(compile_command,
                                        capture_output=True,
                                        text=True)
        returncode = compile_output.returncode
        build_errors = compile_output.stderr
        compilable = str(returncode) == '0'
        return compilable, build_errors
