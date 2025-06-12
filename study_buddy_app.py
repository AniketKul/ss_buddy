#!/usr/bin/env python3
"""
Smart Study Buddy Assistant - Main Application
Leverages NVIDIA API Catalog for intelligent educational assistance
"""

import os
import json
import time
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from flask import Flask, render_template, request, jsonify, session
import requests
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'study-buddy-secret-key-change-in-production')

# Configuration
NVIDIA_API_KEY = os.environ.get('NVIDIA_API_KEY', '')
NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"

@dataclass
class StudyQuery:
    """Represents a study query with metadata"""
    query: str
    subject: str
    difficulty: str
    query_type: str
    timestamp: datetime
    user_id: str
    
@dataclass
class StudyResponse:
    """Represents a response from the study buddy"""
    response: str
    model_used: str
    cost: float
    response_time: float
    confidence: float

class TaskClassifier:
    """Classifies study queries into appropriate categories"""
    
    TASK_PATTERNS = {
        'simple_qa': [
            'what is', 'define', 'definition of', 'meaning of', 'who is', 'when did',
            'where is', 'how many', 'list', 'name', 'identify'
        ],
        'complex_reasoning': [
            'explain why', 'analyze', 'compare', 'contrast', 'evaluate', 'justify',
            'argue', 'discuss', 'examine', 'assess', 'critique', 'synthesize'
        ],
        'code_generation': [
            'write code', 'program', 'function', 'algorithm', 'debug', 'fix code',
            'implement', 'class', 'method', 'variable', 'loop', 'if statement'
        ],
        'creative_writing': [
            'write essay', 'creative writing', 'story', 'poem', 'brainstorm',
            'generate ideas', 'outline', 'draft', 'narrative', 'persuasive'
        ],
        'mathematics': [
            'solve', 'calculate', 'equation', 'formula', 'derivative', 'integral',
            'probability', 'statistics', 'geometry', 'algebra', 'calculus'
        ]
    }
    
    SUBJECT_PATTERNS = {
        'Mathematics': [
            'math', 'algebra', 'calculus', 'geometry', 'trigonometry', 'statistics',
            'probability', 'equation', 'derivative', 'integral', 'solve', 'calculate'
        ],
        'Science': [
            'science', 'physics', 'chemistry', 'biology', 'experiment', 'molecule',
            'atom', 'cell', 'DNA', 'evolution', 'photosynthesis', 'gravity'
        ],
        'Computer Science': [
            'programming', 'code', 'algorithm', 'function', 'variable', 'loop',
            'python', 'javascript', 'java', 'C++', 'database', 'API'
        ],
        'History': [
            'history', 'war', 'revolution', 'ancient', 'medieval', 'century',
            'empire', 'civilization', 'historical', 'timeline'
        ],
        'Literature': [
            'literature', 'novel', 'poem', 'poetry', 'author', 'character',
            'plot', 'theme', 'metaphor', 'essay', 'writing'
        ],
        'Physics': [
            'physics', 'force', 'energy', 'momentum', 'velocity', 'acceleration',
            'quantum', 'relativity', 'electromagnetic', 'thermodynamics'
        ],
        'Chemistry': [
            'chemistry', 'chemical', 'reaction', 'compound', 'element', 'periodic',
            'molecule', 'bond', 'acid', 'base', 'organic', 'inorganic'
        ],
        'Biology': [
            'biology', 'cell', 'organism', 'DNA', 'gene', 'evolution', 'ecosystem',
            'photosynthesis', 'respiration', 'anatomy', 'physiology'
        ],
        'Economics': [
            'economics', 'market', 'supply', 'demand', 'inflation', 'GDP',
            'trade', 'investment', 'capitalism', 'socialism'
        ]
    }
    
    DIFFICULTY_PATTERNS = {
        'Elementary': [
            'simple', 'basic', 'easy', 'beginner', 'introduction', 'what is',
            'elementary', 'grade school'
        ],
        'Middle School': [
            'middle school', 'junior high', 'intermediate', 'explain simply'
        ],
        'High School': [
            'high school', 'secondary', 'advanced', 'AP', 'honors'
        ],
        'College': [
            'college', 'university', 'undergraduate', 'bachelor', 'academic',
            'research', 'thesis', 'complex'
        ],
        'Graduate': [
            'graduate', 'masters', 'PhD', 'doctoral', 'research', 'advanced study',
            'dissertation', 'scholarly'
        ]
    }
    
    @classmethod
    def classify_query(cls, query: str) -> str:
        """Classify a query into one of the task categories"""
        query_lower = query.lower()
        
        # Count matches for each category
        category_scores = {}
        for category, patterns in cls.TASK_PATTERNS.items():
            score = sum(1 for pattern in patterns if pattern in query_lower)
            if score > 0:
                category_scores[category] = score
        
        # Return category with highest score, default to complex_reasoning
        if category_scores:
            return max(category_scores.items(), key=lambda x: x[1])[0]
        return 'complex_reasoning'
    
    @classmethod
    def detect_subject(cls, query: str) -> str:
        """Automatically detect the subject from the query"""
        query_lower = query.lower()
        
        # Count matches for each subject
        subject_scores = {}
        for subject, patterns in cls.SUBJECT_PATTERNS.items():
            score = sum(1 for pattern in patterns if pattern in query_lower)
            if score > 0:
                subject_scores[subject] = score
        
        # Return subject with highest score, default to General
        if subject_scores:
            return max(subject_scores.items(), key=lambda x: x[1])[0]
        return 'General'
    
    @classmethod
    def detect_difficulty(cls, query: str) -> str:
        """Automatically detect the difficulty level from the query"""
        query_lower = query.lower()
        
        # Count matches for each difficulty level
        difficulty_scores = {}
        for difficulty, patterns in cls.DIFFICULTY_PATTERNS.items():
            score = sum(1 for pattern in patterns if pattern in query_lower)
            if score > 0:
                difficulty_scores[difficulty] = score
        
        # Additional heuristics for difficulty detection
        word_count = len(query.split())
        complexity_indicators = [
            'analyze', 'evaluate', 'synthesize', 'critique', 'compare', 'contrast',
            'justify', 'argue', 'discuss', 'examine', 'assess'
        ]
        
        has_complexity = any(indicator in query_lower for indicator in complexity_indicators)
        
        # If we have explicit difficulty matches, use those
        if difficulty_scores:
            detected_difficulty = max(difficulty_scores.items(), key=lambda x: x[1])[0]
        else:
            # Use heuristics based on query complexity
            if word_count < 5:
                detected_difficulty = 'Elementary'
            elif word_count < 10 and not has_complexity:
                detected_difficulty = 'Middle School'
            elif word_count < 15 or not has_complexity:
                detected_difficulty = 'High School'
            elif has_complexity:
                detected_difficulty = 'College'
            else:
                detected_difficulty = 'High School'  # Default
        
        return detected_difficulty

