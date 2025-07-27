# Adding New Agents

How to extend 925stackai with custom agents to add new functionality.

## Overview

The 925stackai system is designed for extensibility through its modular agent architecture. Adding new agents allows you to extend functionality while maintaining the existing system structure and interfaces.

## Agent Architecture

### Base Agent Structure

All agents inherit from the base `Agent` class:

```python
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class Agent(ABC):
    """Base class for all agents in the 925stackai system"""
    
    def __init__(self, name: str, config: Dict[str, Any]):
        self.name = name
        self.config = config
        self.memory_agent = None  # Injected by orchestrator
        
    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input and return response"""
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Return list of capabilities this agent provides"""
        pass
    
    def set_memory_agent(self, memory_agent):
        """Set reference to memory agent for context access"""
        self.memory_agent = memory_agent
```

## Step-by-Step Guide

### 1. Define Agent Purpose

First, clearly define what your new agent will do:

**Example**: Creating an `AnalysisAgent` for business analytics

* **Purpose**: Analyze quote patterns, customer trends, and business metrics
* **Inputs**: Historical data, date ranges, analysis type
* **Outputs**: Charts, statistics, insights, recommendations

### 2. Create Agent Class

Create a new file in the `app/agents/` directory:

```python
# app/agents/analysis_agent.py

from typing import Dict, Any, List
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

from .base_agent import Agent

class AnalysisAgent(Agent):
    """Agent responsible for business analytics and data insights"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__("analysis_agent", config)
        self.supported_analyses = [
            "quote_trends",
            "customer_segments", 
            "revenue_analysis",
            "seasonal_patterns"
        ]
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process analysis request and generate insights"""
        analysis_type = input_data.get("analysis_type")
        date_range = input_data.get("date_range", self._default_date_range())
        
        if analysis_type not in self.supported_analyses:
            return self._error_response(f"Unsupported analysis: {analysis_type}")
        
        try:
            # Get data from memory agent
            data = await self._get_analysis_data(date_range)
            
            # Perform analysis
            if analysis_type == "quote_trends":
                result = self._analyze_quote_trends(data)
            elif analysis_type == "customer_segments":
                result = self._analyze_customer_segments(data)
            elif analysis_type == "revenue_analysis":
                result = self._analyze_revenue(data)
            elif analysis_type == "seasonal_patterns":
                result = self._analyze_seasonal_patterns(data)
            
            return {
                "success": True,
                "analysis_type": analysis_type,
                "data": result,
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            return self._error_response(str(e))
    
    def get_capabilities(self) -> List[str]:
        """Return list of analysis capabilities"""
        return [
            "quote_trend_analysis",
            "customer_segmentation",
            "revenue_analytics", 
            "seasonal_pattern_detection",
            "business_insights"
        ]
    
    async def _get_analysis_data(self, date_range: Dict) -> pd.DataFrame:
        """Retrieve data from memory agent for analysis"""
        if not self.memory_agent:
            raise Exception("Memory agent not available")
        
        # Get quote history data
        quotes = self.memory_agent.get_quotes_in_range(
            start_date=date_range["start"],
            end_date=date_range["end"]
        )
        
        return pd.DataFrame(quotes)
    
    def _analyze_quote_trends(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze quote volume and value trends"""
        # Group by date
        daily_stats = data.groupby(data['created_date'].dt.date).agg({
            'quote_id': 'count',
            'total_amount': ['sum', 'mean']
        }).round(2)
        
        # Create trend chart
        chart = px.line(
            x=daily_stats.index,
            y=daily_stats[('total_amount', 'sum')],
            title="Daily Quote Revenue Trend"
        )
        
        return {
            "trend_data": daily_stats.to_dict(),
            "chart": chart.to_json(),
            "insights": self._generate_trend_insights(daily_stats)
        }
    
    def _generate_trend_insights(self, data: pd.DataFrame) -> List[str]:
        """Generate text insights from trend data"""
        insights = []
        
        # Calculate growth rate
        if len(data) > 1:
            recent_avg = data.tail(7).mean()
            earlier_avg = data.head(7).mean()
            growth_rate = ((recent_avg - earlier_avg) / earlier_avg * 100)
            
            if growth_rate > 10:
                insights.append(f"Strong growth: {growth_rate:.1f}% increase in recent period")
            elif growth_rate < -10:
                insights.append(f"Declining trend: {growth_rate:.1f}% decrease in recent period")
            else:
                insights.append("Stable performance with minimal variance")
        
        return insights
```

