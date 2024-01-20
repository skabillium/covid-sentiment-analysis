import re
import os

script_regex = r'^\d+-.*\.py$'
description_regex = r'^\s*("""[\s\S]*?""")'


files = os.listdir(os.getcwd())
files.sort()

scripts = [f for f in files if re.match(script_regex, f)]


print('Running scripts in correct order of execution:')
for script in scripts:
    print(f'\nRunning {script}:')
    with open(script, 'r') as file:
        content = file.read()

    match = re.search(description_regex, content)
    if match:
        print(eval(match.group(1)).strip() + '\n')

    os.system(f'python {script}')
