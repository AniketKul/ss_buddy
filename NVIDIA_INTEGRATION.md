# 🚀 NVIDIA API Catalog Integration

## Overview

The Smart Study Buddy Assistant now uses **NVIDIA API Catalog** with the official **NVIDIA LLM Router** framework, providing access to high-quality hosted models with intelligent routing and excellent performance.

## 🎯 Model Selection

The system uses the official NVIDIA LLM Router to intelligently route queries to specialized NVIDIA models:

| Task Type | NVIDIA Model | Use Case | Cost/Token |
|-----------|--------------|----------|------------|
| **Simple Q&A** | `meta/llama-3.1-8b-instruct` | Quick facts, definitions | $0.0002 |
| **Complex Reasoning** | `meta/llama-3.1-70b-instruct` | Deep analysis, explanations | $0.0006 |
| **Code Generation** | `nvidia/llama-3.3-nemotron-super-49b-v1` | Programming help | $0.002 |
| **Creative Writing** | `mistralai/mixtral-8x22b-instruct-v0.1` | Essays, stories | $0.0012 |
| **Mathematics** | `meta/llama-3.1-70b-instruct` | Advanced math problems | $0.0018 |

## 🔑 Getting Your NVIDIA API Key

1. **Visit NVIDIA API Catalog**: https://build.nvidia.com/explore/discover
2. **Sign up/Login** with your NVIDIA account
3. **Browse Models**: Explore available models and their capabilities
4. **Generate API Key**: 
   - Go to your account settings
   - Create a new API key
   - Copy the key (starts with `nvapi-...`)

## ⚙️ Configuration

### Update .env File
```bash
# NVIDIA API Catalog Configuration
NVIDIA_API_KEY=nvapi-your-actual-key-here
```

### Verify Integration
```bash
# Test the health endpoint
curl http://localhost:5000/api/health

# Test a query with official NVIDIA LLM Router
curl -X POST http://localhost:5000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is machine learning?"}'
```

## 🧠 How It Works

### 1. Query Analysis
```python
# Auto-detects from: "Write a Python function to sort a list"
detected_subject = "Computer Science"      # From keywords: python, function
detected_difficulty = "Middle School"      # From complexity analysis  
task_type = "code_generation"             # From Triton classification
```

### 2. Model Routing (Official NVIDIA LLM Router)
```python
# Routes using official Triton inference servers
request_body = {
    "model": "",
    "messages": [...],
    "nim-llm-router": {
        "policy": "task_router",
        "routing_strategy": "triton"
    }
}
```

### 3. API Call
```python
# Uses OpenAI-compatible interface with NVIDIA extensions
response_data, chosen_model, chosen_classifier = await router_core.route_request(request_body)
```

## 📊 Current Status

### ✅ Working Features
- **Official NVIDIA LLM Router**: Uses exact same logic as the official implementation
- **Triton Classification**: ML-based classification using Triton inference servers
- **Auto-detection**: Subject, difficulty, and task type classification
- **Model routing**: Intelligent selection of appropriate NVIDIA models
- **Cost tracking**: Real-time cost estimation and session analytics
- **Web interface**: Modern, responsive UI with real-time updates
- **API endpoints**: RESTful API for programmatic access

### 🔄 With Valid API Key
When you add a valid NVIDIA API key, the system will:
- Make real API calls to NVIDIA's hosted models via official router
- Use Triton inference servers for classification
- Provide actual AI-generated responses
- Track real usage costs
- Deliver high-quality educational assistance

### 🎯 Example Responses (with API key)

**Biology Question:**
```
Query: "What is photosynthesis?"
→ Detected: Science/High School/Open QA
→ Model: meta/llama-3.1-70b-instruct
→ Response: Detailed explanation of photosynthesis process...
```

**Programming Question:**
```
Query: "Write a Python function for binary search"
→ Detected: Computer Science/High School/Code Generation  
→ Model: nvidia/llama-3.3-nemotron-super-49b-v1
→ Response: Complete Python function with explanations...
```

**Math Problem:**
```
Query: "Solve the integral of x² from 0 to 5"
→ Detected: Mathematics/College/Reasoning
→ Model: nvidia/llama-3.3-nemotron-super-49b-v1
→ Response: Step-by-step calculus solution...
```

## 💰 Cost Optimization

The official NVIDIA LLM Router optimizes costs by:
- **Smart Routing**: Uses Triton classification to select optimal models
- **Task-Specific Models**: Matches model capabilities to query needs via ML classification
- **Real-Time Tracking**: Monitors spending per session
- **Efficient Prompting**: Structured prompts for better responses

### Estimated Daily Costs (100 queries)
- **60% Simple queries** (Llama 3.1 8B): ~$0.30
- **25% Complex queries** (Llama 3.1 70B): ~$0.75  
- **10% Code queries** (Nemotron 70B): ~$1.20
- **5% Reasoning queries** (Nemotron 70B): ~$0.60
- **Total**: ~$2.85/day vs $8.00+ with single premium model

## 🚀 Next Steps

1. **Get API Key**: Sign up at NVIDIA API Catalog
2. **Update Configuration**: Add your API key to `.env`
3. **Test Integration**: Try various query types with official router
4. **Monitor Usage**: Track costs and performance
5. **Scale Up**: Deploy to production when ready

## 🛠️ Troubleshooting

### Common Issues
- **"No NVIDIA API key provided"**: Add valid key to `.env` file
- **API errors**: Check key validity and network connectivity
- **Triton classification errors**: Verify Triton server availability
- **High costs**: Review query patterns and model selection
- **Slow responses**: Check NVIDIA API status and network

### Debug Commands
```bash
# Check application logs
tail -f logs/app.log

# Test API connectivity
curl -H "Authorization: Bearer $NVIDIA_API_KEY" \
  https://integrate.api.nvidia.com/v1/models

# Test router functionality
python test_nvidia_router.py

# Verify environment variables
python -c "import os; print(os.environ.get('NVIDIA_API_KEY', 'Not set'))"
```

## 📈 Performance Benefits

### Official NVIDIA LLM Router Advantages
- **Enterprise-Grade Classification**: ML-based routing via Triton inference
- **High-Quality Models**: State-of-the-art AI models
- **Reliable Infrastructure**: Enterprise-grade hosting
- **Cost-Effective**: Intelligent model selection reduces costs
- **Easy Integration**: OpenAI-compatible API with NVIDIA extensions
- **Official Support**: Backed by NVIDIA AI Blueprints team

---

**Ready to unlock the full power of NVIDIA's official LLM Router? Add your API key and start learning! 🎓** 