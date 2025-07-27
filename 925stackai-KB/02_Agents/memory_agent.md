# Memory Agent

Manages persistent conversational memory and user context across interactions.

## Overview

The Memory Agent is responsible for maintaining conversation history, user preferences, and contextual information that enhances the quoting experience. It uses a combination of vector storage for semantic search and structured JSON storage for precise data retrieval.

## Core Components

### Vector Storage (FAISS)

Enables semantic search of conversation history:
- Stores embedded conversation snippets
- Retrieves relevant context based on similarity
- Maintains conversation threading across sessions

### JSON Storage

Structured persistence for:
- User profiles and preferences
- Quote history with detailed breakdowns
- Window configuration templates
- Customer contact information

## Memory Operations

### Saving Conversation Context

```python
def save_memory(self, conversation_id: str, content: dict):
    # Save to vector store for semantic retrieval
    embedding = self.embedder.embed(content['text'])
    self.vector_store.add(
        id=conversation_id,
        embedding=embedding,
        metadata=content
    )
    
    # Save structured data to JSON
    self.json_store.update(conversation_id, {
        'timestamp': content['timestamp'],
        'user_input': content['user_input'],
        'quote_result': content['quote_result'],
        'preferences': content.get('preferences', {})
    })
```

### Context Retrieval

```python
def retrieve_context(self, query: str, user_id: str) -> List[dict]:
    # Semantic search for relevant conversations
    query_embedding = self.embedder.embed(query)
    similar_memories = self.vector_store.search(
        query_embedding, 
        filter={'user_id': user_id},
        k=5
    )
    
    # Combine with structured user data
    user_profile = self.json_store.get_user_profile(user_id)
    
    return {
        'similar_conversations': similar_memories,
        'user_profile': user_profile,
        'recent_quotes': self.get_recent_quotes(user_id)
    }
```

## Memory Types

### Conversation Memory

Short-term context within a chat session:
- Current quote parameters
- Clarification questions and responses
- Progressive refinement of requirements

### User Preferences

Long-term patterns and preferences:
- Typical window configurations
- Preferred cleaning frequency
- Budget considerations
- Service history

### Quote History

Detailed records of past quotes:
- Window counts and types
- Final pricing breakdowns
- Service dates and completion status
- Customer satisfaction feedback

## Integration with Other Agents

### Quoting Agent Integration

The Memory Agent provides context to enhance quote accuracy:
- Previous window configurations for the same property
- Customer preferences for cleaning level
- Historical pricing for comparison

### GUI Agent Coordination

Seamless user experience through:
- Pre-populating forms with known information
- Suggesting common configurations
- Displaying relevant quote history

## Data Privacy and Retention

- All personal data encrypted at rest
- Configurable retention periods for different data types
- GDPR-compliant data deletion capabilities
- Anonymous usage analytics for system improvement

## Performance Optimization

- Lazy loading of conversation history
- Efficient indexing strategies for vector search
- Caching of frequently accessed user profiles
- Background cleanup of outdated memory entries

For technical implementation details, see [Memory Persistence](../04_Logic/memory_persistence.md).
