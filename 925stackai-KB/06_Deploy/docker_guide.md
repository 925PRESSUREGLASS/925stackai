# Docker Deployment Guide

Containerize and deploy 925stackai using Docker for consistent, scalable deployment.

## Prerequisites

* Docker Desktop 4.0+ or Docker Engine 20.10+
* Docker Compose 2.0+
* 8GB RAM minimum (16GB recommended)
* 20GB free disk space

## Docker Configuration

### Dockerfile

The project includes a multi-stage Dockerfile for optimized builds:

```dockerfile
# Build stage
FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Production stage
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd --create-home --shell /bin/bash app
WORKDIR /home/app/925stackai

# Copy Python packages from builder
COPY --from=builder /root/.local /home/app/.local

# Copy application code
COPY --chown=app:app . .

# Switch to non-root user
USER app

# Make sure scripts are executable
RUN chmod +x scripts/*.sh

# Set environment variables
ENV PATH=/home/app/.local/bin:$PATH
ENV PYTHONPATH=/home/app/925stackai

EXPOSE 8000 8501

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

# Default command
CMD ["./scripts/start-services.sh"]
```

### Docker Compose Configuration

```yaml
version: '3.8'

services:
  app:
    build: .
    container_name: 925stackai-app
    ports:
      - "8000:8000"  # FastAPI
      - "8501:8501"  # Streamlit
    environment:
      - DEBUG=false
      - LOG_LEVEL=INFO
      - DATABASE_URL=postgresql://user:password@postgres:5432/925stackai
      - REDIS_URL=redis://redis:6379/0
      - MEMORY_STORAGE_PATH=/app/data/memory
    volumes:
      - app_data:/app/data
      - app_logs:/app/logs
    depends_on:
      - postgres
      - redis
      - ollama
    restart: unless-stopped
    networks:
      - 925stackai-network

  postgres:
    image: postgres:15-alpine
    container_name: 925stackai-postgres
    environment:
      - POSTGRES_DB=925stackai
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./scripts/init-db.sql:/docker-entrypoint-initdb.d/init-db.sql
    ports:
      - "5432:5432"
    restart: unless-stopped
    networks:
      - 925stackai-network

  redis:
    image: redis:7-alpine
    container_name: 925stackai-redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped
    networks:
      - 925stackai-network

  ollama:
    image: ollama/ollama:latest
    container_name: 925stackai-ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    environment:
      - OLLAMA_HOST=0.0.0.0
    restart: unless-stopped
    networks:
      - 925stackai-network

  nginx:
    image: nginx:alpine
    container_name: 925stackai-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
    depends_on:
      - app
    restart: unless-stopped
    networks:
      - 925stackai-network

volumes:
  app_data:
  app_logs:
  postgres_data:
  redis_data:
  ollama_data:

networks:
  925stackai-network:
    driver: bridge
```

## Quick Start

### 1. Clone and Configure

```bash
git clone https://github.com/925PRESSUREGLASS/925stackai.git
cd 925stackai

# Copy environment template
cp .env.docker .env

# Edit configuration
nano .env
```

### 2. Build and Start

```bash
# Build all services
docker-compose build

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f app
```

### 3. Initialize Ollama

```bash
# Pull the Llama 3 model
docker-compose exec ollama ollama pull llama3

# Verify model is available
docker-compose exec ollama ollama list
```

### 4. Access Services

* **Application**: http://localhost:8501
* **API Documentation**: http://localhost:8000/docs
* **Database**: localhost:5432
* **Redis**: localhost:6379

## Production Deployment

### Environment Configuration

Create a production `.env` file:

```env
# Production settings
DEBUG=false
LOG_LEVEL=WARNING
SECRET_KEY=your-super-secret-production-key

# Database (use external managed database in production)
DATABASE_URL=postgresql://user:password@your-db-host:5432/925stackai

# Redis (use external Redis in production)
REDIS_URL=redis://your-redis-host:6379/0

# Security
ALLOWED_HOSTS=your-domain.com,api.your-domain.com
CORS_ORIGINS=https://your-domain.com

# SSL/TLS
USE_SSL=true
SSL_CERT_PATH=/etc/nginx/ssl/cert.pem
SSL_KEY_PATH=/etc/nginx/ssl/key.pem

# Monitoring
SENTRY_DSN=your-sentry-dsn
```

