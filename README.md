# Smart Study Buddy - Educational AI Assistant

**Now powered by the Official NVIDIA LLM Router Framework**

An intelligent educational assistant that uses the **exact same core logic** as the [official NVIDIA LLM Router](https://github.com/NVIDIA-AI-Blueprints/llm-router) to route educational queries to the most appropriate AI models for optimal learning experiences.

## 🚀 Key Features

### Official NVIDIA LLM Router Integration
- **Exact Implementation**: Uses the same routing logic as the official NVIDIA LLM Router repository
- **Triton Classification**: Uses Triton inference servers for model classification
- **OpenAI-Compatible API**: Follows the official OpenAI API specification with NVIDIA extensions

### Educational Enhancements
- **Subject Detection**: Automatically identifies the academic subject (Math, Science, History, etc.)
- **Difficulty Assessment**: Determines appropriate academic level (Elementary to Graduate)
- **Learning-Optimized Responses**: Provides step-by-step explanations tailored to the detected level
- **Real-time Statistics**: Tracks usage patterns and model performance

### Modern Web Interface
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Real-time Chat**: Interactive conversation interface with typing indicators
- **Model Transparency**: Shows which AI model and routing policy was used for each response
- **Performance Metrics**: Displays response times and token usage

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

## 🔧 Implementation Details

### Core Components

1. **`nvidia_router_core.py`** - Official NVIDIA LLM Router implementation
   - `NVIDIALLMRouterCore`: Exact replication of Rust proxy.rs logic
   - `RouterConfig`: Configuration loading with YAML support
   - `Policy` & `Llm`: Data structures matching official schema

2. **`nvidia_router_config.yaml`** - Official configuration file
   - Copied directly from the official repository
   - Contains exact model mappings and Triton server URLs

3. **`study_buddy_app.py`** - Flask application with educational enhancements
   - Wraps the official router core with educational context
   - Provides web API and user interface

### Key Differences from Previous Implementation

| Aspect | Previous (Pattern-Based) | Current (Official NVIDIA Router) |
|--------|-------------------------|----------------------------------|
| **Classification** | Keyword pattern matching | Triton inference servers |
| **Model Selection** | Simple heuristics | Pre-trained classification models |
| **API Format** | Custom format | Official OpenAI + NVIDIA extensions |
| **Routing Logic** | Educational-specific patterns | Enterprise-grade routing policies |
| **Scalability** | Limited to predefined patterns | ML-based classification with continuous learning |
| **Compatibility** | Custom implementation | Compatible with official NVIDIA infrastructure |

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- NVIDIA API Key ([Get one here](https://build.nvidia.com/))

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

4. **Run the application**
```bash
python study_buddy_app.py
```

5. **Open your browser**
Navigate to `http://localhost:5000`

### Docker Deployment

```bash
# Build the image
docker build -t smart-study-buddy .

# Run with your API key
docker run -p 5000:5000 -e NVIDIA_API_KEY="your-key" smart-study-buddy
```

## 📊 API Endpoints

### Educational Query Processing
```bash
POST /api/query
{
  "query": "Explain photosynthesis",
  "policy": "task_router",
  "routing_strategy": "triton"
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

## 🔍 Routing Logic Explanation

The application uses the **exact same routing logic** as the official NVIDIA LLM Router:

### Step 1: Request Parsing
- Extracts `nim-llm-router` parameters from request body
- Validates policy name and routing strategy
- Prepares messages for classification

### Step 2: Policy Selection
- Chooses between `task_router` and `complexity_router` policies
- Each policy has its own classification model and model mappings

### Step 3: Classification
- **Triton Path**: Sends request to Triton inference server
  - Creates `INPUT` tensor with query text
  - Receives probability distribution over categories
  - Selects category with highest probability

### Step 4: Model Selection
- Maps classification result to specific NVIDIA model
- Uses exact model mappings from official configuration

### Step 5: Request Proxying
- Removes `nim-llm-router` parameters
- Sets correct model name in request
- Forwards to selected NVIDIA model API
- Returns response with routing metadata

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

### Router Configuration
The `nvidia_router_config.yaml` file contains the official NVIDIA LLM Router configuration:
- Policy definitions with Triton server URLs
- Model mappings for each classification category
- API endpoints and authentication settings

## 📈 Monitoring & Analytics

- **Real-time Statistics**: Query counts, response times, model usage
- **Policy Analytics**: Usage patterns across routing policies
- **Educational Metrics**: Subject and difficulty level distributions
- **Performance Tracking**: Average response times and token usage

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