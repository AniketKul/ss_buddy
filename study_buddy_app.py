#!/usr/bin/env python3
"""
Smart Study Buddy - Educational AI Assistant
Now powered by the official NVIDIA LLM Router framework

This application uses the exact same core logic as the official NVIDIA LLM Router:
https://github.com/NVIDIA-AI-Blueprints/llm-router

Features:
- Official NVIDIA LLM Router implementation with Triton classification
- Educational context detection and enhancement
- Modern web interface with real-time chat
- Docker deployment support
"""

import os
import asyncio
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import json

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Import the official NVIDIA LLM Router implementation
from nvidia_router_core import NVIDIARouterService, RouterConfig

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Initialize NVIDIA LLM Router Service
try:
    # Try to load from config file first
    if os.path.exists('nvidia_router_config.yaml'):
        nvidia_router = NVIDIARouterService('nvidia_router_config.yaml')
        logger.info("Loaded NVIDIA LLM Router with configuration file")
    else:
        # Use default embedded configuration
        nvidia_router = NVIDIARouterService()
        logger.info("Loaded NVIDIA LLM Router with default configuration")
except Exception as e:
    logger.error(f"Failed to initialize NVIDIA LLM Router: {e}")
    nvidia_router = None

# Statistics tracking
stats = {
    'total_queries': 0,
    'queries_by_subject': {},
    'queries_by_difficulty': {},
    'queries_by_policy': {},
    'queries_by_model': {},
    'average_response_time': 0,
    'total_response_time': 0
}

@app.route('/')
def index():
    """Serve the main application page"""
    return render_template('index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files"""
    return send_from_directory('static', filename)

@app.route('/api/query', methods=['POST'])
def handle_query():
    """
    Handle educational queries using official NVIDIA LLM Router logic
    """
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        policy = data.get('policy', 'task_router')  # task_router or complexity_router
        routing_strategy = data.get('routing_strategy', 'triton')  # triton or manual
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        if not nvidia_router:
            return jsonify({
                'error': 'NVIDIA LLM Router not available',
                'response': 'I apologize, but the routing service is currently unavailable. Please try again later.',
                'model_used': 'unavailable'
            }), 500
        
        # Process query using official NVIDIA LLM Router
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(
                nvidia_router.process_educational_query(query, policy, routing_strategy)
            )
        finally:
            loop.close()
        
        # Update statistics
        stats['total_queries'] += 1
        
        if 'detected_subject' in result:
            subject = result['detected_subject']
            stats['queries_by_subject'][subject] = stats['queries_by_subject'].get(subject, 0) + 1
        
        if 'detected_difficulty' in result:
            difficulty = result['detected_difficulty']
            stats['queries_by_difficulty'][difficulty] = stats['queries_by_difficulty'].get(difficulty, 0) + 1
        
        if 'policy_used' in result:
            policy_used = result['policy_used']
            stats['queries_by_policy'][policy_used] = stats['queries_by_policy'].get(policy_used, 0) + 1
        
        if 'model_used' in result:
            model = result['model_used']
            stats['queries_by_model'][model] = stats['queries_by_model'].get(model, 0) + 1
        
        if 'response_time' in result:
            response_time = result['response_time']
            stats['total_response_time'] += response_time
            stats['average_response_time'] = stats['total_response_time'] / stats['total_queries']
        
        # Add timestamp
        result['timestamp'] = datetime.now().isoformat()
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        return jsonify({
            'error': str(e),
            'response': 'I apologize, but I encountered an error processing your question. Please try again.',
            'model_used': 'error',
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/stats')
def get_stats():
    """Get application statistics"""
    return jsonify(stats)

@app.route('/api/config')
def get_config():
    """Get router configuration information"""
    if not nvidia_router:
        return jsonify({'error': 'Router not available'}), 500
    
    config_info = {
        'policies': [],
        'total_models': 0
    }
    
    for policy in nvidia_router.config.policies:
        policy_info = {
            'name': policy.name,
            'models': [llm.name for llm in policy.llms],
            'model_count': len(policy.llms)
        }
        config_info['policies'].append(policy_info)
        config_info['total_models'] += len(policy.llms)
    
    return jsonify(config_info)

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    health_status = {
        'status': 'healthy',
        'nvidia_router_available': nvidia_router is not None,
        'nvidia_api_key_configured': bool(os.getenv('NVIDIA_API_KEY')),
        'timestamp': datetime.now().isoformat()
    }
    
    if nvidia_router:
        health_status['policies_loaded'] = len(nvidia_router.config.policies)
        health_status['total_models'] = sum(len(policy.llms) for policy in nvidia_router.config.policies)
    
    return jsonify(health_status)

@app.route('/api/test-router', methods=['POST'])
def test_router():
    """
    Test the NVIDIA LLM Router with a sample query
    This endpoint demonstrates the official router API format
    """
    try:
        data = request.get_json()
        policy = data.get('policy', 'task_router')
        routing_strategy = data.get('routing_strategy', 'triton')
        model = data.get('model')  # For manual routing
        
        if not nvidia_router:
            return jsonify({'error': 'Router not available'}), 500
        
        # Create a test request in official NVIDIA LLM Router format
        test_request = {
            "model": "",  # Will be filled by router
            "messages": [
                {
                    "role": "user",
                    "content": "Can you write me a song? Use as many emojis as possible."
                }
            ],
            "max_tokens": 64,
            "stream": False,
            "nim-llm-router": {
                "policy": policy,
                "routing_strategy": routing_strategy
            }
        }
        
        # Add model for manual routing
        if routing_strategy == 'manual' and model:
            test_request["nim-llm-router"]["model"] = model
        
        # Process using the router core
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            response_data, chosen_model, chosen_classifier = loop.run_until_complete(
                nvidia_router.router_core.route_request(test_request)
            )
        finally:
            loop.close()
        
        return jsonify({
            'success': True,
            'chosen_model': chosen_model,
            'chosen_classifier': chosen_classifier,
            'policy_used': policy,
            'routing_strategy': routing_strategy,
            'response_preview': response_data['choices'][0]['message']['content'][:200] + '...',
            'usage': response_data.get('usage', {}),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Router test failed: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

if __name__ == '__main__':
    # Check for required environment variables
    if not os.getenv('NVIDIA_API_KEY'):
        logger.warning("NVIDIA_API_KEY not set. The application may not work properly.")
        print("\n" + "="*60)
        print("WARNING: NVIDIA_API_KEY environment variable not set!")
        print("Please set your NVIDIA API key:")
        print("export NVIDIA_API_KEY='your-api-key-here'")
        print("="*60 + "\n")
    
    # Get port from environment or default to 5000
    port = int(os.getenv('PORT', 5000))
    
    logger.info("Starting Smart Study Buddy with Official NVIDIA LLM Router")
    logger.info(f"Server will be available at http://localhost:{port}")
    
    if nvidia_router:
        logger.info(f"Router loaded with {len(nvidia_router.config.policies)} policies")
        for policy in nvidia_router.config.policies:
            logger.info(f"  - {policy.name}: {len(policy.llms)} models")
    
    app.run(host='0.0.0.0', port=port, debug=False) 