### SSL/TLS Configuration

#### Nginx Configuration (`nginx/nginx.conf`)

```nginx
events {
    worker_connections 1024;
}

http {
    upstream app_backend {
        server app:8000;
    }

    upstream streamlit_frontend {
        server app:8501;
    }

    # Redirect HTTP to HTTPS
    server {
        listen 80;
        server_name your-domain.com;
        return 301 https://$server_name$request_uri;
    }

    # HTTPS Configuration
    server {
        listen 443 ssl http2;
        server_name your-domain.com;

        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;

        # Frontend (Streamlit)
        location / {
            proxy_pass http://streamlit_frontend;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # API Backend
        location /api/ {
            proxy_pass http://app_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Health check
        location /health {
            proxy_pass http://app_backend/api/v1/health;
        }
    }
}
```

### Database Migrations

```bash
# Run database migrations
docker-compose exec app python scripts/migrate_database.py

# Create initial admin user
docker-compose exec app python scripts/create_admin_user.py
```

## Scaling and High Availability

### Horizontal Scaling

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000-8002:8000"  # Scale to 3 instances
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
        window: 120s
    environment:
      - WORKER_ID={{ .Task.Slot }}
    # ... other configuration
```

### Load Balancer Configuration

```yaml
  haproxy:
    image: haproxy:2.4-alpine
    container_name: 925stackai-lb
    ports:
      - "80:80"
      - "8404:8404"  # Stats page
    volumes:
      - ./haproxy/haproxy.cfg:/usr/local/etc/haproxy/haproxy.cfg
    depends_on:
      - app
```

## Monitoring and Logging

### Log Management

```yaml
services:
  app:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### Health Monitoring

```bash
# Check all services health
docker-compose ps

# Monitor resource usage
docker stats

# View application logs
docker-compose logs -f app --tail=100
```

### Prometheus Metrics (Optional)

```yaml
  prometheus:
    image: prom/prometheus:latest
    container_name: 925stackai-prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'

  grafana:
    image: grafana/grafana:latest
    container_name: 925stackai-grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana
      - ./monitoring/grafana/dashboards:/etc/grafana/provisioning/dashboards
```

## Backup and Recovery

### Database Backup

```bash
# Create database backup
docker-compose exec postgres pg_dump -U user 925stackai > backup_$(date +%Y%m%d).sql

# Restore from backup
docker-compose exec -T postgres psql -U user 925stackai < backup_20240715.sql
```

### Application Data Backup

```bash
# Backup application data volume
docker run --rm -v 925stackai_app_data:/data -v $(pwd):/backup \
  alpine tar czf /backup/app_data_backup_$(date +%Y%m%d).tar.gz -C /data .

# Restore application data
docker run --rm -v 925stackai_app_data:/data -v $(pwd):/backup \
  alpine tar xzf /backup/app_data_backup_20240715.tar.gz -C /data
```

## Troubleshooting

### Common Issues

#### Container Won't Start

```bash
# Check logs
docker-compose logs app

# Check resource usage
docker system df

# Restart specific service
docker-compose restart app
```

#### Database Connection Issues

```bash
# Test database connectivity
docker-compose exec app python -c "
import psycopg2
conn = psycopg2.connect('postgresql://user:password@postgres:5432/925stackai')
print('Database connection successful')
"
```

#### Ollama Model Issues

```bash
# Check available models
docker-compose exec ollama ollama list

# Re-pull model if corrupted
docker-compose exec ollama ollama pull llama3
```

### Performance Tuning

```bash
# Increase memory limits
docker-compose.override.yml:
```yaml
services:
  app:
    mem_limit: 4g
    memswap_limit: 4g
  
  ollama:
    mem_limit: 8g
    memswap_limit: 8g
```

## Security Considerations

* Use Docker secrets for sensitive data
* Run containers as non-root users
* Keep base images updated
* Use multi-stage builds to minimize attack surface
* Implement proper network segmentation
* Regular security scanning with tools like Snyk or Trivy

For local development setup, see [Local Run Guide](local_run.md). For troubleshooting, see [Troubleshooting Guide](troubleshooting.md).
