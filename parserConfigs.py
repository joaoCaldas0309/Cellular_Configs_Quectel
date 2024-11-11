import argparse
import subprocess
import sys

def scriptsExecute(scriptName):
    try:
        print(f'Executing the script: {scriptName}')
        subprocess.run([sys.executable, scriptName], check=True)
    except subprocess.CalledProcessError as e:
        print(f'An error occurred while executing {scriptName}: {e}')

def main():
    parser = argparse.ArgumentParser(description="Run scripts in sequence")
    parser.add_argument("First_script", type=str, help="Flashing Serial Number and ICCID at the table")
    parser.add_argument("Second_script", type=str, help="Flash the APN in device")

    args = parser.parse_args()

    scriptsExecute = (args.First_script)

    scriptsExecute = (args.Second_script)

if __name__ == "__main__":
    main()