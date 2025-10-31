import requests
import json
import sys
import subprocess
import re



GITHUB_TOKEN = ""
OWNER = "adi-innersource"
REPO = "viser-autotune-workflow"
RETEST_WORKFLOW_FILE = "ci_cloudRunner.yml"  # workflow filename
PATCHER_WORKFLOW_FILE = "ci_patcher.yml"  # workflow filename
argvLen = len(sys.argv) - 1
if (argvLen != 5):
    print("Invalid arguments ")
    sys.exit(-1)
BRANCH = sys.argv[1]
logfile = sys.argv[2]
currentCfg = int(sys.argv[3])
expected =int(sys.argv[4])
GITHUB_TOKEN = sys.argv[5]

retestUrl = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/workflows/{RETEST_WORKFLOW_FILE}/dispatches"
patcherUrl = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/workflows/{PATCHER_WORKFLOW_FILE}/dispatches"

headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Content-Type": "application/json"
}

payloadPatcher = {
    "ref": BRANCH,
    "inputs": {
        "cfgValue":"1"
    }
}

payloadTester = {
    "ref": BRANCH,
    "inputs": {
        "reConfigRequired":"false",
        "cfgValue":"1",
        "expValue":"1"
    }
}

def parse_and_average(input_source):
    """Parse SleepPerCycle values and calculate average."""
    values = []
    pattern = r'SleepPerCycle=(\d+)\)'
    
    if isinstance(input_source, str):
        # Input is a filename
        try:
            with open(input_source, 'r') as f:
                lines = f.readlines()
        except FileNotFoundError:
            print(f"File not found: {input_source}")
            return
    else:
        # Input is a list of lines or stdin
        lines = input_source
    
    for line in lines:
        print(line)
        match = re.search(pattern, line.strip())
        if match:
            try:
                value = int(match.group(1))
                values.append(value)
                print(f"Found: SleepPerCycle = {value}")
            except ValueError:
                continue

    average = 0
    
    if values:
        average = sum(values) / len(values)
        print(f"\n--- Results ---")
        print(f"Total values found: {len(values)}")
        print(f"Values: {values}")
        print(f"Average SleepPerCycle: {average:.2f}")
        print(f"Min: {min(values)}, Max: {max(values)}")        
    else:
        print("No SleepPerCycle values found in input!")

    return average

averageSleep = parse_and_average(logfile)
expectedHigh = expected + 500
expectedLow = expected if expected > 500 else expected - 500


#do patch increment if result matches
if (averageSleep < expectedHigh) and (averageSleep > expectedLow):
    subprocess.run(["git", "reset", "--hard"], check=True)
    payloadPatcher["inputs"]["cfgValue"] = currentCfg
    response = requests.post(patcherUrl, headers=headers, data=json.dumps(payloadPatcher))
    if response.status_code == 204:
        print("Patcher Workflow triggered successfully!")
    else:
        print("Error:", response.status_code, response.text)
else:
    payloadTester["inputs"]["reConfigRequired"] = "true"
    payloadTester["inputs"]["expValue"] = str(expected)
    if (averageSleep < expectedLow):
        payloadTester["inputs"]["cfgValue"] = str(currentCfg - 1)
    else:
        payloadTester["inputs"]["cfgValue"] = str(currentCfg + 1)

    response = requests.post(retestUrl, headers=headers, data=json.dumps(payloadTester))
    if response.status_code == 204:
        print("Runner Workflow triggered successfully!")
    else:
        print("Error:", response.status_code, response.text)
