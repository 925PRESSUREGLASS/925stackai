# Memory Persistence

How the system stores and retrieves conversational memory and user context.

## Overview

The memory persistence layer provides both semantic search capabilities through vector storage and structured data retrieval through JSON storage. This dual approach enables rich contextual understanding while maintaining precise access to specific user information.

## Storage Architecture

### Vector Storage (FAISS)

Used for semantic similarity search of conversation history:

```python
class VectorMemoryStore:
    def __init__(self, dimension: int = 384):
        self.index = faiss.IndexFlatIP(dimension)
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.metadata = {}
    
    def add_memory(self, memory_id: str, text: str, metadata: dict):
        # Generate embedding for the text
        embedding = self.embedder.encode([text])
        
        # Add to FAISS index
        self.index.add(embedding)
        
        # Store metadata separately
        self.metadata[memory_id] = {
            'text': text,
            'metadata': metadata,
            'index_position': self.index.ntotal - 1
        }
```

### JSON Storage (Structured Data)

Maintains precise user profiles and quote history:

```python
class JSONMemoryStore:
    def __init__(self, storage_path: str):
        self.storage_path = storage_path
        self.user_profiles = {}
        self.quote_history = {}
        self.conversation_logs = {}
    
    def save_user_profile(self, user_id: str, profile: dict):
        self.user_profiles[user_id] = {
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'preferences': profile.get('preferences', {}),
            'contact_info': profile.get('contact_info', {}),
            'property_details': profile.get('property_details', [])
        }
        self._persist_to_disk()
```

## Memory Operations

### Adding New Memories

```python
def store_conversation_exchange(self, session_id: str, exchange: dict):
    # Extract key information
    memory_text = f"User: {exchange['user_input']} Assistant: {exchange['assistant_response']}"
    
    # Create metadata
    metadata = {
        'session_id': session_id,
        'timestamp': exchange['timestamp'],
        'user_input': exchange['user_input'],
        'assistant_response': exchange['assistant_response'],
        'quote_data': exchange.get('quote_data'),
        'context_type': self._classify_context(exchange)
    }
    
    # Store in vector index for semantic search
    memory_id = f"{session_id}_{exchange['timestamp']}"
    self.vector_store.add_memory(memory_id, memory_text, metadata)
    
    # Store structured data for precise retrieval
    if metadata['quote_data']:
        self.json_store.save_quote_history(session_id, metadata['quote_data'])
```

### Semantic Memory Retrieval

```python
def search_similar_conversations(self, query: str, user_id: str, k: int = 5) -> List[dict]:
    # Generate query embedding
    query_embedding = self.embedder.encode([query])
    
    # Search FAISS index
    similarities, indices = self.vector_store.index.search(query_embedding, k * 2)
    
    # Filter by user_id and return relevant memories
    relevant_memories = []
    for i, idx in enumerate(indices[0]):
        if idx >= 0:  # Valid index
            memory_data = self.vector_store.get_memory_by_index(idx)
            if memory_data['metadata'].get('user_id') == user_id:
                memory_data['similarity_score'] = similarities[0][i]
                relevant_memories.append(memory_data)
                
                if len(relevant_memories) >= k:
                    break
    
    return relevant_memories
```

### Structured Data Queries

```python
def get_user_context(self, user_id: str) -> dict:
    """Retrieve comprehensive user context"""
    context = {
        'profile': self.json_store.get_user_profile(user_id),
        'recent_quotes': self.json_store.get_recent_quotes(user_id, limit=5),
        'conversation_summary': self.json_store.get_conversation_summary(user_id),
        'preferences': self.json_store.get_user_preferences(user_id)
    }
    
    return context

def get_quote_history(self, user_id: str, property_address: str = None) -> List[dict]:
    """Get historical quotes, optionally filtered by property"""
    quotes = self.json_store.get_quotes_by_user(user_id)
    
    if property_address:
        quotes = [q for q in quotes if q.get('property_address') == property_address]
    
    return sorted(quotes, key=lambda x: x['created_at'], reverse=True)
```

## Memory Types and Indexing

### Conversation Memory

