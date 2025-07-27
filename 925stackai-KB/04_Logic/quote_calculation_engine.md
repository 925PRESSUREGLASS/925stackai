# Quote Calculation Engine

Algorithm for computing window cleaning quotes based on the Cottesloe pricing structure.

## Overview

The Quote Calculation Engine implements the business logic for converting customer requirements into accurate pricing quotes. It applies the comprehensive [window cleaning pricing structure](../03_Domain/window_cleaning_pricing.md) through a systematic calculation process.

## Core Algorithm

### Input Processing

The engine accepts structured input representing customer requirements:

```python
class QuoteRequest:
    def __init__(self):
        self.location: str = ""
        self.distance_km: float = 0.0
        self.windows: List[WindowItem] = []
        self.cleaning_level: str = "standard"
        self.service_date: datetime = None
        self.urgency: str = "normal"
        self.customer_type: str = "new"

class WindowItem:
    def __init__(self):
        self.type: str = ""  # standard, large, extra_large
        self.count: int = 0
        self.sides: str = "both"  # both, exterior, interior
        self.story: int = 1  # 1 = ground, 2+ = upper
        self.requires_wfp: bool = False
```

### Calculation Process

The engine processes quotes through a multi-stage pipeline:

```python
def calculate_quote(self, request: QuoteRequest) -> QuoteResult:
    quote = QuoteResult()
    
    # Stage 1: Base fees
    quote.add_line_item("Base Fee", 80.00)
    
    # Stage 2: Travel charges
    travel_cost = self.calculate_travel(request.distance_km)
    quote.add_line_item("Travel Fee", travel_cost)
    
    # Stage 3: Window pricing
    window_costs = self.calculate_window_costs(request.windows)
    quote.line_items.extend(window_costs)
    
    # Stage 4: Cleaning adjustments
    cleaning_adjustment = self.apply_cleaning_level(
        quote.window_subtotal, 
        request.cleaning_level
    )
    if cleaning_adjustment != 0:
        quote.add_line_item("Cleaning Level Adjustment", cleaning_adjustment)
    
    # Stage 5: Surcharges
    surcharges = self.calculate_surcharges(request, quote)
    quote.line_items.extend(surcharges)
    
    # Stage 6: Discounts
    discounts = self.calculate_discounts(request, quote)
    quote.line_items.extend(discounts)
    
    # Stage 7: Minimum charge validation
    quote.apply_minimum_charge(90.00)
    
    return quote
```

## Pricing Logic Implementation

### Travel Charge Calculation

```python
def calculate_travel(self, distance_km: float) -> float:
    if distance_km <= 5:
        return 10.00  # Local minimum
    else:
        additional_km = distance_km - 5
        return 10.00 + (additional_km * 2.00)
```

### Window Cost Calculation

```python
def calculate_window_costs(self, windows: List[WindowItem]) -> List[LineItem]:
    costs = []
    
    for window in windows:
        base_rate = self.get_base_rate(window.type, window.sides)
        
        # Apply story-based multiplier
        if window.story >= 2:
            if window.sides in ["both", "exterior"]:
                base_rate = self.apply_height_surcharge(base_rate, window.sides)
        
        total_cost = base_rate * window.count
        
        description = f"{window.count} {window.type} windows ({window.sides})"
        if window.story >= 2:
            description += " - Upper Story"
        
        costs.append(LineItem(description, total_cost))
        
        # Add WFP surcharge if required
        if window.requires_wfp:
            costs.append(LineItem("Water Fed Pole Surcharge", 20.00))
    
    return costs

def get_base_rate(self, window_type: str, sides: str) -> float:
    rates = {
        "standard": {"both": 10.00, "exterior": 6.00, "interior": 4.00},
        "large": {"both": 15.00, "exterior": 9.00, "interior": 6.00},
        "extra_large": {"both": 20.00, "exterior": 12.00, "interior": 8.00}
    }
    return rates[window_type][sides]
```

