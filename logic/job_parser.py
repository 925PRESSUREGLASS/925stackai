from __future__ import annotations
from typing import Dict, Any, List, Optional

def parse_job(data: Dict[str, Any]) -> Dict[str, Any]:
    """Parse a job dictionary and return a normalized job dict."""
    # Example: normalize keys, validate fields, etc.
    job: Dict[str, Any] = {}
    job["service"] = str(data.get("service", ""))
    job["qty"] = int(data.get("qty", 1))
    job["storey"] = int(data.get("storey", 1))
    job["size"] = str(data.get("size", ""))
    job["surcharges"] = data.get("surcharges", {})
    return job

# Example usage for mypy strict compliance
def parse_jobs(data_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [parse_job(d) for d in data_list]
