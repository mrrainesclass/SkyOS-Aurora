import argparse
import requests
import sys
import os

RED = "\033[31m"
RESET = "\033[0m"

# first time the application is used we want to install all the package lists.
# dont use this url the whole time change it later.
installurl = "https://raw.githubusercontent.com/mrrainesclass/SkyOS-assets/patch-1"
if os.path.isfile("apps.txt"):
    pass
else:
    print("Global package list not found on your device. Downloading...")
    response = requests.get(f"{installurl}/apps.txt")
    response = response.text.strip()
    with open("apps.txt", "w") as file:
        file.write(response)
    # now we download the version list.
    

this_dir = os.path.dirname(os.path.abspath(__file__))

root_path = os.path.abspath(os.path.join(this_dir, '..'))  # Go up two levels to get the root directory

apps_dir = os.path.join(root_path, 'apps')

parser = argparse.ArgumentParser(description="Argparse for skypkg.")
parser.add_argument("command", type=str, help="The command you want to execute, such as 'install' or 'update'.")
parser.add_argument("package", type=str, help="The package you want ot install.")
parser.add_argument("--updatelists", type=bool, help="Update your lists. 'skypkg --updatelists True'")
args = parser.parse_args()

command = args.command
package = args.package

if args.updatelists:
    response = requests.get(f"{installurl}/apps.txt")
    response = response.text.strip()
    with open("apps.txt", "") as file:
        file.truncate(0)
        file.write(response)

elif command == "update":
    pass
    sys.exit()

elif command == "install":
    # install the users app.
    with open("apps.txt", "r") as file:
        fdata = file.readlines()
        file.close()
    if package in fdata:
        # install app into DATA
        response = requests.get(f"{installurl}/assets/{package}.py")
        response = response.text.strip()
        with open(f"{apps_dir}\{package}.py") as file:
            file.truncate(0)
            file.write(response)
            print(f"Succesfully installed {package}-{version}")
        sys.exit()
    else:
        print(f"{RED}There is no installable app named {package}.{RESET}")
        sys.exit()

else:
    print("Skypkg could not find the command you want tp install.")