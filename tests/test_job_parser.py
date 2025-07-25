from logic.job_parser import parse_prompt

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
