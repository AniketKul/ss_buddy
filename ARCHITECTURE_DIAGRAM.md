# 🏗️ Smart Study Buddy - High-Level Architecture

## 🌐 Complete System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                    CLIENT LAYER                                        │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│  🌐 Web Browser                    📱 Mobile App                    🔧 API Client      │
│  ├── JavaScript Frontend          ├── React Native                ├── curl/Postman    │
│  ├── Real-time Chat UI           ├── Mobile Interface            ├── Python requests │
│  └── WebSocket Connection        └── HTTP/HTTPS                  └── REST API calls  │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                           │
                                           ▼ HTTP/HTTPS
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                   NETWORK LAYER                                        │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│  🌍 Internet/Intranet             🔒 Load Balancer                🛡️ Firewall         │
│  ├── TCP/IP Routing              ├── HAProxy/Nginx               ├── iptables         │
│  ├── DNS Resolution              ├── SSL Termination             ├── UFW (disabled)   │
│  └── 10.185.99.x Network         └── Health Checks               └── Security Rules   │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                           │
                                           ▼ Port 5000
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                          DPU SERVER (10.185.99.127)                                   │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐   │
│  │                            FLASK APPLICATION LAYER                             │   │
│  ├─────────────────────────────────────────────────────────────────────────────────┤   │
│  │  🚀 Flask Web Server (study_buddy_app.py)                                     │   │
│  │  ├── 🏠 Route: GET /                    → Web Interface                       │   │
│  │  ├── 🎯 Route: POST /api/query          → Main Query Processing               │   │
│  │  ├── 📊 Route: GET /api/stats           → Usage Statistics                    │   │
│  │  ├── ❤️ Route: GET /api/health          → Health Check                        │   │
│  │  ├── ⚙️ Route: GET /api/config          → Configuration Info                  │   │
│  │  └── 🧪 Route: POST /api/test-router    → Router Testing                      │   │
│  └─────────────────────────────────────────────────────────────────────────────────┘   │
│                                           │                                             │
│                                           ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐   │
│  │                        NVIDIA ROUTER SERVICE LAYER                             │   │
│  ├─────────────────────────────────────────────────────────────────────────────────┤   │
│  │  🧠 NVIDIARouterService (nvidia_router_core.py)                               │   │
│  │  ├── 📚 Educational Enhancement                                               │   │
│  │  │   ├── Subject Detection    → Mathematics, Science, CS, etc.               │   │
│  │  │   ├── Difficulty Assessment → Elementary → Graduate                       │   │
│  │  │   └── Context Enrichment   → Educational prompts                          │   │
│  │  │                                                                           │   │
│  │  ├── 🎯 NVIDIA LLM Router Core                                               │   │
│  │  │   ├── Request Parsing      → Extract nim-llm-router params               │   │
│  │  │   ├── Policy Selection     → task_router vs complexity_router            │   │
│  │  │   ├── Message Processing   → Convert to Triton format                    │   │
│  │  │   └── Response Handling    → Parse and format results                    │   │
│  │  │                                                                           │   │
│  │  └── 📊 Statistics & Cost Tracking                                           │   │
│  │      ├── Query Metrics       → Count, timing, subjects                      │   │
│  │      ├── Model Usage         → Track which models used                      │   │
│  │      └── Cost Calculation    → Token-based pricing                          │   │
│  └─────────────────────────────────────────────────────────────────────────────────┘   │
│                                           │                                             │
│                                           ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐   │
│  │                          LOCAL TRITON SERVER                                   │   │
│  ├─────────────────────────────────────────────────────────────────────────────────┤   │
│  │  🔥 CPU-Only Triton Server (localhost:8000)                                   │   │
│  │  ├── 🎯 Task Router Ensemble                                                  │   │
│  │  │   ├── Model: task_router_ensemble                                         │   │
│  │  │   ├── Input: User query text                                              │   │
│  │  │   ├── Output: 12 class probabilities                                      │   │
│  │  │   └── Classes: Brainstorming, Chatbot, Classification, QA, etc.          │   │
│  │  │                                                                           │   │
│  │  ├── 🧠 Complexity Router Ensemble                                           │   │
│  │  │   ├── Model: complexity_router_ensemble                                   │   │
│  │  │   ├── Input: User query text                                              │   │
│  │  │   ├── Output: 7 complexity probabilities                                  │   │
│  │  │   └── Classes: Creativity, Reasoning, Knowledge, etc.                    │   │
│  │  │                                                                           │   │
│  │  └── 🔧 Inference Engine                                                     │   │
│  │      ├── Backend: Python stub processes                                      │   │
│  │      ├── Protocol: HTTP REST API                                             │   │
│  │      └── Endpoints: /v2/models/{model}/infer                                 │   │
│  └─────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐   │
│  │                              CONFIGURATION                                     │   │
│  ├─────────────────────────────────────────────────────────────────────────────────┤   │
│  │  📄 nvidia_router_config.yaml                                                 │   │
│  │  ├── Task Router Policy                                                       │   │
│  │  │   ├── URL: http://localhost:8000/v2/models/task_router_ensemble/infer     │   │
│  │  │   └── 12 LLM Mappings                                                      │   │
│  │  │                                                                           │   │
│  │  ├── Complexity Router Policy                                                 │   │
│  │  │   ├── URL: http://localhost:8000/v2/models/complexity_router_ensemble/... │   │
│  │  │   └── 7 LLM Mappings                                                       │   │
│  │  │                                                                           │   │
│  │  └── 🔑 Environment Variables (.env)                                          │   │
│  │      ├── NVIDIA_API_KEY                                                       │   │
│  │      ├── PORT=5000                                                            │   │
│  │      └── SECRET_KEY                                                           │   │
│  └─────────────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                           │
                                           ▼ HTTPS API Call
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                 NVIDIA CLOUD LAYER                                     │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│  ☁️ NVIDIA API Catalog (integrate.api.nvidia.com)                                     │
│  ├── 🦙 Meta Llama Models                                                              │
│  │   ├── meta/llama-3.1-8b-instruct     → Fast, efficient                           │
│  │   └── meta/llama-3.1-70b-instruct    → High-quality reasoning                    │
│  │                                                                                   │
│  ├── 🚀 NVIDIA Nemotron Models                                                        │
│  │   └── nvidia/llama-3.3-nemotron-super-49b-v1 → Code generation                  │
│  │                                                                                   │
│  ├── 🎭 Mistral Models                                                                │
│  │   └── mistralai/mixtral-8x22b-instruct-v0.1 → Conversational                    │
│  │                                                                                   │
│  └── 🔧 Infrastructure                                                                │
│      ├── GPU Clusters                                                                │
│      ├── Load Balancing                                                              │
│      ├── Auto-scaling                                                                │
│      └── Rate Limiting                                                               │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

