# Quoting Agent

Agent responsible for generating window cleaning quotes based on customer requirements and pricing structure.

## Overview

The Quoting Agent serves as the primary interface between customer inquiries and the quote calculation engine. It interprets natural language requests, extracts relevant parameters (window counts, types, locations), and generates accurate pricing using the established [window cleaning pricing structure](../03_Domain/window_cleaning_pricing.md).

## Core Functionality

### Input Processing
The agent handles various input formats:
- Natural language descriptions: "I need 10 windows cleaned on my 2-story house"
- Structured requests with specific window types and counts
- Follow-up questions about existing quotes or pricing adjustments

### Quote Generation Process

```python
def generate_quote(self, user_input: str, context: dict) -> QuoteResponse:
    # 1. Parse user requirements
    requirements = self.extract_requirements(user_input)
    
    # 2. Validate and structure data
    window_data = self.structure_window_data(requirements)
    
    # 3. Calculate pricing using engine
    quote = self.quote_engine.calculate(window_data)
    
    # 4. Format response with breakdown
    return self.format_quote_response(quote, requirements)
```

### Integration with Pricing Engine
The agent interfaces with the Quote Calculation Engine to apply the comprehensive pricing structure including:
- Base fees and travel charges
- Per-pane pricing based on window size and type
- Cleaning level adjustments (light, standard, heavy)
- Surcharges for upper-story access, weekend work, urgent requests
- Discounts for large jobs or regular customers

## Example Interaction

**User Input**: "I need a quote for 8 standard windows and 2 sliding doors, both sides, ground floor only"

**Agent Processing**:
1. Extracts: 8 standard panes + 2 sliding door panels
2. Assumes: Both interior and exterior cleaning
3. Applies: Standard pricing without upper-story surcharge

**Output**:
```
Quote Breakdown:
- Base Fee: $80.00
- Travel Fee: $10.00
- 8 Standard Panes (both sides): 8 × $10.00 = $80.00
- 2 Sliding Door Panels (both sides): 2 × $20.00 = $40.00
Total: $210.00
```

## Memory Integration

The agent works with the Memory Agent to:
- Recall previous quotes for the same customer
- Remember customer preferences (window types, cleaning frequency)
- Track quote history for follow-up estimates

## Error Handling

The agent includes validation for:
- Incomplete or ambiguous requests (prompts for clarification)
- Invalid window types or configurations
- Pricing edge cases requiring manual review
- Geographic constraints for travel charges

For implementation details of the pricing calculations, see [Quote Calculation Engine](../04_Logic/quote_calculation_engine.md).
