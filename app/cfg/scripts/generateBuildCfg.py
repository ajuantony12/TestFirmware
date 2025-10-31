import sys
import os
from jinja2 import Environment, FileSystemLoader

input = {'release_version': '000000'}
templateFile = ""
outputFile = ""

argvLen = len(sys.argv) - 1

if argvLen >= 2:
    templateFile = sys.argv[1]
    outputFile = sys.argv[2]
    if argvLen >= 3:
        input['release_version'] = sys.argv[3]
else:
    print("Invalid format")
    sys.exit(-1)

# Load templates from current folder
template_dir = os.path.dirname(templateFile)
templatefilename = os.path.basename(templateFile)
env = Environment(loader=FileSystemLoader(template_dir))
template = env.get_template(templatefilename)

# Pass data directly as a dictionary
output = template.render(input)

# Save output
with open(outputFile, 'w') as f:
    f.write(output)

print("✅ File generated: " + outputFile)