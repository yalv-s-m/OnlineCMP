#!/usr/bin/env python3.9

from os import environ
from json import load, dumps
from datetime import datetime
from subprocess import run, DEVNULL
from prepare_data import handle_post_request, generate_tmp_name, create_tmp_dir, fill_tmp_dir, check_whether_compilable


if environ['REQUEST_METHOD'] == 'POST':
        input_text, current_extension = handle_post_request()


# starts a detached container in interactive mode using a prebuild image, depending on the file extension
# then copies source code file inside cont's "/home" dir
def start_cont_cp_file(current_extension, tmp_name, tmp_dir_path):
        start_cont = ['docker', 'run', '-d', '-i', '--name', '{}'.format(tmp_name), 'prebuild-{}'.format(current_extension)]
	
        file_host_path = f'{tmp_dir_path}/main.{current_extension}'
        file_cont_path = f'{tmp_name}:/home/main.{current_extension}'
        copy_file = ['docker', 'cp', '{}'.format(file_host_path), '{}'.format(file_cont_path)]
        
        start_cont_result = run(start_cont, capture_output=True, text=True)
        copy_file_result = run(copy_file, capture_output=True, text=True)
        with open('logs/cont.log', 'a') as file:
                file.write(f'\nStart: {datetime.now()}\n{start_cont_result}\n{copy_file_result}\nEnd\n')



# returns 2 arrays
# each "case" in "test_cases" will be used as input to a program
# each "output" of a program will be compared to a "result" in "expected results"
def read_tests():
        with open('tests-config.json', 'r') as file:
                data = load(file)

        test_cases = data['test_cases']
        expected_results = data['expected_results']
        return test_cases, expected_results


def read_lang_commands():
        with open('lang-commands.json', 'r') as file:
                command_dict = load(file)
        return command_dict


# this array will determine, which child div's inside "<div class="UNIX-output...>" will be painted red
# it is used in "updateUnixOutput()" in "scripts.js"
indexes_of_failed_cases = []



# 'c' and 'cpp' langs require two commands to run, 
# compile command and "/home/a.out". More about it is in "preapre_no_img.check_whether_compilable()".

# If compilation fails, then compiler errors will be written into output.txt, 
# and "indexes_of_failed_cases" will include all number of cases.
# If it succeeds, then "do_tests()"

# For langs, which require only one command to run, just "do_tests()"
def form_results(current_extension, tmp_name, tmp_dir_path, number_of_cases, test_cases, expected_results, command_dict):
        if current_extension == 'c' or current_extension == 'cpp':
                is_compilable, build_errors = check_whether_compilable(current_extension, tmp_name, command_dict)
                if is_compilable:
                        indexes_of_failed_cases = do_tests(tmp_name, tmp_dir_path, test_cases, expected_results, command_dict)
                else:
                        error_output = f'{build_errors}%%%' * number_of_cases
                        with open(f'{tmp_dir_path}/output.txt', 'w') as f:
                                f.write(error_output)
                        indexes_of_failed_cases = list(range(number_of_cases))
        else:
                indexes_of_failed_cases = do_tests(tmp_name, tmp_dir_path, test_cases, expected_results, command_dict)
        return indexes_of_failed_cases


# loops through "tests_cases",
# casts each "case" to string,
# and uses them as input to a container.

# "formatted_output" is either program's output, or interpreter/compiler error
def do_tests(tmp_name, tmp_dir_path, test_cases, expected_results, command_dict):
        final_output = ''
        i = -1
        exec_command = ['docker', 'exec', '-i', '{}'.format(tmp_name)] + command_dict.get(current_extension, [])
        for case in test_cases:
                i += 1
                arg = str(case)
                raw_output = run(exec_command,
                                        input=arg,
                                        capture_output=True,
                                        text=True)
                formatted_output = raw_output.stdout.strip() if raw_output.stdout else raw_output.stderr.strip()
                if str(formatted_output) != str(expected_results[i]):
                        indexes_of_failed_cases.append(i)
                final_output += f'Case: {arg}; Got result: {formatted_output}%%%'
        with open(f'{tmp_dir_path}/output.txt', 'w') as f:
                f.write(final_output)
        return indexes_of_failed_cases


def cleanup(command):
        run(command, stdout=DEVNULL, stderr=DEVNULL)


# "results" will be split into "listOfCases" in "sendData()" in "scripts.js",
# each line will be used as "textContent" for child div's in "<div class=UNIX-output...>" in "updateUnixOutput()"

# "number_of_cases" determines amount of child div's
def send_results(tmp_dir_path, test_cases, number_of_cases, indexes_of_failed_cases):
        with open(f'{tmp_dir_path}/output.txt', 'r') as file:
                results = file.read()
        data = {
                'text': results,
                'number_of_cases': number_of_cases,
                'indexes_of_failed_cases': indexes_of_failed_cases
        }
        print("Content-type: application/json\n")
        print(dumps(data))


def main():
        test_cases, expected_results = read_tests()
        number_of_cases = len(test_cases)
        command_dict = read_lang_commands()
        tmp_name = generate_tmp_name(current_extension)
        tmp_dir_path = create_tmp_dir(tmp_name)
        fill_tmp_dir(tmp_dir_path, input_text, current_extension)
        start_cont_cp_file(current_extension, tmp_name, tmp_dir_path)
        try:
                indexes_of_failed_cases = form_results(current_extension, tmp_name, tmp_dir_path, number_of_cases, test_cases, expected_results, command_dict)
        finally:
                cleanup(['docker', 'kill', '{}'.format(tmp_name)])
                cleanup(['docker', 'rm', '{}'.format(tmp_name)])
                cleanup(['docker', 'rmi', '{}'.format(tmp_name)])
        send_results(tmp_dir_path, test_cases, number_of_cases, indexes_of_failed_cases)


if __name__ == '__main__':
        main()
