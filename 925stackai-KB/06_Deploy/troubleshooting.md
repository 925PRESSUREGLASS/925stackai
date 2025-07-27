## Repository Optimization

### **Optimizing Your Repository**

**Symptoms**: Slow development workflow, large repository size, unnecessary files, or code quality issues

**Solutions**:

1. **Clean Python Cache and Temporary Files**
   - Remove all `.pyc` files and `__pycache__` directories:
     - **Windows (PowerShell):**
       ```powershell
       Get-ChildItem -Path . -Include *.pyc -Recurse | Remove-Item -Force
       Get-ChildItem -Path . -Include __pycache__ -Recurse | Remove-Item -Recurse -Force
       ```
     - **Linux/macOS (Bash):**
       ```bash
       find . -name "*.pyc" -delete
       find . -name "__pycache__" -type d -exec rm -rf {} +
       ```

2. **Remove Unused Dependencies**
   - Review your `requirements.txt` or `pyproject.toml` and uninstall unused packages:
     ```bash
     pip uninstall <package-name>
     ```

3. **Format and Lint Code**
   - Use tools like `black`, `ruff`, or `flake8` to auto-format and lint your code:
     ```bash
     black .
     ruff .
     flake8 .
     ```

4. **Check for Large or Unnecessary Files**
   - Identify large files:
     - **Windows (PowerShell):**
       ```powershell
       Get-ChildItem -Path . -Recurse | Sort-Object Length -Descending | Select-Object -First 20 Name,Length
       ```
     - **Linux/macOS (Bash):**
       ```bash
       du -ah . | sort -rh | head -n 20
       ```

5. **.gitignore Hygiene**
   - Ensure your `.gitignore` excludes virtual environments, cache, logs, and other non-source files.

6. **Rebuild and Optimize Vector Store**
   - Periodically rebuild your vector store for efficiency:
     ```bash
     python scripts/optimize_vector_store.py
     ```

7. **Vacuum and Optimize Database (if using SQLite)**
   - For SQLite:
     ```bash
     sqlite3 <your_db_file>.db 'VACUUM;'
     ```

**Tip:** Regularly run these steps to keep your repository clean, fast, and maintainable.
# Troubleshooting Guide

Common issues and solutions for the 925stackai system.

## General Issues

### **Application Won't Start**

**Symptoms**: Error messages during startup, services not responding

**Solutions**:

1. **Check Python Version**
   ```bash
   python --version  # Should be 3.11+
   ```

2. **Verify Virtual Environment**
   ```bash
   which python  # Should point to venv
   pip list | grep streamlit  # Verify dependencies
   ```

3. **Check Port Conflicts**
   ```bash
   # Windows
   netstat -an | findstr :8501
   netstat -an | findstr :8000
   
   # macOS/Linux
   lsof -i :8501
   lsof -i :8000
   ```

4. **Clear Python Cache**
   ```bash
   find . -name "*.pyc" -delete
   find . -name "__pycache__" -type d -exec rm -rf {} +
   ```

### **Memory or Performance Issues**

**Symptoms**: Slow responses, out-of-memory errors, high CPU usage

**Solutions**:

1. **Check Available Memory**
   ```bash
   # Windows
   wmic OS get TotalVisibleMemorySize,FreePhysicalMemory
   
   # macOS/Linux
   free -h
   ```

2. **Reduce Model Size**
   ```python
   # In config/model_config.py
   MODEL_CONFIG = {
       'model_name': 'llama3:8b',  # Use smaller model
       'max_tokens': 1024,  # Reduce token limit
       'temperature': 0.7
   }
   ```

3. **Limit Conversation History**
   ```python
   # In config/app_config.py
   MAX_CONVERSATION_LENGTH = 20  # Reduce from default 50
   MEMORY_CACHE_SIZE = 100  # Reduce cache size
   ```

## Streamlit UI Issues

### **Blank or White Screen**

**Symptoms**: Streamlit loads but shows empty page

**Solutions**:

1. **Check Browser Console**
   - Open Developer Tools (F12)
   - Look for JavaScript errors in Console tab
   - Check Network tab for failed requests

