import csv
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union

class QuoteDataLoader:
    """
    Loads and parses training data for quote prediction from multiple formats:
    - CSV files: structured tabular data of jobs and quotes.
    - JSON files: list of job record objects.
    - Markdown logs: unstructured or semi-structured job descriptions.
    Provides data in a unified format (list of input-output pairs) for training.
    """
    def __init__(self):
        self.data: List[Tuple[str, str]] = []  # (input_text, output_text)
    
    def load_csv(self, file_path: Union[str, Path]) -> List[Dict[str, Any]]:
        """Load job records from a CSV file (each row as a dict)."""
        records: List[Dict[str, Any]] = []
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Convert numeric fields and boolean flags as needed
                record = {k: self._parse_value(v) for k, v in row.items()}
                records.append(record)
        return records
    
    def load_json(self, file_path: Union[str, Path]) -> List[Dict[str, Any]]:
        """Load job records from a JSON file (either list of dicts or single dict)."""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            # Single JSON object (e.g., a dict of records) -> take values
            return list(data.values())
        else:
            return []
    
    def load_markdown(self, file_path: Union[str, Path]) -> List[Dict[str, Any]]:
        """Load job records from a Markdown file with annotated examples."""
        records: List[Dict[str, Any]] = []
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        # Naive parsing: assume each example is separated by '---' or headings.
        # This can be replaced with a proper markdown parser if needed.
        raw_entries = text.split('---')
        for entry in raw_entries:
            entry = entry.strip()
            if not entry:
                continue
            record = self._parse_markdown_entry(entry)
            if record:
                records.append(record)
        return records
    
    def _parse_markdown_entry(self, entry: str) -> Dict[str, Any]:
        """
        Parse a single markdown entry into a record dict.
        Expected format (for example):
        "Service: Window Cleaning\nQuantity: 20\nSize: large\nOther Conditions: heavy soiling\nQuote: $100\n..."
        """
        record: Dict[str, Any] = {}
        lines = entry.splitlines()
        for line in lines:
            line = line.strip()
            if not line or ':' not in line:
                continue
            key, val = [x.strip() for x in line.split(':', 1)]
            # Normalize keys to lowercase, no spaces
            key_id = key.lower().replace(' ', '_')
            record[key_id] = self._parse_value(val)
        return record
    
    def _parse_value(self, val) -> Any:
        """Attempt to interpret numeric, boolean, or JSON values from strings or lists."""
        import json
        if isinstance(val, list):
            val = ",".join(str(v) for v in val)
        val = val.strip()
        # Try JSON parsing for dict/list fields
        if (val.startswith('{') and val.endswith('}')) or (val.startswith('[') and val.endswith(']')):
            try:
                return json.loads(val)
            except Exception:
                pass
        if val.isdigit():
            return int(val)
        try:
            return float(val)
        except ValueError:
            low = val.lower()
            if low in {"yes", "true", "y", "t"}:
                return True
            if low in {"no", "false", "n", "f"}:
                return False
            return val
    
    def prepare_training_data(self, records: List[Dict[str, Any]]) -> List[Tuple[str, str]]:
        """
        Convert structured records into (input_text, output_text) pairs for model training.
        For each job record, we create:
        - input_text: a descriptive prompt (could be JSON or natural language description).
        - output_text: the expected quote output (as JSON string).
        """
        pairs: List[Tuple[str, str]] = []
        for rec in records:
            # Create an input description (as JSON or NL). Here use JSON-like string for structured input.
            # Example: {"service": "window", "qty": 20, "size": "large", "surcharges": {"heavy_soil": true}}
            input_struct = {k: rec[k] for k in ["service", "qty", "size", "surcharges"] if k in rec}
            input_text = json.dumps(input_struct)
            # Create output text as JSON string of the quote (items, total). If record contains expected output, use it.
            if "items" in rec and "total" in rec:
                # Use provided quote structure if present
                output_struct = {"items": rec["items"], "total": rec["total"]}
            else:
                # If no output given, we can compute expected quote via rules as surrogate ground truth
                from llama3_model.utils.condition_logic import apply_conditions
                output_struct = apply_conditions(input_struct)
                output_struct.pop("surcharges", None)  # omit surcharges breakdown in final output
            output_text = json.dumps(output_struct)
            pairs.append((input_text, output_text))
        return pairs
    
    def load_all(self, paths: List[Union[str, Path]]) -> List[Tuple[str, str]]:
        """
        Load multiple data files and aggregate training pairs.
        """
        all_records: List[Dict[str, Any]] = []
        for path in paths:
            path = Path(path)
            if not path.exists():
                continue
            if path.suffix.lower() == '.csv':
                all_records += self.load_csv(path)
            elif path.suffix.lower() == '.json':
                all_records += self.load_json(path)
            elif path.suffix.lower() in {'.md', '.markdown'}:
                all_records += self.load_markdown(path)
        # Prepare unified training data
        self.data = self.prepare_training_data(all_records)
        return self.data