class LLMRouter:
    """Interface to NVIDIA API Catalog for real model responses"""
    
    MODEL_CONFIGS = {
        'simple_qa': {
            'model': 'meta/llama-3.1-8b-instruct',
            'cost_per_token': 0.0002,
            'max_tokens': 512,
            'temperature': 0.3
        },
        'complex_reasoning': {
            'model': 'meta/llama-3.1-70b-instruct',
            'cost_per_token': 0.0006,
            'max_tokens': 1024,
            'temperature': 0.7
        },
        'code_generation': {
            'model': 'meta/codellama-70b',
            'cost_per_token': 0.0006,
            'max_tokens': 2048,
            'temperature': 0.1
        },
        'creative_writing': {
            'model': 'mistralai/mixtral-8x7b-instruct-v0.1',
            'cost_per_token': 0.0005,
            'max_tokens': 1536,
            'temperature': 0.8
        },
        'mathematics': {
            'model': 'nvidia/nemotron-4-340b-instruct',
            'cost_per_token': 0.008,
            'max_tokens': 1024,
            'temperature': 0.2
        }
    }
    
    def __init__(self):
        self.api_key = NVIDIA_API_KEY
        self.base_url = NVIDIA_BASE_URL
    
    def route_query(self, query: StudyQuery) -> StudyResponse:
        """Route a study query to the appropriate model"""
        start_time = time.time()
        
        # Classify the query
        task_type = TaskClassifier.classify_query(query.query)
        model_config = self.MODEL_CONFIGS.get(task_type, self.MODEL_CONFIGS['complex_reasoning'])
        
        # Prepare the prompt with educational context
        educational_prompt = self._prepare_educational_prompt(query, task_type)
        
        try:
            # Make request to NVIDIA API
            response = self._make_nvidia_request(educational_prompt, model_config, task_type)
            
            response_time = time.time() - start_time
            estimated_cost = self._estimate_cost(response, model_config)
            
            return StudyResponse(
                response=response,
                model_used=model_config['model'],
                cost=estimated_cost,
                response_time=response_time,
                confidence=0.9
            )
            
        except Exception as e:
            logger.error(f"Error routing query: {e}")
            # Fallback to a helpful educational response
            fallback_response = self._generate_fallback_response(query, task_type)
            return StudyResponse(
                response=fallback_response,
                model_used="fallback",
                cost=0.0,
                response_time=time.time() - start_time,
                confidence=0.5
            )
    
    def _prepare_educational_prompt(self, query: StudyQuery, task_type: str) -> str:
        """Prepare an educational prompt based on query type"""
        base_prompt = f"""You are a helpful study buddy assistant. The student is asking about {query.subject} at a {query.difficulty} level.

Student's question: {query.query}

Please provide a clear, educational response that:
1. Directly answers the question
2. Explains concepts in an age-appropriate way for {query.difficulty} level
3. Provides examples when helpful
4. Encourages further learning

"""
        
        # Add task-specific instructions
        if task_type == 'simple_qa':
            base_prompt += "Keep your answer concise but complete. Focus on the key facts and definitions."
        elif task_type == 'complex_reasoning':
            base_prompt += "Break down your reasoning step by step. Help the student understand the 'why' behind the answer. Use logical progression."
        elif task_type == 'code_generation':
            base_prompt += "Provide working code with clear comments. Explain what each part does and why. Include best practices."
        elif task_type == 'creative_writing':
            base_prompt += "Be creative and inspiring. Provide concrete examples and techniques. Encourage imagination."
        elif task_type == 'mathematics':
            base_prompt += "Show your work step by step. Explain each mathematical operation clearly. Verify your answer."
        
        return base_prompt
    
    def _make_nvidia_request(self, prompt: str, model_config: Dict, task_type: str) -> str:
        """Make request to NVIDIA API Catalog"""
        if not self.api_key:
            logger.warning("No NVIDIA API key provided, using fallback response")
            return self._generate_fallback_response_by_type(task_type)
        
        try:
            model_name = model_config['model']
            max_tokens = model_config['max_tokens']
            temperature = model_config['temperature']
            
            # Make the API call using HTTP requests
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": model_name,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": temperature,
                "max_tokens": max_tokens,
                "top_p": 1,
                "frequency_penalty": 0,
                "presence_penalty": 0
            }
            
            response = requests.post(f"{self.base_url}/v1/chat/completions", headers=headers, json=data)
            response.raise_for_status()
            
            # Extract the response
            response_json = response.json()
            response_text = response_json['choices'][0]['message']['content']
            return response_text.strip() if response_text else "I apologize, but I couldn't generate a response."
                
        except Exception as e:
            logger.error(f"NVIDIA API error: {e}")
            return self._generate_fallback_response_by_type(task_type)
    
    def _generate_fallback_response_by_type(self, task_type: str) -> str:
        """Generate appropriate fallback responses by task type"""
        fallbacks = {
            'simple_qa': "I can help explain this concept! This is a fundamental topic that involves key principles and definitions. Let me break it down in simple terms for better understanding.",
            'complex_reasoning': "This is an interesting question that requires careful analysis. Let me walk through the reasoning step by step, considering multiple perspectives and examining the underlying principles.",
            'code_generation': "Here's how we can approach this programming problem:\n\n```python\n# This is a sample code structure\n# We would implement the solution step by step\n# with clear comments explaining each part\n```\n\nLet me explain the logic and best practices involved.",
            'creative_writing': "What a creative challenge! Let's explore this topic with imagination and inspiration. Consider these approaches: brainstorming unique angles, developing compelling narratives, and using vivid descriptions to engage your audience.",
            'mathematics': "Let's solve this step by step:\n\n1. First, identify what we're looking for\n2. Apply the relevant mathematical principles\n3. Work through the calculations systematically\n4. Verify our answer makes sense\n\nMathematics is about logical progression and clear reasoning."
        }
        return fallbacks.get(task_type, "I'm here to help you learn! Let me provide a thoughtful response to your question.")
    
    def _generate_fallback_response(self, query: StudyQuery, task_type: str) -> str:
        """Generate a contextual fallback response"""
        base_response = self._generate_fallback_response_by_type(task_type)
        return f"Regarding your {query.subject} question at the {query.difficulty} level: {base_response}"
    
    def _estimate_cost(self, response: str, model_config: Dict) -> float:
        """Estimate the cost of the response"""
        # Rough token estimation (4 chars per token average)
        estimated_tokens = len(response) // 4
        return estimated_tokens * model_config['cost_per_token']

