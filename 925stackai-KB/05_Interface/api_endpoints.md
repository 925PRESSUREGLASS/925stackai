# API Endpoints

Programmatic access to the 925stackai quoting service through RESTful API endpoints.

## Overview

The 925stackai system provides REST API endpoints for external integration, allowing third-party applications to access quote generation, user management, and system monitoring capabilities.

## Base Configuration

### API Server Setup

```python
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="925stackai Window Cleaning API",
    description="AI-powered window cleaning quote generation",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Data Models

### Request Models

```python
class WindowItem(BaseModel):
    type: str  # "standard", "large", "extra_large"
    count: int
    sides: str  # "both", "exterior", "interior"
    story: int = 1
    requires_wfp: bool = False

class QuoteRequest(BaseModel):
    location: str
    distance_km: Optional[float] = None
    windows: List[WindowItem]
    cleaning_level: str = "standard"
    service_date: Optional[str] = None
    urgency: str = "normal"
    customer_type: str = "new"
    customer_id: Optional[str] = None

class ChatMessage(BaseModel):
    message: str
    session_id: str
    user_id: Optional[str] = None
```

### Response Models

```python
class LineItem(BaseModel):
    description: str
    amount: float

class QuoteResponse(BaseModel):
    quote_id: str
    total: float
    line_items: List[LineItem]
    calculation_notes: List[str]
    valid_until: str
    created_at: str

class ChatResponse(BaseModel):
    response: str
    quote_data: Optional[QuoteResponse] = None
    session_id: str
    requires_clarification: bool = False