### 3. Register Agent with Orchestrator

Update the agent orchestrator to include your new agent:

```python
# app/orchestrator.py

from .agents.analysis_agent import AnalysisAgent

class AgentOrchestrator:
    def __init__(self):
        self.agents = {}
        self._initialize_agents()
    
    def _initialize_agents(self):
        """Initialize all system agents"""
        # Existing agents
        self.agents['quoting'] = QuotingAgent(config.QUOTING_CONFIG)
        self.agents['memory'] = MemoryAgent(config.MEMORY_CONFIG)
        self.agents['gui'] = GUIAgent(config.GUI_CONFIG)
        self.agents['evaluation'] = EvaluationAgent(config.EVAL_CONFIG)
        
        # New agent
        self.agents['analysis'] = AnalysisAgent(config.ANALYSIS_CONFIG)
        
        # Set memory agent references
        for agent in self.agents.values():
            if hasattr(agent, 'set_memory_agent'):
                agent.set_memory_agent(self.agents['memory'])
    
    def get_agent(self, agent_name: str) -> Agent:
        """Get agent by name"""
        return self.agents.get(agent_name)
    
    async def route_request(self, request_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Route requests to appropriate agents"""
        if request_type == "analysis":
            return await self.agents['analysis'].process(data)
        # ... existing routing logic
```

### 4. Add Configuration

Add configuration for your new agent:

```python
# config/analysis_config.py

ANALYSIS_CONFIG = {
    "default_date_range_days": 30,
    "max_data_points": 1000,
    "chart_template": "plotly_white",
    "cache_results": True,
    "cache_ttl": 3600,  # 1 hour
    "supported_exports": ["json", "csv", "png"]
}
```

### 5. Update GUI Integration

Integrate the new agent with the Streamlit interface:

```python
# gui/components/analysis_dashboard.py

import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta

def render_analysis_dashboard(orchestrator):
    """Render analysis dashboard in Streamlit"""
    st.header("📊 Business Analytics")
    
    # Analysis type selection
    analysis_type = st.selectbox(
        "Select Analysis Type",
        ["quote_trends", "customer_segments", "revenue_analysis", "seasonal_patterns"]
    )
    
    # Date range selection
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", 
                                 value=datetime.now() - timedelta(days=30))
    with col2:
        end_date = st.date_input("End Date", value=datetime.now())
    
    # Run analysis button
    if st.button("Run Analysis"):
        with st.spinner("Analyzing data..."):
            # Call analysis agent
            result = await orchestrator.route_request("analysis", {
                "analysis_type": analysis_type,
                "date_range": {
                    "start": start_date.isoformat(),
                    "end": end_date.isoformat()
                }
            })
            
            if result.get("success"):
                display_analysis_results(result)
            else:
                st.error(f"Analysis failed: {result.get('error')}")

def display_analysis_results(result: Dict[str, Any]):
    """Display analysis results in Streamlit"""
    data = result["data"]
    
    # Show chart if available
    if "chart" in data:
        st.plotly_chart(data["chart"], use_container_width=True)
    
    # Show insights
    if "insights" in data:
        st.subheader("Key Insights")
        for insight in data["insights"]:
            st.write(f"• {insight}")
    
    # Show raw data table
    if "trend_data" in data:
        st.subheader("Detailed Data")
        st.dataframe(pd.DataFrame(data["trend_data"]))
```

### 6. Add API Endpoints

Create API endpoints for external access:

```python
# app/api/analysis_endpoints.py

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, List
from datetime import date

router = APIRouter(prefix="/api/v1/analysis", tags=["analysis"])

class AnalysisRequest(BaseModel):
    analysis_type: str
    start_date: date
    end_date: date
    parameters: Dict[str, Any] = {}

@router.post("/run")
async def run_analysis(
    request: AnalysisRequest,
    orchestrator = Depends(get_orchestrator)
):
    """Run business analysis"""
    try:
        result = await orchestrator.route_request("analysis", {
            "analysis_type": request.analysis_type,
            "date_range": {
                "start": request.start_date.isoformat(),
                "end": request.end_date.isoformat()
            },
            "parameters": request.parameters
        })
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/types")
async def get_analysis_types(orchestrator = Depends(get_orchestrator)):
    """Get available analysis types"""
    analysis_agent = orchestrator.get_agent('analysis')
    return {
        "supported_analyses": analysis_agent.supported_analyses,
        "capabilities": analysis_agent.get_capabilities()
    }
```

