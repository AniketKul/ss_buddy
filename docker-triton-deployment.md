# Triton Server Docker Deployment Guide

This guide explains how to deploy the Triton inference server using Docker instead of Kubernetes for the Smart Study Buddy application.

## 🐳 Quick Docker Deployment

### Prerequisites
- Docker installed and running
- Models directory available (from this repository)

### Step 1: Prepare Model Repository

```bash
# Create model repository directory
mkdir -p /tmp/triton-models

# Copy models from this repository
cp -r models/* /tmp/triton-models/

# Verify model structure
find /tmp/triton-models -type f
```

Expected structure:
```
/tmp/triton-models/
├── task_router_ensemble/
│   ├── config.pbtxt
│   └── 1/
│       └── model.py
└── complexity_router_ensemble/
    ├── config.pbtxt
    └── 1/
        └── model.py
```

### Step 2: Deploy Triton Server (CPU-Only)

```bash
# Pull the Triton server image
docker pull nvcr.io/nvidia/tritonserver:24.01-py3

# Run Triton server (CPU-only, no GPU flags)
docker run -d \
  --name triton-server \
  -p 8000:8000 \
  -p 8001:8001 \
  -p 8002:8002 \
  -v /tmp/triton-models:/models \
  --restart unless-stopped \
  nvcr.io/nvidia/tritonserver:24.01-py3 \
  tritonserver --model-repository=/models --log-verbose=1
```

### Step 3: Verify Deployment

```bash
# Check container status
docker ps | grep triton

# Check health
curl http://localhost:8000/v2/health/ready

# List available models
curl http://localhost:8000/v2/models

# Test task router model
curl -X POST http://localhost:8000/v2/models/task_router_ensemble/infer \
  -H "Content-Type: application/json" \
  -d '{"inputs":[{"name":"INPUT","datatype":"BYTES","shape":[1,1],"data":[["test query"]]}]}'

# Test complexity router model
curl -X POST http://localhost:8000/v2/models/complexity_router_ensemble/infer \
  -H "Content-Type: application/json" \
  -d '{"inputs":[{"name":"INPUT","datatype":"BYTES","shape":[1,1],"data":[["test query"]]}]}'
```

## 🔧 Configuration Details

### Model Configuration
Both models are configured for CPU-only inference:
- **Backend**: Python
- **Instance Group**: `KIND_CPU`
- **Max Batch Size**: 1

### Network Configuration
- **Port 8000**: HTTP inference endpoint
- **Port 8001**: GRPC inference endpoint  
- **Port 8002**: Metrics endpoint

### Resource Usage
- **Memory**: ~512MB
- **CPU**: 0.1-0.5 cores (ARM64 or x86_64)
- **Storage**: Minimal (models are ~1KB each)

## 🚀 Production Deployment

### Using Docker Compose

Create `docker-compose.triton.yml`:
```yaml
version: '3.8'

services:
  triton-server:
    image: nvcr.io/nvidia/tritonserver:24.01-py3
    container_name: triton-server
    ports:
      - "8000:8000"
      - "8001:8001"
      - "8002:8002"
    volumes:
      - ./models:/models
    command: tritonserver --model-repository=/models --log-verbose=1
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/v2/health/ready"]
      interval: 30s
      timeout: 10s
      retries: 3
```

Deploy with:
```bash
docker-compose -f docker-compose.triton.yml up -d
```

### Using Systemd Service

Create `/etc/systemd/system/triton-server.service`:
```ini
[Unit]
Description=Triton Inference Server
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStartPre=/usr/bin/docker pull nvcr.io/nvidia/tritonserver:24.01-py3
ExecStart=/usr/bin/docker run -d --name triton-server \
  -p 8000:8000 -p 8001:8001 -p 8002:8002 \
  -v /tmp/triton-models:/models \
  --restart unless-stopped \
  nvcr.io/nvidia/tritonserver:24.01-py3 \
  tritonserver --model-repository=/models --log-verbose=1
ExecStop=/usr/bin/docker stop triton-server
ExecStopPost=/usr/bin/docker rm triton-server

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable triton-server.service
sudo systemctl start triton-server.service
```

## 🔍 Monitoring and Troubleshooting

### Logs
```bash
# View container logs
docker logs triton-server

# Follow logs in real-time
docker logs -f triton-server

# Check for CPU-only operation
docker logs triton-server | grep -i "gpu\|cpu\|cuda"
```

### Performance Monitoring
```bash
# Container resource usage
docker stats triton-server

# Model statistics
curl http://localhost:8000/v2/models/task_router_ensemble/stats
curl http://localhost:8000/v2/models/complexity_router_ensemble/stats
```

### Common Issues

**1. Port Already in Use**
```bash
# Check what's using port 8000
sudo netstat -tlnp | grep 8000

# Kill existing process if needed
sudo fuser -k 8000/tcp
```

**2. Model Loading Errors**
```bash
# Check model files exist
ls -la /tmp/triton-models/

# Verify model configuration
curl http://localhost:8000/v2/models/task_router_ensemble/config
```

**3. Container Won't Start**
```bash
# Check Docker daemon
sudo systemctl status docker

# Check available disk space
df -h /tmp/

# Check memory usage
free -h
```

## 🔄 Updating Models

To update models without downtime:

```bash
# 1. Update model files
cp -r models/* /tmp/triton-models/

# 2. Reload models (if Triton supports it)
curl -X POST http://localhost:8000/v2/repository/models/task_router_ensemble/load

# 3. Or restart container
docker restart triton-server
```

## 🎯 DPU-Specific Optimizations

For NVIDIA BlueField DPU deployment:

```bash
# Use DPU-optimized settings
docker run -d \
  --name triton-server \
  -p 8000:8000 \
  -v /tmp/triton-models:/models \
  --cpus="2.0" \
  --memory="1g" \
  --restart unless-stopped \
  nvcr.io/nvidia/tritonserver:24.01-py3 \
  tritonserver --model-repository=/models \
  --log-verbose=1 \
  --backend-config=python,shm-region-prefix-name=triton_python_backend
```

This configuration is optimized for:
- Limited resources
- Network processing offload
- CPU-only inference 