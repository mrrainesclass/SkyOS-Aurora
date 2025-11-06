import argparse
import requests
import sys
import os

# Colors
RED = "\033[31m"
RESET = "\033[0m"

def find_file_in_folder(folder_path, file_name):
    """Search recursively for a file in a folder."""
    for root, dirs, files in os.walk(folder_path):
        if file_name in files:
            return os.path.join(root, file_name)
    return None

# Base URL for installation assets
installurl = "https://raw.githubusercontent.com/Alter-Net-codes/SkyOS-assets/main"

# Download package list if missing
if not os.path.isfile("apps.txt"):
    print("Global package list not found on your device. Downloading...")
    try:
        response = requests.get(f"{installurl}/apps.txt")
        response.raise_for_status()
        with open("apps.txt", "w") as file:
            file.write(response.text.strip())
        print("Global package list downloaded successfully.")
    except Exception as e:
        print(f"{RED}Failed to download package list: {e}{RESET}")
        sys.exit(1)

# Define directories
this_dir = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.abspath(os.path.join(this_dir, '..'))
apps_dir = os.path.join(root_path, 'apps')

# Ensure apps directory exists
os.makedirs(apps_dir, exist_ok=True)

# Argument parsing
parser = argparse.ArgumentParser(description="SkyPKG - SkyOS package manager.")
parser.add_argument("command", nargs="?", type=str, help="Command (install, update, etc.)")
parser.add_argument("package", nargs="?", type=str, help="Package to install or update.")
parser.add_argument("--updatelists", action="store_true", help="Update the global package lists.")
args = parser.parse_args()

try:
    # Handle --updatelists
    if args.updatelists:
        print("Updating global package lists...")
        response = requests.get(f"{installurl}/apps.txt")
        response.raise_for_status()
        with open("apps.txt", "w") as file:
            file.write(response.text.strip())
        print("Package lists updated successfully.")
        sys.exit(0)

    # Require command and package for install/update
    if not args.command or not args.package:
        print(f"{RED}Usage: skypkg <command> <package>{RESET}")
        sys.exit(1)

    command = args.command.lower()
    package = args.package.strip()

    # Load app list
    with open("apps.txt", "r") as file:
        fdata = [line.strip() for line in file.readlines()]

    app_path = os.path.join(apps_dir, f"{package}.py")

    # Update command
    if command == "update":
        if package not in fdata:
            print(f"{RED}There is no updatable package named {package}.{RESET}")
            sys.exit(1)

        print(f"Updating {package}...")
        response = requests.get(f"{installurl}/assets/{package}.py")
        response.raise_for_status()
        with open(app_path, "w") as file:
            file.write(response.text.strip())
        print(f"Successfully updated {package}.")
        sys.exit(0)

    # Install command
    elif command == "install":
        if os.path.exists(app_path):
            print(f"{RED}Package '{package}' is already installed. Use 'skypkg update {package}' to update it.{RESET}")
            sys.exit(1)

        if package not in fdata:
            print(f"{RED}There is no installable package named {package}.{RESET}")
            sys.exit(1)

        print(f"Installing {package}...")
        response = requests.get(f"{installurl}/assets/{package}.py")
        response.raise_for_status()
        with open(app_path, "w") as file:
            file.write(response.text.strip())
        print(f"Successfully installed {package}.")
        sys.exit(0)

    else:
        print(f"{RED}Unknown command: {command}{RESET}")
        sys.exit(1)

except requests.exceptions.RequestException as e:
    print(f"{RED}Network error: {e}{RESET}")
    sys.exit(1)
except Exception as e:
    print(f"{RED}An error occurred: {e}{RESET}")

    sys.exit(1)
