import os
import subprocess

os.system("docker build -t my-py-app .")

args = [3, 8, 51]
formatted = ''

for case in args:
	arg = str(case)
	outp = subprocess.run(['docker', 'run', '-i', '--name', 'py-cont', 'my-py-app', '&&', 'docker', 'exec', '-i', 'py-cont', 'python3', 'file.py'], input=arg, capture_output=True, text=True)
	formatted += outp.stdout.strip()

print(formatted)

os.system("docker kill py-cont")
os.system("docker rm py-cont")
os.system("docker rmi my-py-app")
