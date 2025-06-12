# 🎓 Smart Study Buddy Assistant

An intelligent educational assistant that leverages **NVIDIA API Catalog** to provide personalized learning support. The system automatically detects the subject and difficulty level of student questions, then routes them to the most appropriate AI model for optimal responses.

## ✨ Features

- **🤖 Intelligent Query Routing**: Automatically classifies questions and routes to specialized models
- **📚 Auto-Detection**: Detects subject (9 categories) and difficulty level (5 levels) from questions
- **🎯 Specialized Models**: Uses different NVIDIA models optimized for specific tasks:
  - **Simple Q&A**: Llama 3.1 8B (fast, efficient)
  - **Complex Reasoning**: Llama 3.1 70B (deep analysis)
  - **Code Generation**: CodeLlama 70B (programming help)
  - **Creative Writing**: Mixtral 8x7B (creative tasks)
  - **Mathematics**: Nemotron 4 340B (advanced math)
- **💰 Cost Tracking**: Real-time cost estimation and session statistics
- **📊 Session Analytics**: Track queries, costs, and learning progress
- **🎨 Modern UI**: Clean, responsive interface optimized for learning

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- NVIDIA API Catalog account and API key

### Installation

1. **Clone and setup:**
   ```bash
   git clone <repository-url>
   cd ss_buddy
   chmod +x setup.sh
   ./setup.sh
   ```

2. **Get your NVIDIA API key:**
   - Visit [NVIDIA API Catalog](https://build.nvidia.com/explore/discover)
   - Sign up/login and generate an API key
   - Add it to your `.env` file:
     ```
     NVIDIA_API_KEY=your-actual-api-key-here
     ```

3. **Start the application:**
   ```bash
   source venv/bin/activate
   python study_buddy_app.py
   ```

4. **Open your browser:**
   - Navigate to `http://localhost:5000`
   - Start asking questions!

## 🎯 How It Works

### Automatic Detection
The system analyzes your question to automatically determine:

**Subject Categories:**
- Mathematics, Science, Computer Science
- History, Literature, Physics
- Chemistry, Biology, Economics

**Difficulty Levels:**
- Elementary, Middle School, High School
- College, Graduate

**Task Types:**
- Simple Q&A, Complex Reasoning
- Code Generation, Creative Writing
- Mathematics

### Model Routing
Based on the analysis, your question is routed to the most appropriate NVIDIA model:

| Task Type | Model | Strengths |
|-----------|-------|-----------|
| Simple Q&A | Llama 3.1 8B | Fast, clear explanations |
| Complex Reasoning | Llama 3.1 70B | Deep analysis, step-by-step |
| Code Generation | CodeLlama 70B | Programming expertise |
| Creative Writing | Mixtral 8x7B | Creative, inspiring |
| Mathematics | Nemotron 4 340B | Advanced mathematical reasoning |

## 💡 Example Usage

Simply type your question - no need to specify subject or difficulty:

- **"What is photosynthesis?"** → Auto-detected as Biology/High School → Llama 3.1 8B
- **"Explain quantum entanglement"** → Auto-detected as Physics/College → Llama 3.1 70B  
- **"Write a Python function to sort a list"** → Auto-detected as Computer Science/High School → CodeLlama 70B
- **"Solve: ∫x²dx from 0 to 5"** → Auto-detected as Mathematics/College → Nemotron 4 340B

## 🏗️ Architecture

```
Student Question
       ↓
Task Classifier (Auto-detect subject/difficulty/type)
       ↓
LLM Router (Select optimal NVIDIA model)
       ↓
NVIDIA API Catalog (Generate response)
       ↓
Educational Response + Analytics
```

## 📊 API Endpoints

- `GET /` - Main application interface
- `POST /api/query` - Submit study questions
- `GET /api/stats` - Get session statistics
- `GET /health` - Health check

## 🔧 Configuration

Environment variables in `.env`:

```bash
# Application
SECRET_KEY=your-secret-key
FLASK_ENV=development
FLASK_DEBUG=True

# NVIDIA API
NVIDIA_API_KEY=your-nvidia-api-key

# Server
PORT=5000
HOST=0.0.0.0
```

## 🐳 Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build manually
docker build -t study-buddy .
docker run -p 5000:5000 --env-file .env study-buddy
```

## 📈 Cost Management

The system provides real-time cost tracking:
- Per-query cost estimation
- Session total costs
- Model usage statistics
- Cost-optimized routing

## 🛠️ Development

### Project Structure
```
ss_buddy/
├── study_buddy_app.py      # Main Flask application
├── templates/
│   └── index.html          # Web interface
├── static/
│   ├── css/style.css       # Styling
│   └── js/app.js          # Frontend logic
├── requirements.txt        # Python dependencies
├── Dockerfile             # Container configuration
├── docker-compose.yml     # Multi-service setup
└── setup.sh              # Automated setup
```

### Adding New Models
To add support for new NVIDIA models, update the `MODEL_CONFIGS` in `study_buddy_app.py`:

```python
MODEL_CONFIGS = {
    'new_task_type': {
        'model': 'nvidia/new-model-name',
        'cost_per_token': 0.001,
        'max_tokens': 1024,
        'temperature': 0.5
    }
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

- Check the health endpoint: `curl http://localhost:5000/health`
- Review logs for debugging
- Ensure your NVIDIA API key is valid
- Verify network connectivity to NVIDIA API Catalog

## 🎯 Roadmap

- [ ] Add more specialized models
- [ ] Implement user authentication
- [ ] Add conversation history
- [ ] Support for file uploads
- [ ] Multi-language support
- [ ] Advanced analytics dashboard

---

**Built with ❤️ using NVIDIA API Catalog for intelligent educational assistance** 