```

## Core Endpoints

### Quote Generation

```python
@app.post("/api/v1/quote", response_model=QuoteResponse)
async def generate_quote(
    request: QuoteRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Generate a window cleaning quote based on provided requirements.
    
    Args:
        request: Quote requirements including windows, location, etc.
        api_key: Valid API key for authentication
    
    Returns:
        QuoteResponse: Detailed quote with breakdown and total
    
    Example:
        POST /api/v1/quote
        {
            "location": "Cottesloe",
            "distance_km": 2.0,
            "windows": [
                {
                    "type": "standard",
                    "count": 8,
                    "sides": "both",
                    "story": 1
                }
            ],
            "cleaning_level": "standard"
        }
    """
    try:
        # Validate location and calculate distance if not provided
        if request.distance_km is None:
            request.distance_km = calculate_distance_from_cottesloe(request.location)
        
        # Generate quote using calculation engine
        quote_result = quote_engine.calculate_quote(request)
        
        # Save to memory if customer_id provided
        if request.customer_id:
            memory_agent.save_quote_request(request.customer_id, request, quote_result)
        
        return quote_result
        
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
```

### Chat Interface

```python
@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat_interaction(
    message: ChatMessage,
    api_key: str = Depends(verify_api_key)
):
    """
    Process natural language chat messages and generate responses.
    
    Can handle quote requests, questions, and follow-up conversations.
    
    Example:
        POST /api/v1/chat
        {
            "message": "I need a quote for 10 windows",
            "session_id": "session_123",
            "user_id": "user_456"
        }
    """
    try:
        # Get conversation context
        context = memory_agent.get_conversation_context(
            message.session_id, 
            message.user_id
        )
        
        # Process through GUI agent
        response = gui_agent.process_chat_message(message.message, context)
        
        # Save conversation
        memory_agent.save_conversation_exchange(
            message.session_id,
            message.message,
            response
        )
        
        return ChatResponse(
            response=response.content,
            quote_data=response.quote_data,
            session_id=message.session_id,
            requires_clarification=response.needs_clarification
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Quote History

```python
@app.get("/api/v1/quotes/{customer_id}", response_model=List[QuoteResponse])
async def get_quote_history(
    customer_id: str,
    limit: int = 10,
    api_key: str = Depends(verify_api_key)
):
    """
    Retrieve quote history for a specific customer.
    
    Args:
        customer_id: Unique customer identifier
        limit: Maximum number of quotes to return
    
    Returns:
        List of previous quotes for the customer
    """
    try:
        quotes = memory_agent.get_quote_history(customer_id, limit)
        return quotes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

## Administrative Endpoints

### System Health

```python
@app.get("/api/v1/health")
async def health_check():
    """
    Check system health and component status.
    
    Returns:
        System status and component availability
    """
    health_status = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "components": {
            "quote_engine": "operational",
            "memory_store": "operational",
            "ai_agents": "operational"
        }
    }
    
    try:
        # Test each component
        test_quote = QuoteRequest(
            location="Test",
            distance_km=1.0,
            windows=[WindowItem(type="standard", count=1, sides="both")]
        )
        quote_engine.calculate_quote(test_quote)
        
        # Test memory access
        memory_agent.health_check()
        
        return health_status
        
    except Exception as e:
        health_status["status"] = "degraded"
        health_status["error"] = str(e)
        raise HTTPException(status_code=503, detail=health_status)
```

### Metrics and Analytics

```python
@app.get("/api/v1/metrics")
async def get_metrics(api_key: str = Depends(verify_admin_key)):
    """
    Retrieve system metrics and usage statistics.
    
    Requires admin-level API key.
    """
    metrics = {
        "quotes_generated_today": evaluation_agent.get_daily_quote_count(),
        "average_response_time": evaluation_agent.get_avg_response_time(),
        "error_rate": evaluation_agent.get_error_rate(),
        "popular_locations": memory_agent.get_popular_locations(),
        "average_quote_value": memory_agent.get_average_quote_value()
    }
    
    return metrics
```

## Authentication

### API Key Management

```python
async def verify_api_key(api_key: str = Header(...)):
    """Verify API key for standard endpoints"""
    if not api_key_manager.is_valid(api_key):
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )
    return api_key

async def verify_admin_key(api_key: str = Header(...)):
    """Verify admin API key for sensitive endpoints"""
    if not api_key_manager.is_admin(api_key):
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )
    return api_key
```

### Rate Limiting

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/api/v1/quote")
@limiter.limit("10/minute")  # 10 requests per minute per IP
async def generate_quote_limited(request: Request, quote_req: QuoteRequest):
    return await generate_quote(quote_req)
```

## Error Handling

### Custom Exception Handlers

```python
@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "details": exc.errors(),
            "message": "Please check your request format"
        }
    )

@app.exception_handler(QuoteCalculationError)
async def quote_calculation_exception_handler(request: Request, exc: QuoteCalculationError):
    return JSONResponse(
        status_code=400,
        content={
            "error": "Quote Calculation Error",
            "message": str(exc),
            "suggestion": "Please verify window counts and property details"
        }
    )
```

## Example Usage

### Python Client

```python
import requests

class WindowCleaningAPI:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.headers = {"X-API-Key": api_key}
    
    def get_quote(self, location: str, windows: list) -> dict:
        """Get a quote for window cleaning"""
        request_data = {
            "location": location,
            "windows": windows,
            "cleaning_level": "standard"
        }
        
        response = requests.post(
            f"{self.base_url}/api/v1/quote",
            json=request_data,
            headers=self.headers
        )
        
        return response.json()

# Usage example
api = WindowCleaningAPI("https://api.925stackai.com", "your-api-key")
quote = api.get_quote("Cottesloe", [
    {"type": "standard", "count": 8, "sides": "both", "story": 1}
])
print(f"Total quote: ${quote['total']:.2f}")
```

### JavaScript Client

```javascript
class WindowCleaningAPI {
    constructor(baseUrl, apiKey) {
        this.baseUrl = baseUrl;
        this.apiKey = apiKey;
    }
    
    async getQuote(location, windows) {
        const response = await fetch(`${this.baseUrl}/api/v1/quote`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-API-Key': this.apiKey
            },
            body: JSON.stringify({
                location: location,
                windows: windows,
                cleaning_level: 'standard'
            })
        });
        
        return await response.json();
    }
}

// Usage
const api = new WindowCleaningAPI('https://api.925stackai.com', 'your-api-key');
const quote = await api.getQuote('Cottesloe', [
    {type: 'standard', count: 8, sides: 'both', story: 1}
]);
console.log(`Total: $${quote.total}`);
```

## Documentation and Testing

The API includes:
- OpenAPI/Swagger documentation at `/docs`
- ReDoc documentation at `/redoc`
- Interactive testing interface
- Postman collection for integration testing

For local deployment instructions, see [Local Run Guide](../06_Deploy/local_run.md).
