import os

os.system("docker kill py-cont")
os.system("docker rm py-cont")
os.system("docker rmi my-py-app")
