## Repository Optimization

**Symptoms:** Slow workflow, large repo size, unnecessary files, or code quality issues

**Minimization Tips:**
- Delete unused files and dependencies
- Use `.gitignore` for non-essential files
- Refactor to remove duplicate code
- List only required packages in `requirements.txt`
- Store large assets externally if possible
- Keep docs concise and relevant

# GUI Agent

Coordinates the Streamlit UI interactions and manages the flow between user interface and backend agents.

## Overview

The GUI Agent serves as the orchestration layer between the Streamlit web interface and the specialized backend agents. It handles user input routing, response formatting, and maintains the conversational flow within the web application.

## Core Responsibilities

### Input Processing and Routing

The GUI Agent analyzes incoming user messages to determine the appropriate response pathway:

```python
def process_user_input(self, message: str, session_state: dict) -> Response:
    # Determine intent from user message
    intent = self.classify_intent(message)
    
    if intent == 'quote_request':
        return self.handle_quote_request(message, session_state)
    elif intent == 'question':
        return self.handle_general_question(message, session_state)
    elif intent == 'clarification':
        return self.handle_clarification(message, session_state)
    else:
        return self.handle_fallback(message, session_state)
```

### Agent Coordination

Manages interactions between specialized agents:

- **Quote Requests**: Routes to Quoting Agent with Memory Agent context
- **Follow-up Questions**: Combines Memory Agent history with appropriate specialist
- **Error Handling**: Provides user-friendly error messages and suggested actions

### Session Management

Maintains conversation state across Streamlit interactions:

```python
class SessionManager:
    def __init__(self):
        self.conversation_history = []
        self.current_quote_context = {}
        self.user_preferences = {}
    
    def add_exchange(self, user_input: str, agent_response: str):
        self.conversation_history.append({
            'timestamp': datetime.now(),
            'user': user_input,
            'assistant': agent_response,
            'context': self.current_quote_context.copy()
        })
```

## UI Component Management

### Chat Interface

Handles the primary chat experience:

- Message display with proper formatting
- Quote breakdown visualization
- Progress indicators for long-running calculations
- Error state management

### Quote Display

Specialized formatting for quote responses:

```python
def format_quote_display(self, quote_data: dict) -> str:
    formatted = f"""
    ## Quote Summary
    
    **Property**: {quote_data['location']}
    **Total**: ${quote_data['total']:.2f}
    
    ### Breakdown:
    """
    
    for item in quote_data['line_items']:
        formatted += f"- {item['description']}: ${item['amount']:.2f}\n"
    
    return formatted
```

### Input Validation

Provides real-time feedback on user inputs:

- Window count validation
- Location format checking
- Service type verification
- Scheduling constraint validation


## Knowledge Base (KB) Integration

### Default Integration Pattern

The GUI Agent and backend agents can leverage the `925stackai-KB` folder as a structured knowledge base for quoting, help, and contextual responses.

**How it works:**

1. **Loading the KB**: On startup, the system loads all Markdown files from `925stackai-KB` into memory (as text or parsed sections).
2. **Search/Retrieval**: When a user asks a question or requests a quote, the agent searches the KB for relevant sections using keyword or semantic search.
3. **Agent Usage**: The agent can:
   - Provide direct answers from the KB (e.g., quoting rules, service descriptions)
   - Display KB content in the Streamlit UI (e.g., help, tooltips, explanations)
   - Use KB context to enhance quoting, validation, or recommendations
4. **UI Display**: The Streamlit UI can show KB snippets, FAQs, or explanations inline or on demand.

**Example (Python pseudocode):**

```python
from pathlib import Path

def load_kb(folder="925stackai-KB"):
    kb = {}
    for md_file in Path(folder).rglob("*.md"):
        kb[md_file.stem] = md_file.read_text(encoding="utf-8")
    return kb

def search_kb(kb, query):
    # Simple keyword search (replace with semantic search as needed)
    results = []
    for title, content in kb.items():
        if query.lower() in content.lower():
            results.append((title, content))
    return results

# Usage in agent logic
kb = load_kb()
matches = search_kb(kb, user_input)
if matches:
    display_to_user(matches[0][1])
```

**Best Practices:**
- Keep KB files organized by topic (quoting, pricing, troubleshooting, etc.)
- Use clear headings and structure in Markdown for easy parsing
- Update KB as business logic or FAQs evolve

See also: [Troubleshooting Guide](../06_Deploy/troubleshooting.md), [Docker Guide](docker_guide.md)

## Integration Patterns
### Memory Integration

Leverages Memory Agent for enhanced user experience:

```python
def enhance_with_memory(self, user_input: str, session_id: str):
    # Retrieve relevant context
    context = self.memory_agent.retrieve_context(user_input, session_id)
    
    # Pre-populate known information
    if context.get('user_profile'):
        self.prefill_user_data(context['user_profile'])
    
    # Suggest based on history
    if context.get('recent_quotes'):
        self.suggest_similar_services(context['recent_quotes'])
```

### Error Recovery

Graceful handling of system errors:

- Fallback to basic quoting when AI agents are unavailable
- Clear error messages with suggested workarounds
- Automatic retry mechanisms for transient failures

## User Experience Features

### Progressive Disclosure

Guides users through complex quoting scenarios:

1. Initial request capture
2. Clarification questions as needed
3. Option presentation with recommendations
4. Final quote confirmation

### Contextual Help

Dynamic assistance based on current interaction:

- Tooltip explanations for window types
- Pricing methodology transparency
- Service area and travel charge information

### Natural Text Chat Query

Enables users to interact with the system using free-form natural language queries via a chat interface.

**How it works:**

1. The Streamlit UI provides a chat input box for users to type questions or requests.
2. On submit, the message is passed to the agent's `process_user_input` method.
3. If the intent is a question or help request, the agent uses the KB search logic to find and display relevant answers.
4. The conversation is displayed in a chat-like format, showing both user and agent messages.

**Example (Streamlit snippet):**

```python
import streamlit as st

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

user_input = st.chat_input('Ask a question or request a quote...')
if user_input:
    # Process input and get response (pseudo-code)
    response = agent.process_user_input(user_input, st.session_state)
    st.session_state['chat_history'].append({'user': user_input, 'assistant': response})

for exchange in st.session_state['chat_history']:
    st.chat_message('user').write(exchange['user'])
    st.chat_message('assistant').write(exchange['assistant'])
```

This enables natural language querying and conversational interaction with the agent, leveraging the knowledge base and quoting logic.
- Service area and travel charge information

### Response Formatting

Ensures consistent, professional output:

- Markdown formatting for quotes
- Structured tables for comparisons
- Visual emphasis for key information
- Mobile-responsive design considerations

## Performance Optimization

- Lazy loading of conversation history
- Efficient state management in Streamlit
- Background processing for complex calculations
- Caching of frequently requested information

For detailed UI implementation, see [Streamlit UI Documentation](../05_Interface/streamlit_ui.md).