class StudyBuddyService:
    """Main service class for the Study Buddy application"""
    
    def __init__(self):
        self.router = LLMRouter()
        self.user_sessions = {}  # In production, use a proper database
    
    def process_study_query(self, user_id: str, query_text: str) -> Dict:
        """Process a study query and return response with metadata"""
        
        # Automatically detect subject and difficulty from the query
        detected_subject = TaskClassifier.detect_subject(query_text)
        detected_difficulty = TaskClassifier.detect_difficulty(query_text)
        
        # Create study query object
        study_query = StudyQuery(
            query=query_text,
            subject=detected_subject,
            difficulty=detected_difficulty,
            query_type="",  # Will be determined by classifier
            timestamp=datetime.now(),
            user_id=user_id
        )
        
        # Route query and get response
        response = self.router.route_query(study_query)
        
        # Update user session
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = {
                'queries': [],
                'total_cost': 0.0,
                'session_start': datetime.now()
            }
        
        self.user_sessions[user_id]['queries'].append({
            'query': asdict(study_query),
            'response': asdict(response)
        })
        self.user_sessions[user_id]['total_cost'] += response.cost
        
        return {
            'response': response.response,
            'model_used': response.model_used,
            'cost': response.cost,
            'response_time': response.response_time,
            'confidence': response.confidence,
            'session_cost': self.user_sessions[user_id]['total_cost'],
            'detected_subject': detected_subject,
            'detected_difficulty': detected_difficulty
        }
    
    def get_user_stats(self, user_id: str) -> Dict:
        """Get user session statistics"""
        if user_id not in self.user_sessions:
            return {'queries': 0, 'total_cost': 0.0, 'session_time': 0}
        
        session = self.user_sessions[user_id]
        session_time = (datetime.now() - session['session_start']).total_seconds() / 60  # minutes
        
        return {
            'queries': len(session['queries']),
            'total_cost': session['total_cost'],
            'session_time': round(session_time, 1)
        }

# Initialize the service
study_buddy = StudyBuddyService()

# Flask Routes
@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/query', methods=['POST'])
def handle_query():
    """Handle study queries"""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({'error': 'Query cannot be empty'}), 400
        
        # Get or create user session
        user_id = session.get('user_id', f"user_{int(time.time())}")
        session['user_id'] = user_id
        
        # Process the query
        result = study_buddy.process_study_query(user_id, query)
        
        return jsonify({
            'success': True,
            'data': result
        })
        
    except Exception as e:
        logger.error(f"Error handling query: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/stats')
def get_stats():
    """Get user session statistics"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'queries': 0, 'total_cost': 0.0, 'session_time': 0})
    
    stats = study_buddy.get_user_stats(user_id)
    return jsonify(stats)

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting Smart Study Buddy Assistant on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug) 