2. **Clear Browser Cache**
   ```bash
   # Or use Ctrl+Shift+R for hard refresh
   ```

3. **Verify Streamlit Configuration**
   ```bash
   # Check .streamlit/config.toml
   streamlit config show
   ```

4. **Test with Different Browser**
   - Try Chrome, Firefox, or Edge
   - Disable browser extensions temporarily

### **Connection Errors**

**Symptoms**: "Connection failed" or timeout errors

**Solutions**:

1. **Check Streamlit Process**
   ```bash
   # Windows
   tasklist | findstr "streamlit"
   
   # macOS/Linux
   ps aux | grep streamlit
   ```

2. **Restart Streamlit**
   ```bash
   # Kill existing process
   pkill -f streamlit
   
   # Restart
   streamlit run gui/app.py --server.port 8501
   ```

3. **Check Firewall Settings**
   - Ensure ports 8501 and 8000 are not blocked
   - Add exceptions for Python/Streamlit if needed

## API and Backend Issues

### **Quote Calculation Errors**

**Symptoms**: Incorrect prices, missing quote breakdowns

**Solutions**:

1. **Verify Pricing Data**
   ```bash
   python scripts/validate_pricing.py
   ```

2. **Check Calculation Logic**
   ```python
   # Test in Python console
   from app.logic.quote_engine import QuoteEngine
   engine = QuoteEngine()
   
   # Test simple quote
   test_result = engine.calculate_simple_quote(
       windows=8, 
       location="Cottesloe"
   )
   print(test_result)
   ```

3. **Review Log Files**
   ```bash
   tail -f logs/app.log | grep "quote"
   ```

### **Memory/Database Errors**

**Symptoms**: "Database connection failed", memory retrieval errors

**Solutions**:

1. **Check Database Connection**
   ```python
   # Test database connectivity
   python scripts/test_db_connection.py
   ```

2. **Rebuild Vector Store**
   ```bash
   python scripts/rebuild_vector_store.py
   ```

3. **Clear Memory Cache**
   ```bash
   rm -rf data/memory/cache/*
   python scripts/init_memory.py
   ```

## LLM and AI Issues

### **Ollama Not Working**

**Symptoms**: "Model not found", connection refused to localhost:11434

**Solutions**:

1. **Check Ollama Service**
   ```bash
   # Check if Ollama is running
   curl http://localhost:11434/api/tags
   
   # Start Ollama if not running
   ollama serve
   ```

2. **Verify Model Installation**
   ```bash
   ollama list
   
   # Install if missing
   ollama pull llama3
   ```

3. **Test Model Directly**
   ```bash
   ollama run llama3 "Hello, can you help with window cleaning quotes?"
   ```

### **Slow AI Responses**

**Symptoms**: Long wait times for quote generation

**Solutions**:

1. **Use Smaller Model**
   ```bash
   # Switch to faster model
   ollama pull llama3:8b
   ```

2. **Optimize Prompts**
   ```python
   # In app/agents/prompts.py
   QUOTE_PROMPT = """
   Brief prompt here...  # Reduce prompt length
   """
   ```

3. **Enable Response Caching**
   ```python
   # In config/cache_config.py
   ENABLE_RESPONSE_CACHE = True
   CACHE_TTL = 3600  # 1 hour
   ```

## Docker Issues

### **Container Won't Start**

**Symptoms**: Docker containers exit immediately or fail to start

**Solutions**:

1. **Check Docker Logs**
   ```bash
   docker-compose logs app
   docker-compose logs ollama
   ```

2. **Verify Docker Resources**
   ```bash
   docker system df
   docker system prune  # Clean up if needed
   ```

3. **Check Environment Variables**
   ```bash
   docker-compose config  # Validate compose file
   ```

### **Volume Mount Issues**

**Symptoms**: Data not persisting, permission errors

**Solutions**:

1. **Fix Permissions**
   ```bash
   # Linux/macOS
   sudo chown -R $USER:$USER data/
   chmod -R 755 data/
   ```

