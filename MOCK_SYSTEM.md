# 🎭 NVIDIA API Mock System

## Overview

The mock system allows you to develop and test the Study Buddy application without making real API calls to NVIDIA's API catalog. This preserves the core routing logic while providing realistic responses for development and testing.

## 🎯 What Gets Mocked vs What Doesn't

### ✅ MOCKED (Development Mode)
- **NVIDIA API Catalog calls** to `https://integrate.api.nvidia.com`
- AI responses from models like:
  - `meta/llama-3.1-70b-instruct`
  - `mistralai/mixtral-8x22b-instruct-v0.1`
  - `nvidia/llama-3.3-nemotron-super-49b-v1`
  - All other NVIDIA hosted models

### 🔗 NOT MOCKED (Real Calls)
- **Triton Classification calls** to `localhost:8000`
- ML-based routing and model selection
- Task and complexity classification inference

## 🚀 Quick Start

### Enable Mock Mode (Default)
```bash
# In .env file
NVIDIA_MOCK_MODE=true
```

### Disable Mock Mode (Live API calls)
```bash
# In .env file  
NVIDIA_MOCK_MODE=false
# Also ensure you have a valid API key
NVIDIA_API_KEY="nvapi-your-key-here"
```

### Test the Mock System
```bash
python test_mock_functionality.py
```

## 🎨 Mock Response Features

### Contextual Intelligence
The mock system generates responses based on:
- **Subject Detection**: Mathematics, Science, Computer Science, Creative, General
- **Query Type**: Code generation, explanations, analysis, creative writing
- **Model Characteristics**: Each model has unique response styles and lengths

### Realistic Characteristics
- **Response Times**: Simulated based on model complexity
- **Token Usage**: Calculated based on content length
- **Cost Estimation**: Matches real NVIDIA pricing
- **Model-Specific Styles**: 
  - Llama 8B: Concise responses
  - Llama 70B: Detailed explanations  
  - Nemotron: Technical/code-focused
  - Mixtral: Creative/conversational

### Example Mock Responses

#### Mathematics Query
```
Query: "Explain the Pythagorean theorem"
Mock Response: Detailed step-by-step explanation with formulas and examples
Model Used: meta/llama-3.1-70b-instruct (detailed model)
```

#### Code Generation Query
```
Query: "Write a Python binary search function"
Mock Response: Complete code with explanation and complexity analysis
Model Used: nvidia/llama-3.3-nemotron-super-49b-v1 (code specialist)
```

#### Creative Query  
```
Query: "Write a song with emojis"
Mock Response: Creative song with heavy emoji usage
Model Used: mistralai/mixtral-8x22b-instruct-v0.1 (creative model)
```

## 🔧 Configuration Options

### Environment Variables
```bash
# Enable/disable mock mode
NVIDIA_MOCK_MODE=true  # or false

# Your real API key (for live mode)
NVIDIA_API_KEY="nvapi-your-key-here"
```

### Programmatic Control
```python
from nvidia_router_core import NVIDIARouterService

# Force mock mode on
router = NVIDIARouterService(enable_mocking=True)

# Force mock mode off  
router = NVIDIARouterService(enable_mocking=False)

# Use environment variable setting
router = NVIDIARouterService()  # Uses NVIDIA_MOCK_MODE
```

## 🧪 Testing and Development

### Run Full Test Suite
```bash
# Test mock functionality
python test_mock_functionality.py

# Test original router functionality  
python test_nvidia_router.py

# Start the web application
python study_buddy_app.py
```

### Verify Mock Mode in Logs
```
🎭 Mock mode enabled for NVIDIA API catalog responses
🎭 Using mock response for model: meta/llama-3.1-70b-instruct
```

### Verify Live Mode in Logs
```
🔗 Live mode - will make real API calls to NVIDIA
🔗 Making real API call to: https://integrate.api.nvidia.com/v1/chat/completions
```

## 📊 Benefits of Mock Mode

### Development Benefits
- **No API Costs**: Develop without spending money on API calls
- **Consistent Testing**: Predictable responses for testing
- **Offline Development**: Work without internet connection to NVIDIA
- **Fast Iteration**: No network latency for API calls

### Educational Benefits  
- **Learn the System**: Understand routing logic without API complexity
- **Safe Experimentation**: Test different configurations risk-free
- **Demo Mode**: Show functionality without live API dependencies

### Production Readiness
- **Easy Toggle**: Switch to live mode with one environment variable
- **Same Logic**: Identical routing and classification behavior
- **Real Metrics**: Accurate cost and usage tracking

## 🔄 Switching Between Modes

### Development to Production
```bash
# 1. Update environment
NVIDIA_MOCK_MODE=false

# 2. Ensure API key is valid
NVIDIA_API_KEY="your-production-key"

# 3. Restart application
python study_buddy_app.py
```

### Production to Development
```bash
# 1. Enable mock mode
NVIDIA_MOCK_MODE=true

# 2. Restart application  
python study_buddy_app.py
```

## 🛠️ Mock System Architecture

### File Structure
```
nvidia_api_mock.py          # Mock response generator
nvidia_router_core.py       # Core router with mock integration
test_mock_functionality.py  # Mock system tests
.env                        # Configuration
```

### Mock Response Flow
```
1. Query received by router
2. Triton classification (REAL CALL)
3. Model selected based on classification  
4. Check if URL is NVIDIA API catalog
5. IF mock mode: Generate contextual response
6. IF live mode: Make real API call
7. Return response with metadata
```

## 🎯 Mock Response Quality

### Subject-Aware Responses
- **Mathematics**: Step-by-step solutions with formulas
- **Science**: Detailed explanations with examples
- **Computer Science**: Working code with explanations
- **Creative**: Engaging creative content
- **General**: Informative explanations

### Model-Specific Behavior
- **8B Models**: Shorter, more concise responses
- **70B Models**: Longer, more detailed responses  
- **Nemotron**: Technical and code-focused
- **Mixtral**: Creative and conversational

### Realistic Metadata
- **Token Usage**: ~4 chars per token estimation
- **Processing Time**: Model-specific delays
- **Cost Calculation**: Based on real NVIDIA pricing
- **Response IDs**: Unique identifiers per response

## 🚨 Important Notes

### What's Preserved
✅ **Official NVIDIA LLM Router Logic**: Exact same routing algorithm  
✅ **Triton Classification**: Real ML-based model selection  
✅ **Educational Context**: Subject and difficulty detection  
✅ **Cost Tracking**: Accurate usage and cost metrics  
✅ **API Format**: OpenAI-compatible response format  

### What's Simulated
🎭 **AI Responses**: Generated based on query context  
🎭 **Processing Time**: Simulated based on model characteristics  
🎭 **Response Variation**: Multiple templates for variety  

### Best Practices
- Use mock mode for development and testing
- Switch to live mode for production deployment
- Test both modes before deploying
- Monitor logs to confirm which mode is active
- Keep API keys secure and separate from mock testing

---

**Ready to develop without API costs? Enable mock mode and start building! 🎓** 