### 7. Add Testing

Create tests for your new agent:

```python
# tests/test_analysis_agent.py

import pytest
from unittest.mock import Mock, AsyncMock
import pandas as pd
from datetime import datetime

from app.agents.analysis_agent import AnalysisAgent

@pytest.fixture
def analysis_agent():
    config = {"default_date_range_days": 30}
    agent = AnalysisAgent(config)
    
    # Mock memory agent
    mock_memory = Mock()
    mock_memory.get_quotes_in_range = AsyncMock(return_value=[
        {
            "quote_id": "Q1", 
            "total_amount": 100.0, 
            "created_date": datetime(2024, 1, 1)
        },
        {
            "quote_id": "Q2", 
            "total_amount": 150.0, 
            "created_date": datetime(2024, 1, 2)
        }
    ])
    agent.set_memory_agent(mock_memory)
    
    return agent

@pytest.mark.asyncio
async def test_quote_trends_analysis(analysis_agent):
    """Test quote trends analysis functionality"""
    result = await analysis_agent.process({
        "analysis_type": "quote_trends",
        "date_range": {
            "start": "2024-01-01",
            "end": "2024-01-31"
        }
    })
    
    assert result["success"] is True
    assert "trend_data" in result["data"]
    assert "insights" in result["data"]

def test_agent_capabilities(analysis_agent):
    """Test agent capabilities reporting"""
    capabilities = analysis_agent.get_capabilities()
    
    assert "quote_trend_analysis" in capabilities
    assert "customer_segmentation" in capabilities
    assert len(capabilities) > 0
```

### 8. Update Documentation

Add documentation for your new agent:

```markdown
# Analysis Agent

Agent responsible for business analytics and data insights.

## Capabilities

* Quote trend analysis
* Customer segmentation  
* Revenue analytics
* Seasonal pattern detection

## Usage

```python
result = await orchestrator.route_request("analysis", {
    "analysis_type": "quote_trends",
    "date_range": {
        "start": "2024-01-01", 
        "end": "2024-01-31"
    }
})
```

## API Endpoints

* `POST /api/v1/analysis/run` - Run analysis
* `GET /api/v1/analysis/types` - Get available analysis types
```

## Best Practices

### Agent Design Principles

1. **Single Responsibility**: Each agent should have a focused purpose
2. **Loose Coupling**: Minimize dependencies between agents
3. **Error Handling**: Graceful failure with meaningful error messages
4. **Configuration**: Use external configuration for flexibility
5. **Testing**: Comprehensive unit and integration tests

### Memory Integration

```python
# Always check if memory agent is available
if not self.memory_agent:
    raise Exception("Memory agent not available")

# Use memory agent for context and persistence
context = self.memory_agent.get_context(session_id)
self.memory_agent.save_analysis_result(result)
```

### Performance Considerations

* Use async/await for I/O operations
* Implement caching for expensive computations
* Limit data retrieval to necessary ranges
* Use background tasks for long-running analyses

### Security and Privacy

* Validate all inputs
* Implement proper access controls
* Anonymize sensitive data in analytics
* Follow data retention policies

## Integration Testing

Test the complete integration:

```python
# tests/test_agent_integration.py

@pytest.mark.asyncio
async def test_new_agent_integration():
    """Test new agent works with orchestrator"""
    orchestrator = AgentOrchestrator()
    
    # Test agent registration
    assert 'analysis' in orchestrator.agents
    
    # Test routing
    result = await orchestrator.route_request("analysis", {
        "analysis_type": "quote_trends",
        "date_range": {"start": "2024-01-01", "end": "2024-01-31"}
    })
    
    assert result["success"] is True
```

By following this guide, you can extend the 925stackai system with new agents that integrate seamlessly with the existing architecture while maintaining code quality and system reliability.
