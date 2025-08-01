# Smart Study Buddy - Educational AI Assistant


**Powered by the Official NVIDIA LLM Router Framework**

An intelligent educational assistant that uses the **exact same core logic** as the [official NVIDIA LLM Router](https://github.com/NVIDIA-AI-Blueprints/llm-router) to route educational queries to the most appropriate AI models for optimal learning experiences.

## 🚀 Key Features

### Official NVIDIA LLM Router Integration
- **Exact Implementation**: Uses the same routing logic as the official NVIDIA LLM Router repository
- **Triton Classification**: Uses Triton inference servers for model classification
- **OpenAI-Compatible API**: Follows the official OpenAI API specification with NVIDIA extensions
- **Intelligent Routing**: Automatically selects optimal models based on query complexity and task type

### Educational Enhancements
- **Subject Detection**: Automatically identifies the academic subject (Math, Science, Literature, etc.)
- **Difficulty Assessment**: Determines appropriate academic level (Elementary to Graduate)
- **Learning-Optimized Responses**: Provides step-by-step explanations tailored to the detected level
- **Real-time Statistics**: Tracks usage patterns and model performance with cost optimization

### Modern Web Interface
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Real-time Chat**: Interactive conversation interface with typing indicators
- **Model Transparency**: Shows which AI model and routing policy was used for each response
- **Performance Metrics**: Displays response times, token usage, and costs

## 🏗️ Architecture

This application implements the exact same routing architecture as the official NVIDIA LLM Router:

```
User Query → nim-llm-router params → Policy Selection → Classification → Model Selection → Response
```

### Routing Policies

**Task Router Policy** - Classifies queries by task type:
- **Code Generation** → `nvidia/llama-3.3-nemotron-super-49b-v1`
- **Open QA** → `meta/llama-3.1-70b-instruct`
- **Summarization** → `meta/llama-3.1-70b-instruct`
- **Chatbot** → `mistralai/mixtral-8x22b-instruct-v0.1`
- **Classification** → `meta/llama-3.1-8b-instruct`
- And more...

**Complexity Router Policy** - Classifies queries by complexity:
- **Reasoning** → `nvidia/llama-3.3-nemotron-super-49b-v1`
- **Creativity** → `meta/llama-3.1-70b-instruct`
- **Domain-Knowledge** → `mistralai/mixtral-8x22b-instruct-v0.1`
- **Contextual-Knowledge** → `meta/llama-3.1-8b-instruct`
- And more...

## 🧠 How LLM Routing Works

The Smart Study Buddy uses a sophisticated 5-step routing process to automatically select the most appropriate AI model for each query:

### Step 1: Query Analysis
When you submit a question, the system first analyzes your input to understand what type of task you're requesting:
- **Educational Context**: Detects the subject (Math, Science, Literature, etc.) and difficulty level
- **Task Type**: Identifies whether you're asking for explanations, code generation, creative writing, etc.
- **Complexity Assessment**: Determines if the query requires simple factual answers or complex reasoning

### Step 2: Policy Selection
Based on your query, the system chooses between two routing strategies:
- **Task Router**: Routes based on what you want to do (explain, code, summarize, chat, etc.)
- **Complexity Router**: Routes based on how complex your request is (reasoning, creativity, domain knowledge, etc.)

### Step 3: AI Classification
Your query is sent to a Triton inference server that runs a specialized classification model:
- **Machine Learning Classification**: Uses pre-trained models to analyze your text
- **Probability Distribution**: Returns confidence scores for different categories
- **Real-time Processing**: Classification happens in milliseconds

**Example Classification:**
```
Query: "Can you help me write a Python function to calculate fibonacci numbers?"
→ Task Classification: Code Generation (85% confidence)
→ Selected Model: nvidia/llama-3.3-nemotron-super-49b-v1
```

### Step 4: Model Selection
Based on the classification results, the system automatically selects the optimal model:
- **Specialized Models**: Each model excels at different types of tasks
- **Cost Optimization**: Smaller models for simple tasks, larger models for complex reasoning
- **Performance Balance**: Optimizes for both quality and response time

**Model Specializations:**
- **Code Tasks** → Nemotron (specialized for programming)
- **Creative Writing** → Llama 70B (excellent for creative tasks)
- **Simple Q&A** → Llama 8B (fast and efficient)
- **Complex Reasoning** → Nemotron or Llama 70B (powerful reasoning capabilities)

### Step 5: Response Generation
The selected model processes your query and generates a response:
- **Educational Enhancement**: Adds step-by-step explanations for learning
- **Contextual Adaptation**: Adjusts complexity based on detected difficulty level
- **Quality Assurance**: Ensures responses are appropriate for educational use

### Why This Matters

**Cost Efficiency**: By using smaller models for simple tasks and larger models only when needed, the system reduces costs by 2-5x compared to always using the largest model.

**Quality Optimization**: Each model is chosen for its strengths, resulting in better responses than a one-size-fits-all approach.

**Speed**: Simple queries get fast responses from efficient models, while complex queries get the computational power they need.

**Learning-Focused**: The routing considers educational value, ensuring responses help you learn rather than just providing answers.

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

Create a `.env` file in the project root:
```bash
# Study Buddy Configuration
SECRET_KEY=study-buddy-dev-secret-key
FLASK_ENV=development

# NVIDIA API Catalog Configuration
NVIDIA_API_KEY="your-nvidia-api-key-here"

# Server Configuration
PORT=5000
HOST=0.0.0.0
```

4. **Deploy Triton Server (Kubernetes)**
```bash
# Deploy Triton server with NodePort
kubectl apply -f triton-deployment.yaml

# Verify deployment
kubectl get svc -n triton
```

5. **Run the application**
```bash
python study_buddy_app.py
```

6. **Open your browser**
Navigate to `http://localhost:5000`

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

### Health Check
```bash
GET /api/health
```

### Statistics
```bash
GET /api/stats
```

## 🎯 Educational Enhancements

While maintaining the official routing core, the application adds educational context:

- **Subject Detection**: Identifies academic subjects using pattern matching
- **Difficulty Assessment**: Determines appropriate academic level
- **Enhanced Prompts**: Adds educational context to improve learning outcomes
- **Progress Tracking**: Monitors learning patterns and model effectiveness
- **Cost Optimization**: Uses appropriate model sizes for 2-5x cost reduction

## 🔧 Configuration

### Environment Variables
- `NVIDIA_API_KEY`: Your NVIDIA API key (required)
- `PORT`: Server port (default: 5000)
- `HOST`: Server host (default: 0.0.0.0)
- `SECRET_KEY`: Flask secret key
- `FLASK_ENV`: Flask environment (development/production)

### Router Configuration
The `nvidia_router_config.yaml` file contains the official NVIDIA LLM Router configuration with policy definitions, model mappings, and API endpoints.

## 🐛 Troubleshooting

### Common Issues

**1. NVIDIA API Key Not Found**
- Ensure `.env` file exists with `NVIDIA_API_KEY` set
- Check that `load_dotenv()` is working in Python files

**2. Triton Server Connection Failed**
- Verify Kubernetes service: `kubectl get svc -n triton`
- Check NodePort accessibility: `curl http://10.185.98.229:30800/v2/health/ready`

**3. Application Health Check**
```bash
curl http://localhost:5000/api/health
```

## 🤝 Contributing

This project implements the official NVIDIA LLM Router logic. For core routing improvements, consider contributing to the [official repository](https://github.com/NVIDIA-AI-Blueprints/llm-router).

For educational enhancements and UI improvements:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the Apache 2.0 License. The NVIDIA LLM Router components are based on the official implementation and maintain the same Apache 2.0 license.

## 🙏 Acknowledgments

- **NVIDIA AI LLM Router Team** (https://github.com/NVIDIA-AI-Blueprints/llm-router) for the official LLM Router implementation
- **NVIDIA NIM** for providing the model APIs
- **Open Source Community** for the foundational libraries

---

**Note**: This implementation uses the exact same core logic as the official NVIDIA LLM Router with Triton inference servers for classification, maintaining full compatibility with the official router architecture.