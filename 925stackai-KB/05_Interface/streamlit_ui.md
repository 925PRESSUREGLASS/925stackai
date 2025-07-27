# Streamlit UI

Web application for chat-based window cleaning quotes and customer interaction.

## Overview

The Streamlit user interface provides an intuitive chat-based experience for customers to request quotes, ask questions, and interact with the 925stackai system. The UI seamlessly integrates with the backend agents to deliver real-time quote generation and natural language assistance.

## Application Structure

### Main Components

```python
def main():
    st.set_page_config(
        page_title="925 Stack AI - Window Cleaning Quotes",
        page_icon="🪟",
        layout="wide"
    )
    
    # Initialize session state
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    if 'current_quote' not in st.session_state:
        st.session_state.current_quote = None
    
    # Render UI components
    render_header()
    render_chat_interface()
    render_sidebar()
    render_footer()
```

### Chat Interface Implementation

```python
def render_chat_interface():
    st.header("💬 Chat with our AI Assistant")
    
    # Display conversation history
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.conversation_history:
            render_message(message)
    
    # Input area
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_area(
            "Type your message...",
            placeholder="E.g., 'I need a quote for 10 windows' or 'What are your rates?'",
            key="user_input"
        )
        
        col1, col2 = st.columns([1, 4])
        with col1:
            submitted = st.form_submit_button("Send")
        
        if submitted and user_input:
            process_user_message(user_input)
```

### Message Processing

```python
def process_user_message(user_input: str):
    # Add user message to history
    st.session_state.conversation_history.append({
        'role': 'user',
        'content': user_input,
        'timestamp': datetime.now()
    })
    
    # Show processing indicator
    with st.spinner("Thinking..."):
        # Route to GUI Agent for processing
        response = gui_agent.process_user_input(
            user_input, 
            st.session_state
        )
    
    # Add assistant response to history
    st.session_state.conversation_history.append({
        'role': 'assistant',
        'content': response.content,
        'quote_data': response.quote_data,
        'timestamp': datetime.now()
    })
    
    # Update current quote if provided
    if response.quote_data:
        st.session_state.current_quote = response.quote_data
    
    # Rerun to show new messages
    st.rerun()
```

## UI Components

### Quote Display Widget

```python
def render_quote_display(quote_data: dict):
    st.subheader("📋 Your Quote")
    
    # Quote summary card
    with st.container():
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.metric("Total Quote", f"${quote_data['total']:.2f}")
        
        with col2:
            st.metric("Windows", quote_data['total_windows'])
        
        with col3:
            st.metric("Property", quote_data['location'])
    
    # Detailed breakdown
    with st.expander("View Detailed Breakdown", expanded=True):
        breakdown_df = pd.DataFrame(quote_data['line_items'])
        st.dataframe(
            breakdown_df,
            column_config={
                "description": "Service",
                "amount": st.column_config.NumberColumn(
                    "Amount",
                    format="$%.2f"
                )
            },
            hide_index=True
        )
```

### Sidebar Information Panel

```python
def render_sidebar():
    with st.sidebar:
        st.header("ℹ️ Quick Info")
        
        # Service area map
        st.subheader("Service Areas")
        st.info("Primary: Cottesloe and surrounding areas\nTravel charges apply beyond 5km")
        
        # Pricing quick reference
        st.subheader("Quick Pricing")
        pricing_data = {
            "Standard Window (both sides)": "$10.00",
            "Large Window (both sides)": "$15.00",
            "Exterior Only": "$6.00",
            "Base Fee": "$80.00",
            "Travel Fee": "$10.00+"
        }
        
        for service, price in pricing_data.items():
            st.write(f"**{service}:** {price}")
        
        # Contact information
        st.subheader("Contact")
        st.write("📞 Phone: [Your Number]")
        st.write("📧 Email: [Your Email]")
        st.write("🌐 Website: [Your Website]")
```

### Message Rendering

