import subprocess
import os
import time


build_command = ['docker', 'build', '-t', 'my-py-app', '.']
start_command = ['docker', 'run', '-i', '--name', 'py-cont', 'my-py-app']

subprocess.call(build_command)
start_process = subprocess.run(start_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

#output_out = start_process.communicate()[0]
#output_err = start_process.communicate()[1]

#a = start_process.wait()

time.sleep(2)

arg = '16'

final = subprocess.run(['docker', 'exec', '-i', 'py-cont', 'python3', 'file.py'], input=arg, capture_output=True, text=True)

print(final)


'''
if a == None:
	time.sleep(0.5)
elif a == 0:
	print("it loaded!")
	raw_output = subprocess.run(['docker', 'exec', '-i', 'py-cont', 'python3', 'file.py'], capture_output=True, text=True)
	print(raw_output)



print(f"outp: {output_out.decode('UTF-8')}")
print(f"err: {output_err.decode('UTF-8')}")
'''






os.system("docker kill py-cont")
os.system("docker rm py-cont")
os.system("docker rmi my-py-app")