### Cleaning Level Adjustments

```python
def apply_cleaning_level(self, window_subtotal: float, level: str) -> float:
    modifiers = {
        "light": -0.10,
        "standard": 0.00,
        "mild": 0.10,
        "heavy": 0.20,
        "very_heavy": 0.30,
        "deep": 0.40
    }
    
    modifier = modifiers.get(level, 0.00)
    return window_subtotal * modifier
```

### Surcharge Calculation

```python
def calculate_surcharges(self, request: QuoteRequest, quote: QuoteResult) -> List[LineItem]:
    surcharges = []
    
    # Weekend/Holiday surcharge
    if self.is_weekend_or_holiday(request.service_date):
        surcharge = quote.subtotal * 0.30
        surcharges.append(LineItem("Weekend/Holiday Surcharge (+30%)", surcharge))
    
    # Urgency surcharges (apply to travel only)
    if request.urgency == "same_day":
        travel_surcharge = quote.get_travel_cost() * 0.25
        surcharges.append(LineItem("Same Day Surcharge (+25% travel)", travel_surcharge))
    elif request.urgency == "urgent":
        travel_surcharge = quote.get_travel_cost() * 0.50
        surcharges.append(LineItem("Urgent Surcharge (+50% travel)", travel_surcharge))
    
    return surcharges
```

### Discount Application

```python
def calculate_discounts(self, request: QuoteRequest, quote: QuoteResult) -> List[LineItem]:
    discounts = []
    
    # Winter discount (June-August)
    if self.is_winter_month(request.service_date):
        window_cost = quote.get_window_cost()
        discount = window_cost * 0.10
        discounts.append(LineItem("Winter Discount (-10% labour)", -discount))
    
    # Large job discount
    total_windows = sum(w.count for w in request.windows)
    if total_windows >= 50:
        discount_rate = 0.15
    elif total_windows >= 25:
        discount_rate = 0.10
    elif total_windows >= 10:
        discount_rate = 0.05
    else:
        discount_rate = 0.00
    
    if discount_rate > 0:
        discount = quote.subtotal * discount_rate
        discounts.append(LineItem(f"Large Job Discount (-{discount_rate*100:.0f}%)", -discount))
    
    return discounts
```

## Example JSON Input/Output

### Input Example

```json
{
    "location": "Swanbourne",
    "distance_km": 6.0,
    "windows": [
        {
            "type": "standard",
            "count": 6,
            "sides": "both",
            "story": 1,
            "requires_wfp": false
        },
        {
            "type": "standard",
            "count": 4,
            "sides": "exterior",
            "story": 2,
            "requires_wfp": true
        }
    ],
    "cleaning_level": "mild",
    "service_date": "2024-07-15T10:00:00",
    "urgency": "normal",
    "customer_type": "new"
}
```

### Output Example

```json
{
    "quote_id": "Q-2024-001",
    "total": 263.80,
    "line_items": [
        {"description": "Base Fee", "amount": 80.00},
        {"description": "Travel Fee", "amount": 12.00},
        {"description": "6 standard windows (both)", "amount": 60.00},
        {"description": "4 standard windows (exterior) - Upper Story", "amount": 48.00},
        {"description": "Water Fed Pole Surcharge", "amount": 20.00},
        {"description": "Mild Cleaning Adjustment (+10%)", "amount": 13.80}
    ],
    "calculation_notes": [
        "Travel: 6km = $10 + (1 × $2)",
        "Upper story exterior rate: $12 (double ground exterior)",
        "Mild cleaning: +10% on window costs only"
    ]
}
```

## Integration Points

The calculation engine is used by:

- **Quoting Agent**: For generating customer quotes
- **Evaluation Agent**: For testing calculation accuracy
- **API Endpoints**: For programmatic quote generation
- **Streamlit UI**: For real-time quote display

For usage examples, see the [quoting examples documentation](../03_Domain/quoting_examples.md).