Indexed by:
- Session ID for temporal grouping
- User ID for privacy boundaries
- Topic classification (quote request, question, complaint, etc.)
- Temporal windows (recent, this week, this month)

### User Profile Memory

Organized by:
- Contact information and preferences
- Property profiles with typical window configurations
- Service history and frequency patterns
- Pricing preferences and budget considerations

### Quote Memory

Structured storage including:
- Complete quote breakdowns with line items
- Customer requirements and specifications
- Acceptance/rejection status
- Follow-up communications

## Performance Optimization

### Indexing Strategy

```python
def optimize_memory_performance(self):
    # Create temporal indices for quick recent access
    self._create_temporal_index('last_24h')
    self._create_temporal_index('last_week')
    self._create_temporal_index('last_month')
    
    # Topic-based clustering for semantic efficiency
    self._cluster_by_topic(['quote_requests', 'general_questions', 'complaints'])
    
    # User-specific indices for privacy and speed
    self._create_user_indices()

def _create_temporal_index(self, time_window: str):
    """Create optimized indices for temporal queries"""
    cutoff_time = self._get_cutoff_time(time_window)
    recent_memories = [
        m for m in self.memories 
        if m['timestamp'] >= cutoff_time
    ]
    
    # Create specialized FAISS index for recent memories
    recent_index = faiss.IndexFlatIP(self.dimension)
    for memory in recent_memories:
        recent_index.add(memory['embedding'])
    
    self.temporal_indices[time_window] = recent_index
```

### Caching Strategy

```python
class MemoryCache:
    def __init__(self, max_size: int = 1000):
        self.cache = {}
        self.access_order = deque(maxlen=max_size)
        self.max_size = max_size
    
    def get_user_context(self, user_id: str) -> dict:
        cache_key = f"user_context_{user_id}"
        
        if cache_key in self.cache:
            # Move to end of access order
            self.access_order.remove(cache_key)
            self.access_order.append(cache_key)
            return self.cache[cache_key]
        
        # Load from storage and cache
        context = self.memory_store.get_user_context(user_id)
        self._cache_with_eviction(cache_key, context)
        return context
```

## Data Privacy and Security

### Encryption at Rest

```python
def encrypt_memory_data(self, data: dict) -> bytes:
    """Encrypt sensitive memory data before storage"""
    serialized = json.dumps(data).encode('utf-8')
    
    # Use Fernet for symmetric encryption
    cipher_suite = Fernet(self.encryption_key)
    encrypted_data = cipher_suite.encrypt(serialized)
    
    return encrypted_data

def decrypt_memory_data(self, encrypted_data: bytes) -> dict:
    """Decrypt memory data for use"""
    cipher_suite = Fernet(self.encryption_key)
    decrypted_data = cipher_suite.decrypt(encrypted_data)
    
    return json.loads(decrypted_data.decode('utf-8'))
```

### Data Retention Policies

```python
def apply_retention_policy(self):
    """Remove old data according to retention policies"""
    current_time = datetime.now()
    
    # Remove conversation memories older than 2 years
    old_conversations = [
        m for m in self.memories 
        if (current_time - m['timestamp']).days > 730
    ]
    
    for memory in old_conversations:
        self.remove_memory(memory['id'])
    
    # Archive old quote data (keep for 7 years for business records)
    self.archive_old_quotes(cutoff_days=2555)  # 7 years
```

## Integration with Agents

The memory persistence layer integrates with all agents through a unified interface:

```python
class MemoryInterface:
    def __init__(self, vector_store: VectorMemoryStore, json_store: JSONMemoryStore):
        self.vector_store = vector_store
        self.json_store = json_store
    
    def get_context_for_agent(self, agent_type: str, user_id: str, query: str) -> dict:
        """Provide agent-specific context"""
        if agent_type == 'quoting':
            return self._get_quoting_context(user_id, query)
        elif agent_type == 'gui':
            return self._get_gui_context(user_id, query)
        else:
            return self._get_general_context(user_id, query)
```

For agent-specific usage patterns, see the individual agent documentation in [02_Agents](../02_Agents/).
