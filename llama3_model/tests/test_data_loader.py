import os
from pathlib import Path

from llama3_model.data_loader import QuoteDataLoader


def test_load_csv(tmp_path):
    # Create a sample CSV file
    # Use only flat fields for robust parsing
    csv_content = "service,qty,size,total\nwindow,10,large,50.0\n"
    csv_file = tmp_path / "sample.csv"
    csv_file.write_text(csv_content)
    loader = QuoteDataLoader()
    records = loader.load_csv(csv_file)
    assert isinstance(records, list)
    assert len(records) == 1
    assert records[0]["service"] == "window"
    assert records[0]["qty"] == 10
    assert records[0]["size"] == "large"
    assert records[0]["total"] == 50.0


def test_prepare_training_data():
    loader = QuoteDataLoader()
    records = [
        {
            "service": "window",
            "qty": 10,
            "size": "large",
            "surcharges": {"heavy_soil": True},
            "items": [
                {
                    "service": "window",
                    "qty": 10,
                    "unit_price": 4.0,
                    "size": "large",
                    "subtotal": 50.0,
                }
            ],
            "total": 50.0,
        }
    ]
    pairs = loader.prepare_training_data(records)
    assert isinstance(pairs, list)
    assert len(pairs) == 1
    input_text, output_text = pairs[0]
    assert "window" in input_text
    assert "total" in output_text
