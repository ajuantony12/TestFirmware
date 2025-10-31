import sys
import os
from jinja2 import Environment, FileSystemLoader

input = {'release_version': '000000'}
templateFile = ""
currentCfgFile = ""
outputFile = ""

argvLen = len(sys.argv) - 1

if argvLen >= 3:
    templateFile = sys.argv[1]
    currentCfgFile = sys.argv[2]
    outputFile = sys.argv[3]
else:
    print("Invalid format")
    sys.exit(-1)

#get Current release version
keyword = "#define VERSION"   # keyword to look for
relaseversion = 0

with open(currentCfgFile, "r") as f:
    found = False
    for line in f:
        # Check if line starts with keyword
        if line.startswith(keyword):
            words = line.split() 
            relaseversion = int(words[-1])
            found = True
            break
    
    if not found:
        print("Could not find current version")
        sys.exit(-1)

input['release_version'] = str(relaseversion + 1)
print(input)

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