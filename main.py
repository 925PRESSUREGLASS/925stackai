"""Unified entry-point for the quoting AI system."""

import argparse
from orchestrator import Orchestrator


def parse_args() -> str:
    parser = argparse.ArgumentParser(description="Quoting AI entry-point")
    parser.add_argument("--prompt", required=True, help="User prompt for quoting agent")
    args = parser.parse_args()
    return str(args.prompt)


def main() -> None:
    user_prompt = parse_args()
    orchestrator = Orchestrator()
    response = orchestrator.run(user_prompt)
    print("\n=== AI Response ===\n")
    print(response)


if __name__ == "__main__":
    main()
