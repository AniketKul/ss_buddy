# 🚀 Smart Study Buddy - Deployment Guide

## Quick Start (Development)

### 1. Automated Setup
```bash
# Clone or navigate to the project directory
cd ss_buddy

# Run the setup script
./setup.sh

# Activate virtual environment
source venv/bin/activate

# Start the application
python study_buddy_app.py
```

### 2. Manual Setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env
# Edit .env with your configuration

# Run the application
python study_buddy_app.py
```

The application will be available at: **http://localhost:5000**

## Production Deployment

### Option 1: Docker Compose (Recommended)

```bash
# Set environment variables
export NVIDIA_API_KEY="your-nvidia-api-key"
export SECRET_KEY="your-secret-key"

# Deploy with Docker Compose
docker-compose up -d

# Check status
docker-compose ps
```

### Option 2: Kubernetes Deployment

```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: study-buddy
spec:
  replicas: 3
  selector:
    matchLabels:
      app: study-buddy
  template:
    metadata:
      labels:
        app: study-buddy
    spec:
      containers:
      - name: study-buddy
        image: study-buddy:latest
        ports:
        - containerPort: 5000
        env:
        - name: NVIDIA_API_KEY
          valueFrom:
            secretKeyRef:
              name: study-buddy-secrets
              key: nvidia-api-key
        - name: ROUTER_BASE_URL
          value: "http://llm-router-service:8080"
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: study-buddy-service
spec:
  selector:
    app: study-buddy
  ports:
  - port: 80
    targetPort: 5000
  type: LoadBalancer
```

### Option 3: Direct Server Deployment

```bash
# Install system dependencies
sudo apt update
sudo apt install python3 python3-pip python3-venv nginx

# Clone application
git clone <repository-url>
cd ss_buddy

# Setup application
./setup.sh

# Configure systemd service
sudo cp study-buddy.service /etc/systemd/system/
sudo systemctl enable study-buddy
sudo systemctl start study-buddy

# Configure Nginx reverse proxy
sudo cp nginx.conf /etc/nginx/sites-available/study-buddy
sudo ln -s /etc/nginx/sites-available/study-buddy /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

## NVIDIA LLM Router Integration

### Prerequisites
- NVIDIA GPU with 4GB+ memory (V100 or newer)
- NVIDIA Container Toolkit
- NVIDIA NGC API Key
- NVIDIA API Catalog Key

### Setup LLM Router

1. **Clone NVIDIA LLM Router**
```bash
git clone https://github.com/NVIDIA-AI-Blueprints/llm-router
cd llm-router
```

2. **Configure Router**
```yaml
# router-config.yaml
policies:
  - name: "study_task_router"
    url: http://router-server:8000/v2/models/study_router_ensemble/infer
    llms:
      - name: SimpleQA
        model: meta/llama-3.1-8b-instruct
        cost_per_token: 0.0002
      - name: ComplexReasoning
        model: nvidia/llama-3.3-nemotron-super-49b-v1
        cost_per_token: 0.002
      - name: CodeGeneration
        model: deepseek-ai/deepseek-coder-33b-instruct
        cost_per_token: 0.0014
      - name: CreativeWriting
        model: mistralai/mixtral-8x22b-instruct-v0.1
        cost_per_token: 0.0012
      - name: Mathematics
        model: meta/llama-3.1-70b-instruct
        cost_per_token: 0.0018
```

3. **Deploy Router**
```bash
# Set API keys
export NVIDIA_API_KEY="your-key"
export NGC_API_KEY="your-key"

# Deploy router components
docker-compose -f llm-router-compose.yml up -d
```

4. **Update Study Buddy Configuration**
```bash
# Update .env file
ROUTER_BASE_URL=http://your-router-host:8080
NVIDIA_API_KEY=your-nvidia-api-key
```

## Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `FLASK_ENV` | Flask environment | `production` | No |
| `DEBUG` | Enable debug mode | `False` | No |
| `SECRET_KEY` | Flask secret key | Generated | Yes |
| `ROUTER_BASE_URL` | LLM Router URL | `http://localhost:8080` | Yes |
| `NVIDIA_API_KEY` | NVIDIA API key | None | Yes |
| `PORT` | Application port | `5000` | No |

## Monitoring & Logging

### Health Checks
- **Endpoint**: `GET /health`
- **Response**: `{"status": "healthy", "timestamp": "..."}`

### Metrics
- Query count per session
- Cost tracking per user
- Response times
- Model usage statistics

### Logging
```bash
# View application logs
tail -f logs/study_buddy.log

# Docker logs
docker-compose logs -f study-buddy

# Kubernetes logs
kubectl logs -f deployment/study-buddy
```

## Performance Optimization

### Recommended Settings
- **Workers**: 4-8 (based on CPU cores)
- **Memory**: 1-2GB per worker
- **Timeout**: 120 seconds
- **Keep-alive**: 2 seconds

### Scaling
```bash
# Docker Compose scaling
docker-compose up -d --scale study-buddy=3

# Kubernetes scaling
kubectl scale deployment study-buddy --replicas=5
```

## Security Considerations

1. **API Keys**: Store in secure environment variables or secrets management
2. **HTTPS**: Use SSL/TLS in production
3. **Rate Limiting**: Implement request rate limiting
4. **Input Validation**: Sanitize user inputs
5. **CORS**: Configure appropriate CORS policies

## Troubleshooting

### Common Issues

1. **Application won't start**
   - Check Python version (3.8+ required)
   - Verify all dependencies installed
   - Check port availability

2. **LLM Router connection failed**
   - Verify ROUTER_BASE_URL is correct
   - Check network connectivity
   - Validate API keys

3. **High response times**
   - Check LLM Router performance
   - Monitor system resources
   - Consider scaling up

### Debug Mode
```bash
# Enable debug logging
export DEBUG=True
export FLASK_ENV=development

# Run with verbose output
python study_buddy_app.py --debug
```

## Cost Optimization

### Model Selection Strategy
- **Simple QA**: Llama 3 8B (lowest cost)
- **Complex Reasoning**: Nemotron 70B (balanced)
- **Code Generation**: DeepSeek Coder (specialized)
- **Creative Writing**: Mixtral (creative)
- **Mathematics**: Llama 3 70B (analytical)

### Expected Savings
- **Traditional approach**: $3.00/day (100 queries)
- **Smart routing**: $1.50/day (100 queries)
- **Cost reduction**: 50%

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review application logs
3. Consult NVIDIA LLM Router documentation
4. Open an issue in the repository

---

**Ready to deploy your Smart Study Buddy? Follow the guide above and start optimizing your educational AI costs! 🎓** 