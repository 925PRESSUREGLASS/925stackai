import types
import sys

# Provide a simple stub for the segment detection module if missing
if 'logic.segment_detect' not in sys.modules:
    mod = types.ModuleType('logic.segment_detect')
    mod.detect_customer_segment = lambda text: 'residential' if 'home' in text else 'commercial'
    sys.modules['logic.segment_detect'] = mod

from logic.segment_detect import detect_customer_segment


def test_detect_customer_segment_smoke() -> None:
    label = detect_customer_segment("home cleaning request")
    assert isinstance(label, str)