## 🔄 Request Flow Diagram

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   CLIENT    │    │   FLASK     │    │   ROUTER    │    │   TRITON    │    │   NVIDIA    │
│   BROWSER   │    │   SERVER    │    │   SERVICE   │    │   SERVER    │    │   CLOUD     │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │                   │                   │
       │ 1. POST /api/query │                   │                   │                   │
       ├──────────────────→ │                   │                   │                   │
       │                   │                   │                   │                   │
       │                   │ 2. Educational    │                   │                   │
       │                   │    Enhancement    │                   │                   │
       │                   ├──────────────────→│                   │                   │
       │                   │                   │                   │                   │
       │                   │                   │ 3. Classification │                   │
       │                   │                   │    Request        │                   │
       │                   │                   ├──────────────────→│                   │
       │                   │                   │                   │                   │
       │                   │                   │ 4. Probabilities  │                   │
       │                   │                   │    Response       │                   │
       │                   │                   │←──────────────────┤                   │
       │                   │                   │                   │                   │
       │                   │                   │ 5. Model Selection│                   │
       │                   │                   │    & API Call     │                   │
       │                   │                   ├─────────────────────────────────────→ │
       │                   │                   │                   │                   │
       │                   │                   │ 6. Generated      │                   │
       │                   │                   │    Response       │                   │
       │                   │                   │←─────────────────────────────────────┤
       │                   │                   │                   │                   │
       │                   │ 7. Formatted      │                   │                   │
       │                   │    Response       │                   │                   │
       │                   │←──────────────────┤                   │                   │
       │                   │                   │                   │                   │
       │ 8. JSON Response  │                   │                   │                   │
       │←──────────────────┤                   │                   │                   │
       │                   │                   │                   │                   │
