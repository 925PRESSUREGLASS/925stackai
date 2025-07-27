# System Overview

*A modular AI agent orchestration system for window cleaning quote generation with persistent memory and natural language interaction.*

## Architecture Overview

925stackai is built on a distributed agent architecture that leverages LangChain and Ollama for local LLM processing. The system consists of specialized agents that work together to provide intelligent quoting services through a Streamlit web interface.

## Core Components

### Agent Orchestration
The system uses a hub-and-spoke model where individual agents handle specific responsibilities:
- **Quoting Agent**: Processes window cleaning requests and generates accurate quotes
- **Memory Agent**: Manages persistent conversational context and user preferences
- **GUI Agent**: Coordinates interactions between the Streamlit UI and backend services
- **Evaluation Agent**: Performs system testing and quality assessment

### Data Flow Architecture

```python
User Input (Streamlit) 
    ↓
GUI Agent (coordination)
    ↓
Memory Agent (context retrieval) + Quoting Agent (price calculation)
    ↓
Quote Calculation Engine (pricing logic)
    ↓
Response Generation (formatted output)
    ↓
Streamlit UI (display results)
```

### Persistent Memory System
- **FAISS Vector Store**: Semantic search of conversation history
- **JSON Storage**: Structured data persistence for user preferences and quote history
- **ChromaDB**: Document embeddings for knowledge retrieval

## Technology Stack

- **Backend**: Python 3.11+ with LangChain framework
- **Local LLM**: Ollama (Llama 3) for offline AI processing
- **Vector Storage**: FAISS and ChromaDB for embeddings
- **Frontend**: Streamlit for web-based chat interface
- **API Layer**: FastAPI for RESTful endpoints
- **Testing**: pytest with mypy for type checking

## Integration Points

The system is designed for modularity with clear interfaces between components. New agents can be added by implementing the base agent protocol and registering with the orchestrator. The pricing engine is externalized to allow easy updates to business logic without affecting the AI components.

For detailed information on specific agents, see the [02_Agents](../02_Agents/) documentation.
