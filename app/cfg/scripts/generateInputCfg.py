import sys
import os
from jinja2 import Environment, FileSystemLoader

input = {'SleepCycle': '1'}
templateFile = ""
outputFile = ""

argvLen = len(sys.argv) - 1

if argvLen >= 2:
    templateFile = sys.argv[1]
    outputFile = sys.argv[2]
    if argvLen == 3:
        input['SleepCycle'] = sys.argv[3]
    print('Configuration updated to ' + input['SleepCycle'])
else:
    print("Invalid format")
    sys.exit(-1)

template_dir = os.path.dirname(templateFile)
templatefilename = os.path.basename(templateFile)

# Load templates from current folder
env = Environment(loader=FileSystemLoader(template_dir))
template = env.get_template(templatefilename)

# Pass data directly as a dictionary
output = template.render(input)

# Save output
with open(outputFile, 'w') as f:
    f.write(output)

print("✅ File generated: " + outputFile)