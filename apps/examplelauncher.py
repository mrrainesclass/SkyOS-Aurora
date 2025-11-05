import sys
import os
import subprocess

this_dir = os.path.dirname(os.path.abspath(__file__))
multifileappdir = this_dir + r"\multifileapp"
sc1 = rf"{multifileappdir}\test1.py"
sc2 = rf"{multifileappdir}\test2.py"

def main():
    subprocess.run([sys.executable, sc1], check=True)
    subprocess.run([sys.executable, sc2], check=True)
    sys.exit()

if __name__ == "__main__":
    main()