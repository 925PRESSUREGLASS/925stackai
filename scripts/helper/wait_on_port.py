#!/usr/bin/env python3
"""Wait until a TCP port on localhost is open."""

from __future__ import annotations

import argparse
import socket
import time


def wait_on_port(port: int, host: str = "localhost", timeout: int = 60) -> bool:
    end = time.time() + timeout
    while time.time() < end:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            try:
                sock.connect((host, port))
                return True
            except OSError:
                time.sleep(1)
    return False


def main() -> None:
    parser = argparse.ArgumentParser(description="Wait for a TCP port to become available")
    parser.add_argument("port", type=int)
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--timeout", type=int, default=60)
    args = parser.parse_args()
    if wait_on_port(args.port, args.host, args.timeout):
        print(f"{args.host}:{args.port} is ready")
    else:
        raise SystemExit(f"Timeout waiting for {args.host}:{args.port}")


if __name__ == "__main__":
    main()
