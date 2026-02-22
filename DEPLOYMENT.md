# Deployment Guide

This guide covers deploying MCP Confluence Server in various environments.

## Table of Contents
1. [Local Development](#local-development)
2. [Docker](#docker)
3. [Docker Compose](#docker-compose)
4. [Kubernetes](#kubernetes)
5. [Cloud Platforms](#cloud-platforms)
6. [Production Considerations](#production-considerations)

## Local Development

### Prerequisites
- Python 3.9+
- pip or poetry

### Setup

```bash
# Clone repository
git clone <repo-url>
cd mcp-confluence

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env with your Confluence credentials

# Run tests
pytest tests/ -v

# Start server
python -m src.main
```

## Docker

### Build Image

```bash
# Build
docker build -t mcp-confluence:latest .

# Run
docker run -d \
  -e CONFLUENCE_URL=https://your-domain.atlassian.net \
  -e CONFLUENCE_USERNAME=your-email@example.com \
  -e CONFLUENCE_API_TOKEN=your-token \
  -e CONFLUENCE_DEPLOYMENT=cloud \
  --name mcp-confluence \
  mcp-confluence:latest
```

### Run with Environment File

```bash
docker run -d \
  --env-file .env \
  --name mcp-confluence \
  mcp-confluence:latest
```

### Docker Logs

```bash
docker logs -f mcp-confluence
```

## Docker Compose

### Quick Start

```bash
# Create .env file
cp .env.example .env
# Edit .env with your credentials

# Start services
docker-compose up -d

# View logs
docker-compose logs -f mcp-confluence

# Stop services
docker-compose down
```

### Custom Configuration

Edit `docker-compose.yml` to customize:
- Resource limits
- Port mappings
- Volume mounts
- Additional services

### Scale with Docker Compose

For multiple instances:

```yaml
services:
  mcp-confluence:
    build: .
    deploy:
      replicas: 3
```

## Kubernetes

### Prerequisites
- kubectl
- Docker image in registry

### Create ConfigMap

```bash
kubectl create configmap mcp-confluence-config \
  --from-literal=CONFLUENCE_URL=https://your-domain.atlassian.net \
  --from-literal=CONFLUENCE_USERNAME=your-email@example.com \
  --from-literal=CONFLUENCE_DEPLOYMENT=cloud
```

### Create Secret for API Token

```bash
kubectl create secret generic mcp-confluence-secret \
  --from-literal=CONFLUENCE_API_TOKEN=your-token
```

### Deploy with Manifest

```yaml
# mcp-confluence-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mcp-confluence
  labels:
    app: mcp-confluence
spec:
  replicas: 3
  selector:
    matchLabels:
      app: mcp-confluence
  template:
    metadata:
      labels:
        app: mcp-confluence
    spec:
      containers:
      - name: mcp-confluence
        image: your-registry/mcp-confluence:latest
        imagePullPolicy: Always
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        envFrom:
        - configMapRef:
            name: mcp-confluence-config
        - secretRef:
            name: mcp-confluence-secret
        livenessProbe:
          exec:
            command:
            - python
            - -c
            - "import sys; sys.exit(0)"
          initialDelaySeconds: 10
          periodSeconds: 30
        readinessProbe:
          exec:
            command:
            - python
            - -c
            - "import sys; sys.exit(0)"
          initialDelaySeconds: 5
          periodSeconds: 10
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsReadOnlyRootFilesystem: true
---
apiVersion: v1
kind: Service
metadata:
  name: mcp-confluence-service
spec:
  selector:
    app: mcp-confluence
  ports:
  - port: 8000
    targetPort: 8000
  type: ClusterIP
```

Deploy:
```bash
kubectl apply -f mcp-confluence-deployment.yaml
```

## Cloud Platforms

### AWS ECS

1. Create ECR repository
2. Push image to ECR
3. Create ECS task definition
4. Create ECS service

### Google Cloud Run

```bash
# Build and push
gcloud builds submit --tag gcr.io/PROJECT_ID/mcp-confluence

# Deploy
gcloud run deploy mcp-confluence \
  --image gcr.io/PROJECT_ID/mcp-confluence \
  --set-env-vars CONFLUENCE_URL=https://your-domain.atlassian.net \
  --set-env-vars CONFLUENCE_USERNAME=your-email@example.com \
  --set-env-vars CONFLUENCE_API_TOKEN=your-token
```

### Azure Container Instances

```bash
az container create \
  --resource-group myResourceGroup \
  --name mcp-confluence \
  --image myacr.azurecr.io/mcp-confluence:latest \
  --environment-variables \
    CONFLUENCE_URL=https://your-domain.atlassian.net \
    CONFLUENCE_USERNAME=your-email@example.com
```

## Production Considerations

### Security

1. **Secrets Management**
   ```bash
   # Use HashiCorp Vault, AWS Secrets Manager, or similar
   # Never commit credentials to version control
   ```

2. **HTTPS/TLS**
   - Confluence URL should use HTTPS
   - Consider reverse proxy (nginx, traefik)

3. **Access Control**
   - Run with non-root user (Docker: USER mcp)
   - Use read-only filesystem where possible
   - Implement network policies

4. **API Token Rotation**
   - Regular token rotation schedule
   - Use short-lived tokens if possible
   - Monitor token usage

### High Availability

1. **Load Balancing**
   ```bash
   # Use nginx or cloud load balancer
   # Route requests to multiple instances
   ```

2. **Monitoring**
   ```bash
   # Implement health checks
   # Monitor response times
   # Alert on errors
   ```

3. **Logging**
   ```bash
   # Centralize logs (ELK, Splunk, CloudWatch)
   # Include request/response logs
   # Track performance metrics
   ```

### Backup & Recovery

1. Configuration backup
2. Regular testing of recovery procedures
3. Document rollback procedures

### Performance

1. **Caching**
   - Implement page cache
   - Cache frequently accessed spaces
   - Set appropriate TTLs

2. **Rate Limiting**
   ```env
   RATE_LIMIT_DELAY=1
   MAX_RETRIES=3
   ```

3. **Resource Limits**
   ```yaml
   resources:
     limits:
       memory: 512Mi
       cpu: 500m
   ```

### Monitoring & Observability

1. **Health Checks**
   ```bash
   # Kubernetes
   livenessProbe:
     exec:
       command: ["python", "-c", "import sys; sys.exit(0)"]
       
   # Docker
   HEALTHCHECK --interval=30s --timeout=10s ...
   ```

2. **Metrics**
   - Request latency
   - Error rates
   - Token usage
   - Cache hit rates

3. **Logging**
   ```
   LOG_LEVEL=INFO
   # Logs include: requests, errors, performance metrics
   ```

### Updates & Patching

1. Test updates in staging
2. Use blue-green deployment
3. Keep dependencies updated
4. Monitor security advisories

## Troubleshooting Deployment

### Container won't start
```bash
# Check logs
docker logs <container-id>

# Verify environment variables
docker inspect <container-id>

# Test locally
python -m src.main
```

### Connection refused
- Verify CONFLUENCE_URL is correct
- Check network connectivity
- Verify credentials

### High memory usage
- Check for memory leaks
- Reduce log level
- Limit request caching
- Scale horizontally

### Slow responses
- Monitor Confluence server
- Check network latency
- Implement caching
- Scale horizontally

## Support & Resources

- [README.md](README.md) - Project overview
- [QUICKSTART.md](QUICKSTART.md) - Quick setup guide
- [API_REFERENCE.md](API_REFERENCE.md) - Tool documentation
- Issues: Report on GitHub

