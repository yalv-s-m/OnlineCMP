import subprocess
import os
from time import sleep

extension = 'swift'


build_command = ['docker', 'build', '-t', 'my-{}-app'.format(extension), './apps/{}_app'.format(extension)]
start_command = ['docker', 'run', '-i', '--name', '{}-cont'.format(extension), 'my-{}-app'.format(extension)]

subprocess.call(build_command)
start_process = subprocess.Popen(start_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


test_cases = [0, -1, 1, -15, 6, 11, 42]


py_command = ['python3', 'file.py']
c_command = ['./a.out']
swift_command = ['swift', 'main.swift']


command_dict = {
	'py': py_command,
	'c': c_command,
	'swift': swift_command,
}

exec_command = ['docker', 'exec', '-i', '{}-cont'.format(extension)] + command_dict.get(extension, [])




final_output = ''
formatted1 = None
placeholder_input = '1'

try:
	# just checks each 0.2 sec whether the container is launched and available
	# note that tested program's actual output should never be None, otherwise it'll be an infinite loop
	while formatted1 == None:
		sleep(0.2)
		raw1 = subprocess.run(exec_command, 
					input=placeholder_input, 
					capture_output=True, 
					text=True)
		formatted1 = raw1.stdout.strip()
	else:
		for case in test_cases:
			arg = str(case)
			raw_output = subprocess.run(exec_command, 
							input=arg, 
							capture_output=True, 
							text=True)
			formatted_output = raw_output.stdout.strip() if raw_output.stdout else raw_output.stderr.strip()
			final_output += f'Case: {arg}; Got result: {formatted_output} \n'
	print(final_output)

finally:
	os.system(f'docker kill {extension}-cont')
	os.system(f'docker rm {extension}-cont')
	os.system(f'docker rmi my-{extension}-app')
