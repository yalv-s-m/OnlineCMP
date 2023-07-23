import json



'''
command_dict = {
        'py': ['python3', '/home/main.py'],
        'js': ['node', '/home/main.js'],
        'c-compile': ['gcc', '/home/main.c', '-o', '/home/a.out'],
        'c': ['/home/a.out'],
        'cpp-compile': ['g++', '/home/main.cpp', '-o', '/home/a.out'],
        'cpp': ['/home/a.out'],
        'dart': ['dart', '/home/main.dart'],
        'go': ['go', 'run', '/home/main.go'],
        'swift': ['swift', '/home/main.swift'],
}
'''

with open('lang-commands.json', 'r') as file:
    command_dict = json.load(file)

#print(command_dict)


py_command = command_dict.get('py', [])
print(py_command)