```python
def render_message(message: dict):
    if message['role'] == 'user':
        with st.chat_message("user"):
            st.write(message['content'])
            st.caption(f"Sent at {message['timestamp'].strftime('%H:%M')}")
    
    else:  # assistant
        with st.chat_message("assistant"):
            st.write(message['content'])
            
            # Show quote if included
            if message.get('quote_data'):
                render_quote_display(message['quote_data'])
            
            st.caption(f"Reply at {message['timestamp'].strftime('%H:%M')}")
```

## Advanced Features

### Real-time Input Validation

```python
def validate_user_input(input_text: str) -> dict:
    """Provide real-time feedback on user inputs"""
    validation = {
        'is_valid': True,
        'warnings': [],
        'suggestions': []
    }
    
    # Check for common patterns
    if re.search(r'\d+\s*windows?', input_text.lower()):
        validation['suggestions'].append("Great! I can help with your window quote.")
    
    # Check for location mentions
    if not re.search(r'(suburb|address|location)', input_text.lower()):
        validation['warnings'].append("Consider mentioning your location for travel costs.")
    
    return validation
```

### Progressive Form Filling

```python
def render_guided_quote_form():
    """Alternative interface for structured quote input"""
    st.subheader("🎯 Quick Quote Form")
    
    with st.form("quote_form"):
        # Location input
        location = st.text_input("Property Location", placeholder="Suburb or address")
        
        # Window details
        st.write("**Window Details**")
        col1, col2 = st.columns(2)
        
        with col1:
            standard_windows = st.number_input("Standard Windows", min_value=0, value=0)
            large_windows = st.number_input("Large Windows", min_value=0, value=0)
        
        with col2:
            cleaning_sides = st.selectbox("Cleaning", ["Both Sides", "Exterior Only", "Interior Only"])
            building_stories = st.selectbox("Building Height", ["Single Story", "Two Story", "Three+ Stories"])
        
        # Service options
        st.write("**Service Options**")
        cleaning_level = st.selectbox(
            "Cleaning Level",
            ["Standard", "Light Clean", "Deep Clean", "Post-Construction"]
        )
        
        urgency = st.selectbox("Urgency", ["Standard", "Same Day", "Urgent (< 4 hours)"])
        
        # Submit button
        submitted = st.form_submit_button("Get Quote")
        
        if submitted:
            # Convert form data to structured request
            quote_request = build_quote_request_from_form(
                location, standard_windows, large_windows,
                cleaning_sides, building_stories, cleaning_level, urgency
            )
            
            # Process quote
            process_quote_request(quote_request)
```

### Session Management

```python
def initialize_session():
    """Initialize session state variables"""
    defaults = {
        'conversation_history': [],
        'current_quote': None,
        'user_preferences': {},
        'session_id': str(uuid.uuid4()),
        'start_time': datetime.now()
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def save_session_data():
    """Persist session data for future visits"""
    session_data = {
        'session_id': st.session_state.session_id,
        'conversation_history': st.session_state.conversation_history,
        'user_preferences': st.session_state.user_preferences,
        'last_active': datetime.now().isoformat()
    }
    
    # Save to memory agent
    memory_agent.save_session(session_data)
```

## Deployment Configuration

### Production Settings

```python
# config/streamlit_config.toml
[server]
port = 8501
enableCORS = false
enableWebsocketCompression = true

[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"

[browser]
gatherUsageStats = false
```

### Environment Variables

```python
def load_config():
    """Load configuration from environment"""
    config = {
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
        'MEMORY_STORAGE_PATH': os.getenv('MEMORY_STORAGE_PATH', './data/memory'),
        'DEBUG_MODE': os.getenv('DEBUG_MODE', 'false').lower() == 'true',
        'MAX_CONVERSATION_LENGTH': int(os.getenv('MAX_CONVERSATION_LENGTH', '50'))
    }
    
    return config
```

## Performance Optimizations

### Caching Strategy

```python
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_pricing_data():
    """Cache pricing structure for quick access"""
    return pricing_loader.load_current_pricing()

@st.cache_resource
def initialize_agents():
    """Cache agent initialization"""
    return AgentOrchestrator()
```

### Responsive Design

The UI adapts to different screen sizes using Streamlit's responsive column system and mobile-friendly components.

For API integration details, see [API Endpoints Documentation](api_endpoints.md).
