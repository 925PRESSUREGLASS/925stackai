"""
llama3_model package: LLaMA3-style model for quote prediction.
Initializes the package and exposes main classes/functions for convenience.
"""

from llama3_model import utils  # expose utils subpackage
from llama3_model.data_loader import QuoteDataLoader
from llama3_model.inference import generate_quote
from llama3_model.model import Llama3QuoteModel
