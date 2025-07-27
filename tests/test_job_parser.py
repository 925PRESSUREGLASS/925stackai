print("DEBUG: test_job_parser.py reached top of file")
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from logic.job_parser import parse_prompt

print("DEBUG: test_job_parser.py is being executed")


def test_window_qty_storey():
    prompt = "Clean 10 windows on a two storey house"
    job = parse_prompt(prompt)
    assert job["service"] == "window"
    assert job["qty"] == 10
    assert job["storey"] == 2


def test_pressure_large_urgent():
    prompt = "Pressure wash 5 large areas, urgent"
    job = parse_prompt(prompt)
    assert job["service"] == "pressure"
    assert job["qty"] == 5
    assert job["size"] == "large"
    assert job["surcharges"]["urgent"] is True


def test_default_values():
    prompt = "Window cleaning"
    job = parse_prompt(prompt)
    assert job["service"] == "window"
    assert job["qty"] == 1
    assert job["storey"] == 1


if __name__ == "__main__":
    print("Running test_job_parser.py directly...")
    try:
        test_window_qty_storey()
        print("test_window_qty_storey passed")
    except Exception as e:
        print(f"test_window_qty_storey failed: {e}")
    try:
        test_pressure_large_urgent()
        print("test_pressure_large_urgent passed")
    except Exception as e:
        print(f"test_pressure_large_urgent failed: {e}")
    try:
        test_default_values()
        print("test_default_values passed")
    except Exception as e:
        print(f"test_default_values failed: {e}")
