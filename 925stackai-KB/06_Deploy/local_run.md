# Local Run Guide

Set up and run 925stackai on a local development machine.

## Prerequisites

### System Requirements

* **Python**: 3.11 or higher
* **Memory**: Minimum 8GB RAM (16GB recommended for Ollama)
* **Storage**: 10GB free space for models and data
* **OS**: Windows 10/11, macOS 10.15+, or Linux (Ubuntu 20.04+)

### Required Software

1. **Git** - for cloning the repository
2. **Python 3.11+** - with pip package manager
3. **Ollama** - for local LLM inference (optional but recommended)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/925PRESSUREGLASS/925stackai.git
cd 925stackai
```

### 2. Set Up Python Environment

Create and activate a virtual environment:

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
# Install core dependencies
pip install -r requirements.txt

# Install development dependencies (optional)
pip install -r requirements-dev.txt
```

### 4. Environment Configuration

Create a `.env` file in the project root:

```bash
# Copy the example environment file
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# Application Settings
DEBUG=true
LOG_LEVEL=INFO

# API Configuration
API_HOST=127.0.0.1
API_PORT=8000
STREAMLIT_PORT=8501

# Memory Storage
MEMORY_STORAGE_PATH=./data/memory
VECTOR_STORE_PATH=./data/vectors

# LLM Configuration
OLLAMA_BASE_URL=http://localhost:11434
DEFAULT_MODEL=llama3

# Optional: External LLM APIs
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here

# Security
API_SECRET_KEY=your_secret_key_here
ENCRYPTION_KEY=your_encryption_key_here
```

### 5. Initialize Data Storage

```bash
# Create necessary directories
mkdir -p data/memory data/vectors data/quotes

# Initialize the database
python scripts/init_database.py
```

### 6. Install and Configure Ollama (Recommended)

Install Ollama from [ollama.ai](https://ollama.ai):

```bash
# Download and install the Llama 3 model
ollama pull llama3

# Start Ollama service (if not auto-started)
ollama serve
```

## Running the Application

### Method 1: Using the Batch Script (Windows)

```bash
# Run everything with one command
.\run_all.bat
```

This script will:
- Activate the virtual environment
- Install any missing dependencies
- Start the FastAPI backend
- Launch the Streamlit frontend
- Open browser windows for both interfaces

### Method 2: Manual Startup

Start each component separately:

#### Terminal 1: FastAPI Backend

```bash
# Activate environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Start the API server
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

#### Terminal 2: Streamlit Frontend

```bash
# Activate environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Start Streamlit
streamlit run gui/app.py --server.port 8501
```

### Method 3: Development Mode

For development with auto-reload:

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run with development settings
python -m uvicorn app.main:app --reload --log-level debug
```

## Accessing the Application

Once running, access the application through:

* **Streamlit UI**: http://localhost:8501
* **FastAPI Docs**: http://localhost:8000/docs
* **API Endpoints**: http://localhost:8000/api/v1/
* **Health Check**: http://localhost:8000/api/v1/health

## Initial Testing

### Test Quote Generation

Use the Streamlit interface to test basic functionality:

1. Open http://localhost:8501
2. Type: "I need a quote for 8 windows"
3. Verify the system responds with a quote breakdown

### Test API Endpoints

```bash
# Test health endpoint
curl http://localhost:8000/api/v1/health

# Test quote generation
curl -X POST "http://localhost:8000/api/v1/quote" \
     -H "Content-Type: application/json" \
     -H "X-API-Key: your-api-key" \
     -d '{
       "location": "Cottesloe",
       "windows": [
         {"type": "standard", "count": 8, "sides": "both", "story": 1}
       ]
     }'
```

## Data Initialization

### Load Sample Data

```bash
# Load sample quotes and pricing data
python scripts/load_sample_data.py

# Initialize vector store with example conversations
python scripts/init_vector_store.py
```

### Import Custom Pricing

```bash
# Import your pricing structure
python scripts/import_pricing.py --file data/pricing/custom_rates.json
```

## Configuration Options

### Streamlit Configuration

Edit `.streamlit/config.toml`:

```toml
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

### Logging Configuration

Edit `config/logging.yaml`:

```yaml
version: 1
disable_existing_loggers: false

formatters:
  standard:
    format: '%(asctime)s [%(levelname)s] %(name)s: %(message)s'

handlers:
  console:
    class: logging.StreamHandler
    level: INFO
    formatter: standard
    stream: ext://sys.stdout

  file:
    class: logging.FileHandler
    level: DEBUG
    formatter: standard
    filename: logs/app.log

loggers:
  925stackai:
    level: DEBUG
    handlers: [console, file]
    propagate: false

root:
  level: INFO
  handlers: [console]
```

## Development Workflow

### Code Quality Tools

```bash
# Run type checking
mypy app/ gui/ tests/

# Format code
black app/ gui/ tests/

# Run linting
flake8 app/ gui/ tests/

# Run tests
pytest tests/ -v --cov=app
```

### Git Hooks (Optional)

Set up pre-commit hooks:

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run on all files
pre-commit run --all-files
```

## Performance Optimization

### For Development

* Use SQLite for local database (faster startup)
* Limit conversation history in memory
* Use smaller LLM models for testing

### For Production-like Testing

* Use PostgreSQL database
* Enable full memory persistence
* Test with production-sized models

## Backup and Data Management

### Backup User Data

```bash
# Backup conversation data
python scripts/backup_conversations.py --output backups/conversations_$(date +%Y%m%d).json

# Backup user profiles
python scripts/backup_profiles.py --output backups/profiles_$(date +%Y%m%d).json
```

### Reset Development Data

```bash
# Clear all conversations and quotes
python scripts/reset_dev_data.py --confirm

# Reinitialize with sample data
python scripts/load_sample_data.py
```

For deployment to production environments, see the [Docker Guide](docker_guide.md) and [Troubleshooting](troubleshooting.md) documentation.