2. **Recreate Volumes**
   ```bash
   docker-compose down -v
   docker-compose up -d
   ```

## Environment-Specific Issues

### **Windows-Specific Problems**

1. **Path Length Limitations**
   ```bash
   # Enable long paths in Windows
   git config --system core.longpaths true
   ```

2. **PowerShell Execution Policy**
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

3. **Windows Defender Interference**
   - Add project folder to Windows Defender exclusions
   - Temporarily disable real-time protection for testing

### **macOS-Specific Problems**

1. **SSL Certificate Issues**
   ```bash
   # Install certificates
   /Applications/Python\ 3.11/Install\ Certificates.command
   ```

2. **Homebrew Python Conflicts**
   ```bash
   # Use system Python or pyenv
   which python3
   python3 -m venv venv  # Use python3 explicitly
   ```

### **Linux-Specific Problems**

1. **Package Dependencies**
   ```bash
   # Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install python3-dev python3-pip build-essential
   
   # CentOS/RHEL
   sudo yum install python3-devel gcc
   ```

2. **Systemd Service Issues**
   ```bash
   # Check service status
   systemctl --user status 925stackai
   
   # View service logs
   journalctl --user -u 925stackai -f
   ```

## Network and Connectivity Issues

### **External API Failures**

**Symptoms**: Unable to reach external services

**Solutions**:

1. **Check Internet Connection**
   ```bash
   ping google.com
   curl -I https://api.openai.com
   ```

2. **Verify Proxy Settings**
   ```bash
   echo $HTTP_PROXY
   echo $HTTPS_PROXY
   ```

3. **Test with curl**
   ```bash
   curl -v https://api.openai.com/v1/models \
     -H "Authorization: Bearer $OPENAI_API_KEY"
   ```

### **CORS Errors**

**Symptoms**: Browser blocks API requests

**Solutions**:

1. **Update CORS Settings**
   ```python
   # In app/main.py
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["http://localhost:8501"],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

2. **Use Proxy Configuration**
   ```python
   # In .streamlit/config.toml
   [server]
   enableCORS = false
   ```

## Performance Optimization

### **Database Performance**

1. **Index Optimization**
   ```sql
   -- Create indexes for common queries
   CREATE INDEX idx_quotes_user_id ON quotes(user_id);
   CREATE INDEX idx_conversations_session ON conversations(session_id);
   ```

2. **Query Optimization**
   ```python
   # Use pagination for large results
   def get_quotes(user_id, page=1, per_page=20):
       offset = (page - 1) * per_page
       return session.query(Quote).filter_by(user_id=user_id)\
                    .offset(offset).limit(per_page).all()
   ```

### **Memory Optimization**

1. **Clear Caches Regularly**
   ```python
   # In scheduled task
   def cleanup_memory():
       memory_agent.clear_old_cache()
       vector_store.optimize_indices()
   ```

2. **Optimize Vector Store**
   ```python
   # Periodically rebuild for efficiency
   python scripts/optimize_vector_store.py
   ```

## Getting Help

### **Log Collection**

#### For Windows (PowerShell):
```powershell
# Collect all relevant logs (robust to missing logs directory)
New-Item -ItemType Directory -Force -Path troubleshooting_logs | Out-Null
if (Test-Path logs) {
  Copy-Item logs\*.log troubleshooting_logs -ErrorAction SilentlyContinue
} else {
  Write-Host "No logs directory found, skipping log copy."
}
# If you use Docker, uncomment the next line:
# docker-compose logs | Out-File troubleshooting_logs\docker.log
pip freeze > troubleshooting_logs\requirements.txt
```

#### For Linux/macOS (Bash):
```bash
#!/usr/bin/env bash
# Collect all relevant logs (robust to missing logs directory)
mkdir -p troubleshooting_logs
if [ -d "logs" ]; then
  cp logs/*.log troubleshooting_logs/
else
  echo "No logs directory found, skipping log copy."
fi
# If you use Docker, uncomment the next line:
# docker-compose logs > troubleshooting_logs/docker.log
pip freeze > troubleshooting_logs/requirements.txt
```

