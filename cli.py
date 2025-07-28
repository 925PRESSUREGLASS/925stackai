"""Thin wrapper so users can type `python cli.py --prompt "..."`. Calls main.py."""

import sys
from main import main


if __name__ == "__main__":
    main(sys.argv[1:])