```

## 🎯 Model Selection Matrix

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              TASK ROUTER MAPPING                                       │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│  Query Type          │ Triton Class     │ Selected Model                │ Use Case        │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│  "Brainstorm ideas"  │ Brainstorming    │ meta/llama-3.1-70b-instruct  │ Creative tasks  │
│  "Chat with me"      │ Chatbot          │ mixtral-8x22b-instruct-v0.1  │ Conversation    │
│  "Categorize this"   │ Classification   │ meta/llama-3.1-8b-instruct   │ Simple classify │
│  "What is X?"        │ Closed QA        │ meta/llama-3.1-70b-instruct  │ Factual Q&A     │
│  "Write Python code" │ Code Generation  │ nemotron-super-49b-v1        │ Programming     │
│  "Extract data"      │ Extraction       │ meta/llama-3.1-8b-instruct   │ Data extraction │
│  "Explain concept"   │ Open QA          │ meta/llama-3.1-70b-instruct  │ General Q&A     │
│  "Misc request"      │ Other            │ mixtral-8x22b-instruct-v0.1  │ Miscellaneous   │
│  "Rewrite text"      │ Rewrite          │ meta/llama-3.1-8b-instruct   │ Text editing    │
│  "Summarize this"    │ Summarization    │ meta/llama-3.1-70b-instruct  │ Summarization   │
│  "Generate story"    │ Text Generation  │ mixtral-8x22b-instruct-v0.1  │ Creative writing│
│  "Unknown intent"    │ Unknown          │ meta/llama-3.1-8b-instruct   │ Fallback        │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

## 📊 Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                 DATA FLOW                                              │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  📝 User Query: "How does machine learning work?"                                       │
│                                    │                                                   │
│                                    ▼                                                   │
│  🧠 Educational Enhancement                                                             │
│  ├── Subject: "Computer Science"                                                       │
│  ├── Difficulty: "Elementary"                                                          │
│  └── Enhanced Prompt: "You are a study buddy..."                                       │
│                                    │                                                   │
│                                    ▼                                                   │
│  🎯 Triton Classification                                                               │
│  ├── Input: "How does machine learning work?"                                          │
│  ├── Processing: task_router_ensemble model                                            │
│  └── Output: [0.16, 0.18, 0.10, 0.001, 0.038, 0.096, 0.189, ...]                    │
│                                    │                                                   │
│                                    ▼                                                   │
│  🔍 Model Selection                                                                     │
│  ├── Highest Probability: Index 6 (0.189)                                             │
│  ├── Selected Class: "Open QA"                                                         │
│  └── Chosen Model: "meta/llama-3.1-70b-instruct"                                      │
│                                    │                                                   │
│                                    ▼                                                   │
│  ☁️ NVIDIA API Call                                                                    │
│  ├── URL: https://integrate.api.nvidia.com/v1/chat/completions                        │
│  ├── Model: meta/llama-3.1-70b-instruct                                               │
│  ├── Headers: Authorization: Bearer ${NVIDIA_API_KEY}                                  │
│  └── Body: {"model": "meta/llama-3.1-70b-instruct", "messages": [...]}               │
│                                    │                                                   │
│                                    ▼                                                   │
│  📤 Response Processing                                                                 │
│  ├── Generated Text: "Machine learning is a subset of AI..."                          │
│  ├── Usage: {"prompt_tokens": 45, "completion_tokens": 294}                           │
│  ├── Cost: $0.0002 * 45/1000 + $0.0006 * 294/1000 = $0.000185                      │
│  └── Response Time: 3.18 seconds                                                       │
│                                    │                                                   │
│                                    ▼                                                   │
│  📊 Final JSON Response                                                                 │
│  {                                                                                     │
│    "response": "Machine learning is a subset of AI...",                               │
│    "model_used": "meta/llama-3.1-70b-instruct",                                       │
│    "classifier_used": "Open QA",                                                       │
│    "policy_used": "task_router",                                                       │
│    "routing_strategy": "triton",                                                       │
│    "detected_subject": "Computer Science",                                             │
│    "detected_difficulty": "Elementary",                                                │
│    "response_time": 3.18,                                                              │
│    "usage": {...}                                                                      │
│  }                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

## 🔧 Technology Stack

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                               TECHNOLOGY STACK                                         │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│  Layer              │ Technology                    │ Purpose                           │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│  🌐 Frontend         │ HTML5, CSS3, JavaScript      │ User Interface                    │
│  🚀 Web Framework    │ Flask (Python)               │ HTTP Server & API                 │
│  🧠 AI Routing       │ NVIDIA LLM Router            │ Intelligent Model Selection       │
│  🔥 Local Inference  │ Triton Inference Server      │ CPU-only Classification           │
│  ☁️ Cloud LLMs       │ NVIDIA API Catalog           │ Text Generation                   │
│  📊 Data Storage     │ JSON Files                   │ Statistics & Configuration        │
│  🔧 Configuration    │ YAML, Environment Variables  │ System Configuration              │
│  🐍 Programming      │ Python 3.10+                │ Main Application Logic            │
│  📦 Dependencies     │ pip, requirements.txt        │ Package Management                │
│  🐳 Containerization│ Docker (optional)            │ Deployment                        │
│  🌍 Networking       │ HTTP/HTTPS, REST APIs       │ Communication                     │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

## 🎯 Key Architectural Benefits

1. **🔥 Local Intelligence**: DPU handles all routing decisions
2. **☁️ Cloud Scale**: Leverages NVIDIA's powerful models
3. **💰 Cost Optimized**: Right-sized models for each task
4. **⚡ Performance**: Parallel processing and efficient routing
5. **🛡️ Resilient**: Graceful error handling and fallbacks
6. **📊 Observable**: Comprehensive metrics and monitoring
7. **🔧 Configurable**: Easy to modify models and policies
8. **🎓 Educational**: Context-aware responses for learning

This architecture provides the perfect balance of local control and cloud capabilities! 🚀 