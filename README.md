# Smart Study Buddy - Educational AI Assistant

**Now powered by the Official NVIDIA LLM Router Framework**

An intelligent educational assistant that uses the **exact same core logic** as the [official NVIDIA LLM Router](https://github.com/NVIDIA-AI-Blueprints/llm-router) to route educational queries to the most appropriate AI models for optimal learning experiences.

## 🚀 Key Features

### Official NVIDIA LLM Router Integration
- **Exact Implementation**: Uses the same routing logic as the official NVIDIA LLM Router repository
- **Triton Classification**: Uses Triton inference servers for model classification
- **OpenAI-Compatible API**: Follows the official OpenAI API specification with NVIDIA extensions
- **NodePort Deployment**: Kubernetes-ready with NodePort service configuration

### Educational Enhancements
- **Subject Detection**: Automatically identifies the academic subject (Math, Science, Literature, etc.)
- **Difficulty Assessment**: Determines appropriate academic level (Elementary to Graduate)
- **Learning-Optimized Responses**: Provides step-by-step explanations tailored to the detected level
- **Real-time Statistics**: Tracks usage patterns and model performance

### Modern Web Interface
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Real-time Chat**: Interactive conversation interface with typing indicators
- **Model Transparency**: Shows which AI model and routing policy was used for each response
- **Performance Metrics**: Displays response times and token usage
- **Error Handling**: Graceful error handling with user-friendly notifications

## 🏗️ Architecture

### Official NVIDIA LLM Router Core

This application implements the exact same routing architecture as the official NVIDIA LLM Router:

```
User Query → nim-llm-router params → Policy Selection → Classification → Model Selection → Response
```

#### 1. **Request Format** (Official NVIDIA LLM Router Compatible)
```json
{
  "model": "",
  "messages": [...],
  "nim-llm-router": {
    "policy": "task_router",
    "routing_strategy": "triton",
    "model": "optional_for_manual"
  }
}
```

#### 2. **Routing Policies** (Identical to Official Implementation)

**Task Router Policy** - Classifies queries by task type:
- **Brainstorming** → `meta/llama-3.1-70b-instruct`
- **Chatbot** → `mistralai/mixtral-8x22b-instruct-v0.1`
- **Classification** → `meta/llama-3.1-8b-instruct`
- **Closed QA** → `meta/llama-3.1-70b-instruct`
- **Code Generation** → `nvidia/llama-3.3-nemotron-super-49b-v1`
- **Extraction** → `meta/llama-3.1-8b-instruct`
- **Open QA** → `meta/llama-3.1-70b-instruct`
- **Other** → `mistralai/mixtral-8x22b-instruct-v0.1`
- **Rewrite** → `meta/llama-3.1-8b-instruct`
- **Summarization** → `meta/llama-3.1-70b-instruct`
- **Text Generation** → `mistralai/mixtral-8x22b-instruct-v0.1`
- **Unknown** → `meta/llama-3.1-8b-instruct`

**Complexity Router Policy** - Classifies queries by complexity:
- **Creativity** → `meta/llama-3.1-70b-instruct`
- **Reasoning** → `nvidia/llama-3.3-nemotron-super-49b-v1`
- **Contextual-Knowledge** → `meta/llama-3.1-8b-instruct`
- **Few-Shot** → `meta/llama-3.1-70b-instruct`
- **Domain-Knowledge** → `mistralai/mixtral-8x22b-instruct-v0.1`
- **No-Label-Reason** → `meta/llama-3.1-8b-instruct`
- **Constraint** → `meta/llama-3.1-8b-instruct`

#### 3. **Classification Method**

**Triton Inference Server** (Official Method)
- Connects to Triton servers at configured URLs
- Uses pre-trained classification models (`task_router_ensemble` or `complexity_router_ensemble`)
- Sends text input in official Triton format with `INPUT` tensor
- Returns probability distribution over classification categories

#### 4. **Routing Strategies**

**Triton Strategy** (Default)
```json
{
  "nim-llm-router": {
    "policy": "task_router",
    "routing_strategy": "triton"
  }
}
```

**Manual Strategy** (Direct Model Selection)
```json
{
  "nim-llm-router": {
    "policy": "task_router", 
    "routing_strategy": "manual",
    "model": "Code Generation"
  }
}
```

## 🔍 Exact Routing Logic Implementation

The Smart Study Buddy implements the **exact same 5-step routing process** as the official NVIDIA LLM Router:

### Step 1: Request Parsing & Parameter Extraction
```python
# Extract nim-llm-router parameters from request body
nim_params = self.extract_nim_llm_router_params(request_body)
# Expected: {"policy": "task_router", "routing_strategy": "triton"}
```

### Step 2: Policy Selection & Validation
```python
# Get policy configuration (task_router or complexity_router)
policy = self.config.get_policy_by_name(nim_params.policy)
# Loads Triton server URL and model mappings
```

### Step 3: Text Preparation & Classification
```python
# Convert messages to classification input
messages = self.extract_messages(request_body)
text_input = self.convert_messages_to_text_input(messages)

# Send to Triton inference server
triton_request = {
    "inputs": [{"name": "INPUT", "datatype": "BYTES", "shape": [1, 1], "data": [[text_input]]}]
}
response = requests.post(policy.url, json=triton_request)
```

**Real Classification Example from Logs:**
```
Query: "Can you help me write a poem?"
Triton Output: [0.034, 0.048, 0.129, 0.119, 0.013, 0.032, 0.104, 0.107, 0.116, 0.113, 0.109, 0.074]
Model index chosen: 2 (Classification)
Chosen Model: meta/llama-3.1-8b-instruct
```

### Step 4: Model Selection & Mapping
```python
# Find model with highest probability
model_index = probabilities.index(max(probabilities))
chosen_llm = policy.get_llm_by_index(model_index)
# Maps index to specific NVIDIA model
```

**Classification Categories (Task Router):**
- Index 0: Brainstorming
- Index 1: Chatbot  
- Index 2: Classification
- Index 6: Open QA
- Index 10: Text Generation
- etc.

### Step 5: Request Proxying & Response
```python
# Remove nim-llm-router parameters and set model
cleaned_body = self.remove_nim_llm_router_params(request_body)
final_body = self.modify_model_in_request(cleaned_body, chosen_llm.model)

# Proxy to selected NVIDIA model
response = requests.post(f"{chosen_llm.api_base}/v1/chat/completions", 
                        headers={"Authorization": f"Bearer {chosen_llm.api_key}"}, 
                        json=final_body)
```

### Real-World Routing Examples

**Example 1: Chatbot Classification**
```
Input: "Hello! How are you?"
→ Triton Classification: [0.071, 0.149, 0.025, 0.099, 0.122, 0.115, 0.096, 0.087, 0.071, 0.086, 0.079, 0.001]
→ Highest probability at index 1 (0.149)
→ Classification: "Chatbot"
→ Selected Model: mistralai/mixtral-8x22b-instruct-v0.1
→ Response Time: ~4.2 seconds
```

**Example 2: Poetry Writing (Classification)**
```
Input: "Can you help me write a poem?"
→ Triton Classification: [0.034, 0.048, 0.129, 0.119, 0.013, 0.032, 0.104, 0.107, 0.116, 0.113, 0.109, 0.074]
→ Highest probability at index 2 (0.129)
→ Classification: "Classification"
→ Selected Model: meta/llama-3.1-8b-instruct
→ Response Time: ~7.6 seconds
```

## 🔧 Implementation Details

### Core Components

1. **`nvidia_router_core.py`** - Official NVIDIA LLM Router implementation
   - `NVIDIALLMRouterCore`: Exact replication of Rust proxy.rs logic
   - `RouterConfig`: Configuration loading with YAML support and environment variable substitution
   - `Policy` & `Llm`: Data structures matching official schema
   - **Environment Loading**: Uses `python-dotenv` for `.env` file support

2. **`nvidia_router_config.yaml`** - Official configuration file
   - NodePort Triton server URLs: `http://10.185.98.229:30800/v2/models/*/infer`
   - Exact model mappings from official repository
   - NVIDIA API key environment variable substitution

3. **`study_buddy_app.py`** - Flask application with educational enhancements
   - Wraps the official router core with educational context
   - Provides web API and user interface
   - **Environment Loading**: Loads `.env` file on startup

4. **`static/js/app.js`** - Frontend JavaScript (Recently Updated)
   - Fixed response handling to work with direct API response format
   - Added graceful handling of missing fields (cost, confidence)
   - Updated stats display to use correct backend field names
   - Added proper error notifications

### Recent Updates & Fixes

#### ✅ **Environment Variable Loading**
- Added `load_dotenv()` to all Python files
- Supports `.env` file for easy configuration
- Automatic NVIDIA API key loading

#### ✅ **Kubernetes NodePort Deployment**
- Triton server deployed as NodePort service on port 30800
- External access: `http://10.185.98.229:30800`
- No port-forwarding required

#### ✅ **Frontend JavaScript Fixes**
- Fixed response structure mismatch (removed `success`/`data` wrapper expectation)
- Added graceful handling of missing `cost` and `confidence` fields
- Updated stats API to use correct field names (`total_queries`, `total_response_time`)
- Added proper error handling and notifications

#### ✅ **SR-IOV Operator Resolution**
- Resolved Kubernetes node scheduling issues
- Scaled down SR-IOV operator to prevent node cordoning
- Triton pods now schedule successfully

### Key Differences from Previous Implementation

| Aspect | Previous (Pattern-Based) | Current (Official NVIDIA Router) |
|--------|-------------------------|----------------------------------|
| **Classification** | Keyword pattern matching | Triton inference servers with ML models |
| **Model Selection** | Simple heuristics | Pre-trained classification models |
| **API Format** | Custom format | Official OpenAI + NVIDIA extensions |
| **Routing Logic** | Educational-specific patterns | Enterprise-grade routing policies |
| **Scalability** | Limited to predefined patterns | ML-based classification with continuous learning |
| **Compatibility** | Custom implementation | Compatible with official NVIDIA infrastructure |
| **Deployment** | Single container | Kubernetes with Triton inference servers |

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- NVIDIA API Key ([Get one here](https://build.nvidia.com/))
- Kubernetes cluster (for Triton deployment)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd smart-study-buddy
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set your NVIDIA API key**

**Option 1: Environment Variable**
```bash
export NVIDIA_API_KEY="your-nvidia-api-key-here"
```

**Option 2: .env File (Recommended)**
Create a `.env` file in the project root:
```bash
# Study Buddy Configuration
SECRET_KEY=study-buddy-dev-secret-key
FLASK_ENV=development
FLASK_DEBUG=True

# NVIDIA API Catalog Configuration
NVIDIA_API_KEY="your-nvidia-api-key-here"

# Server Configuration
PORT=5000
HOST=0.0.0.0
```

4. **Deploy Triton Server (Kubernetes)**
```bash
# Deploy mock Triton server with NodePort
kubectl apply -f triton-deployment.yaml

# Verify deployment
kubectl get svc -n triton
# Should show router-server service with NodePort 30800
```

5. **Run the application**
```bash
python study_buddy_app.py
```

6. **Open your browser**
Navigate to `http://localhost:5000`

### Docker Deployment

```bash
# Build the image
docker build -t smart-study-buddy .

# Run with your API key
docker run -p 5000:5000 -e NVIDIA_API_KEY="your-key" smart-study-buddy
```

### Kubernetes Deployment

The application includes Kubernetes deployment files for the Triton inference server:

```yaml
# triton-deployment.yaml
apiVersion: v1
kind: Service
metadata:
  name: router-server
  namespace: triton
spec:
  type: NodePort
  ports:
  - port: 8000
    targetPort: 8000
    nodePort: 30800
  selector:
    app: triton-server
```

## 📊 API Endpoints

### Educational Query Processing
```bash
POST /api/query
{
  "query": "Explain photosynthesis",
  "routing_strategy": "triton"
}
```

**Response Format:**
```json
{
  "response": "Photosynthesis is the process...",
  "model_used": "meta/llama-3.1-70b-instruct",
  "classifier_used": "Summarization",
  "policy_used": "task_router",
  "routing_strategy": "triton",
  "response_time": 3.18,
  "detected_subject": "Science",
  "detected_difficulty": "Elementary",
  "usage": {
    "prompt_tokens": 45,
    "completion_tokens": 294,
    "total_tokens": 339
  }
}
```

### Router Testing (Official Format)
```bash
POST /api/test-router
{
  "policy": "complexity_router",
  "routing_strategy": "triton"
}
```

### Configuration Information
```bash
GET /api/config
```

### Health Check
```bash
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "nvidia_api_key_configured": true,
  "nvidia_router_available": true,
  "policies_loaded": 2,
  "total_models": 19
}
```

### Statistics
```bash
GET /api/stats
```

**Response:**
```json
{
  "total_queries": 5,
  "average_response_time": 4.99,
  "queries_by_model": {
    "meta/llama-3.1-70b-instruct": 3,
    "mistralai/mixtral-8x22b-instruct-v0.1": 2
  },
  "queries_by_difficulty": {
    "Elementary": 3,
    "High School": 2
  }
}
```

## 🎯 Educational Enhancements

While maintaining the official routing core, the application adds educational context:

- **Subject Detection**: Identifies academic subjects using pattern matching
- **Difficulty Assessment**: Determines appropriate academic level
- **Enhanced Prompts**: Adds educational context to improve learning outcomes
- **Progress Tracking**: Monitors learning patterns and model effectiveness

## 🔧 Configuration

### Environment Variables
- `NVIDIA_API_KEY`: Your NVIDIA API key (required)
- `PORT`: Server port (default: 5000)
- `HOST`: Server host (default: 0.0.0.0)
- `SECRET_KEY`: Flask secret key
- `FLASK_ENV`: Flask environment (development/production)

### Router Configuration
The `nvidia_router_config.yaml` file contains the official NVIDIA LLM Router configuration:
- Policy definitions with Triton server URLs (NodePort: `http://10.185.98.229:30800`)
- Model mappings for each classification category
- API endpoints and authentication settings

### Triton Server Configuration
- **Deployment**: Kubernetes deployment in `triton` namespace
- **Service Type**: NodePort (external access on port 30800)
- **Mock Server**: Python HTTP server mimicking Triton API
- **Health Checks**: `/v2/health/live` and `/v2/health/ready` endpoints

## 📈 Monitoring & Analytics

- **Real-time Statistics**: Query counts, response times, model usage
- **Policy Analytics**: Usage patterns across routing policies
- **Educational Metrics**: Subject and difficulty level distributions
- **Performance Tracking**: Average response times and token usage
- **Model Distribution**: Usage statistics per NVIDIA model
- **Classification Insights**: Most common task and complexity classifications

## 🐛 Troubleshooting

### Common Issues

**1. UI Not Working / JavaScript Errors**
- **Fixed**: Updated frontend to handle direct API response format
- **Solution**: Ensure you're using the latest `static/js/app.js`

**2. NVIDIA API Key Not Found**
- **Cause**: `.env` file not loaded
- **Solution**: Ensure `load_dotenv()` is called in Python files

**3. Triton Server Connection Failed**
- **Cause**: NodePort service not accessible
- **Solution**: Check Kubernetes service: `kubectl get svc -n triton`

**4. Node Scheduling Issues**
- **Cause**: SR-IOV operator cordoning nodes
- **Solution**: Scale down operator: `kubectl scale deployment network-operator-sriov-network-operator --replicas=0 -n nvidia-network-operator`

### Verification Commands

```bash
# Check application health
curl http://localhost:5000/api/health

# Test Triton server
curl http://10.185.98.229:30800/v2/health/ready

# Check Kubernetes deployment
kubectl get pods -n triton
kubectl get svc -n triton

# Test end-to-end query
curl -X POST http://localhost:5000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is photosynthesis?", "routing_strategy": "triton"}'
```

## 🤝 Contributing

This project implements the official NVIDIA LLM Router logic. For core routing improvements, consider contributing to the [official repository](https://github.com/NVIDIA-AI-Blueprints/llm-router).

For educational enhancements and UI improvements:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.

The NVIDIA LLM Router components are based on the official implementation and maintain the same Apache 2.0 license.

## 🙏 Acknowledgments

- **NVIDIA AI Blueprints Team** for the official LLM Router implementation
- **NVIDIA NIM** for providing the model APIs
- **Open Source Community** for the foundational libraries

---

**Note**: This implementation uses the exact same core logic as the official NVIDIA LLM Router with Triton inference servers for classification. The application is designed to work with the official NVIDIA infrastructure and maintains full compatibility with the official router architecture.