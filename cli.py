"""Thin wrapper so users can type `python cli.py --prompt "..."`. Calls main.py."""

import subprocess
import sys


if __name__ == "__main__":
    subprocess.run([sys.executable, "main.py", *sys.argv[1:]], check=True)
