#!/usr/bin/env python3
"""
NVIDIA LLM Router Core Implementation
Based on the official NVIDIA LLM Router: https://github.com/NVIDIA-AI-Blueprints/llm-router

This implementation follows the exact same logic as the official Rust implementation:
1. Extract nim-llm-router parameters from request
2. Select policy (task_router or complexity_router)
3. Use Triton inference server for classification
4. Route to appropriate model based on classification
5. Proxy request to selected model with OpenAI-compatible API
"""

import os
import json
import time
import logging
import requests
import asyncio
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import yaml

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

logger = logging.getLogger(__name__)

class RoutingStrategy(Enum):
    MANUAL = "manual"
    TRITON = "triton"

@dataclass
class NimLlmRouterParams:
    """Parameters extracted from nim-llm-router field in request"""
    policy: str
    routing_strategy: Optional[RoutingStrategy] = None
    model: Optional[str] = None
    threshold: Optional[float] = None

@dataclass
class Llm:
    """LLM configuration from policy"""
    name: str
    api_base: str
    api_key: str
    model: str

@dataclass
class Policy:
    """Routing policy configuration"""
    name: str
    url: str  # Triton inference server URL for classification
    llms: List[Llm]
    
    def get_llm_by_name(self, name: str) -> Optional[Llm]:
        """Get LLM by name"""
        for llm in self.llms:
            if llm.name.strip() == name.strip():
                return llm
        return None
    
    def get_llm_by_index(self, index: int) -> Optional[Llm]:
        """Get LLM by index"""
        if 0 <= index < len(self.llms):
            return self.llms[index]
        return None
    
    def get_llm_name_by_index(self, index: int) -> Optional[str]:
        """Get LLM name by index"""
        llm = self.get_llm_by_index(index)
        return llm.name if llm else None

@dataclass
class RouterConfig:
    """Router configuration matching official NVIDIA LLM Router"""
    policies: List[Policy]
    
    @classmethod
    def load_config(cls, config_path: str) -> 'RouterConfig':
        """Load configuration from YAML file with environment variable substitution"""
        with open(config_path, 'r') as f:
            content = f.read()
        
        # Replace environment variables
        nvidia_api_key = os.getenv('NVIDIA_API_KEY', '')
        content = content.replace('${NVIDIA_API_KEY}', nvidia_api_key)
        
        config_data = yaml.safe_load(content)
        
        policies = []
        for policy_data in config_data['policies']:
            llms = []
            for llm_data in policy_data['llms']:
                llms.append(Llm(
                    name=llm_data['name'],
                    api_base=llm_data['api_base'],
                    api_key=llm_data['api_key'],
                    model=llm_data['model']
                ))
            
            policies.append(Policy(
                name=policy_data['name'],
                url=policy_data['url'],
                llms=llms
            ))
        
        return cls(policies=policies)
    
    def get_policy_by_name(self, name: str) -> Optional[Policy]:
        """Get policy by name"""
        for policy in self.policies:
            if policy.name.strip() == name.strip():
                return policy
        return None

@dataclass
class InferInputTensor:
    """Triton inference input tensor"""
    name: str
    datatype: str
    shape: List[int]
    data: List[List[str]]

@dataclass
class InferInputs:
    """Triton inference inputs"""
    inputs: List[InferInputTensor]

@dataclass
class TritonOutput:
    """Triton inference output"""
    data: List[float]

@dataclass
class TritonResponse:
    """Triton inference response"""
    outputs: List[TritonOutput]

class NVIDIALLMRouterCore:
    """
    Core NVIDIA LLM Router implementation following the official logic exactly.
    
    This implementation replicates the Rust proxy.rs logic in Python:
    1. Extract nim-llm-router parameters
    2. Select routing strategy (manual vs triton)
    3. For triton: call classification server and get model index
    4. For manual: use specified model directly
    5. Route request to selected model
    """
    
    def __init__(self, config: RouterConfig):
        self.config = config
        self.client = requests.Session()
    
    def extract_nim_llm_router_params(self, request_body: Dict[str, Any]) -> Optional[NimLlmRouterParams]:
        """Extract nim-llm-router parameters from request body"""
        nim_params = request_body.get('nim-llm-router')
        if not nim_params:
            return None
        
        policy = nim_params.get('policy')
        if not policy:
            return None
        
        routing_strategy = None
        if 'routing_strategy' in nim_params:
            strategy_str = nim_params['routing_strategy']
            if strategy_str == 'manual':
                routing_strategy = RoutingStrategy.MANUAL
            elif strategy_str == 'triton':
                routing_strategy = RoutingStrategy.TRITON
        
        return NimLlmRouterParams(
            policy=policy,
            routing_strategy=routing_strategy,
            model=nim_params.get('model'),
            threshold=nim_params.get('threshold', 0.5)
        )
    
    def remove_nim_llm_router_params(self, request_body: Dict[str, Any]) -> Dict[str, Any]:
        """Remove nim-llm-router parameters from request body"""
        cleaned_body = request_body.copy()
        if 'nim-llm-router' in cleaned_body:
            del cleaned_body['nim-llm-router']
        return cleaned_body
    
    def extract_messages(self, request_body: Dict[str, Any]) -> List[Dict[str, str]]:
        """Extract messages from request body"""
        return request_body.get('messages', [])
    
    def convert_messages_to_text_input(self, messages: List[Dict[str, str]]) -> str:
        """Convert messages to text input for classification"""
        text_input = json.dumps(messages)
        # Shorten to max 2000 characters (matching official implementation)
        if len(text_input) > 2000:
            text_input = text_input[-2000:]
        return text_input
    
    def get_last_message_for_triton(self, messages: List[Dict[str, str]]) -> str:
        """Get last message content for Triton classification"""
        if messages:
            return messages[-1].get('content', '')
        return ''
    
    async def choose_model_with_triton(self, policy: Policy, text_input: str, threshold: float = 0.5) -> int:
        """Choose model using Triton inference server classification"""
        logger.info(f"Using policy: {policy.name}")
        logger.info(f"Triton input text: {text_input}")
        
        # Create Triton inference request in proper JSON format
        triton_request = {
            "inputs": [
                {
                    "name": "INPUT",
                    "datatype": "BYTES",
                    "shape": [1, 1],
                    "data": [[text_input]]
                }
            ]
        }
        
        # Make request to Triton server
        headers = {'Content-Type': 'application/json'}
        
        response = self.client.post(
            policy.url,
            headers=headers,
            json=triton_request,
            timeout=30
        )
        
        logger.info(f"Triton classification response status: {response.status_code}")
        
        if not response.ok:
            error_msg = f"Triton service error: {response.status_code} - {response.text}"
            logger.error(error_msg)
            raise Exception(error_msg)
        
        # Parse Triton response
        triton_response = response.json()
        logger.info(f"Triton Output: {triton_response}")
        
        if 'outputs' not in triton_response or not triton_response['outputs']:
            raise Exception("No outputs returned from Triton response")
        
        output_tensor = triton_response['outputs'][0]
        probabilities = output_tensor['data']
        
        # Find model with highest probability
        model_index = probabilities.index(max(probabilities))
        
        logger.info(f"Model index chosen by Triton classifier: {model_index}")
        return model_index
    
    def choose_model_manual(self, policy: Policy, model_name: str) -> int:
        """Choose model manually by name"""
        for i, llm in enumerate(policy.llms):
            if llm.name == model_name:
                return i
        raise Exception(f"Model not found: {model_name}")
    
    def modify_model_in_request(self, request_body: Dict[str, Any], model: str) -> Dict[str, Any]:
        """Modify the model field in request body"""
        modified_body = request_body.copy()
        modified_body['model'] = model
        return modified_body
    
    async def route_request(self, request_body: Dict[str, Any]) -> Tuple[Dict[str, Any], str, str]:
        """
        Route request using NVIDIA LLM Router logic.
        
        Returns:
            Tuple of (response_data, chosen_model, chosen_classifier)
        """
        # Step 1: Extract nim-llm-router parameters
        nim_params = self.extract_nim_llm_router_params(request_body)
        if not nim_params:
            raise Exception(
                "Missing required 'nim-llm-router' parameters in request body. "
                "Expected format: { 'nim-llm-router': { 'policy': 'string', "
                "'routing_strategy': 'manual|triton', 'model': 'string' (for manual strategy) } }"
            )
        
        # Step 2: Get policy
        policy = self.config.get_policy_by_name(nim_params.policy)
        if not policy:
            raise Exception(f"Policy not found: {nim_params.policy}")
        
        # Step 3: Extract messages and prepare text input
        messages = self.extract_messages(request_body)
        text_input = self.convert_messages_to_text_input(messages)
        
        # Step 4: Choose model based on routing strategy
        if nim_params.routing_strategy == RoutingStrategy.MANUAL:
            if not nim_params.model:
                raise Exception("No model specified for manual routing")
            model_index = self.choose_model_manual(policy, nim_params.model)
        elif nim_params.routing_strategy == RoutingStrategy.TRITON:
            triton_text = self.get_last_message_for_triton(messages)
            model_index = await self.choose_model_with_triton(policy, triton_text, nim_params.threshold)
        else:
            raise Exception("No routing strategy specified")
        
        # Step 5: Get chosen LLM
        chosen_llm = policy.get_llm_by_index(model_index)
        if not chosen_llm:
            raise Exception(f"LLM not found at index {model_index}")
        
        chosen_classifier = policy.get_llm_name_by_index(model_index)
        
        logger.info(f"Chosen Classifier: {chosen_classifier}")
        logger.info(f"Chosen Model: {chosen_llm.model}")
        
        # Step 6: Prepare request for downstream LLM
        cleaned_body = self.remove_nim_llm_router_params(request_body)
        final_body = self.modify_model_in_request(cleaned_body, chosen_llm.model)
        
        # Step 7: Make request to chosen LLM
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {chosen_llm.api_key}',
            'Content-Type': 'application/json'
        }
        
        # Construct full URL
        url = f"{chosen_llm.api_base}/v1/chat/completions"
        
        response = self.client.post(
            url,
            headers=headers,
            json=final_body,
            timeout=60
        )
        
        if not response.ok:
            error_msg = f"LLM service error: {response.status_code} - {response.text}"
            logger.error(error_msg)
            raise Exception(error_msg)
        
        response_data = response.json()
        return response_data, chosen_llm.model, chosen_classifier

class NVIDIARouterService:
    """
    Service wrapper that provides educational enhancements on top of the core NVIDIA LLM Router.
    This maintains the exact official routing logic while adding educational context.
    """
    
    def __init__(self, config_path: str = None):
        # Load official NVIDIA LLM Router configuration
        if config_path:
            self.config = RouterConfig.load_config(config_path)
        else:
            # Use embedded configuration matching official defaults
            self.config = self._create_default_config()
        
        self.router_core = NVIDIALLMRouterCore(self.config)
        
        # Educational enhancements (kept separate from core routing logic)
        self.subject_patterns = {
            'Mathematics': ['math', 'algebra', 'calculus', 'geometry', 'statistics'],
            'Science': ['science', 'physics', 'chemistry', 'biology', 'experiment'],
            'Computer Science': ['programming', 'code', 'algorithm', 'function', 'python'],
            'History': ['history', 'war', 'revolution', 'ancient', 'historical'],
            'Literature': ['literature', 'novel', 'poem', 'poetry', 'author']
        }
    
    def _create_default_config(self) -> RouterConfig:
        """Create default configuration matching official NVIDIA LLM Router"""
        # This matches the exact configuration from the official config.yaml
        task_router_llms = [
            Llm("Brainstorming", "https://integrate.api.nvidia.com", os.getenv('NVIDIA_API_KEY', ''), "meta/llama-3.1-70b-instruct"),
            Llm("Chatbot", "https://integrate.api.nvidia.com", os.getenv('NVIDIA_API_KEY', ''), "mistralai/mixtral-8x22b-instruct-v0.1"),
            Llm("Classification", "https://integrate.api.nvidia.com", os.getenv('NVIDIA_API_KEY', ''), "meta/llama-3.1-8b-instruct"),
            Llm("Closed QA", "https://integrate.api.nvidia.com", os.getenv('NVIDIA_API_KEY', ''), "meta/llama-3.1-70b-instruct"),
            Llm("Code Generation", "https://integrate.api.nvidia.com", os.getenv('NVIDIA_API_KEY', ''), "nvidia/llama-3.3-nemotron-super-49b-v1"),
            Llm("Extraction", "https://integrate.api.nvidia.com", os.getenv('NVIDIA_API_KEY', ''), "meta/llama-3.1-8b-instruct"),
            Llm("Open QA", "https://integrate.api.nvidia.com", os.getenv('NVIDIA_API_KEY', ''), "meta/llama-3.1-70b-instruct"),
            Llm("Other", "https://integrate.api.nvidia.com", os.getenv('NVIDIA_API_KEY', ''), "mistralai/mixtral-8x22b-instruct-v0.1"),
            Llm("Rewrite", "https://integrate.api.nvidia.com", os.getenv('NVIDIA_API_KEY', ''), "meta/llama-3.1-8b-instruct"),
            Llm("Summarization", "https://integrate.api.nvidia.com", os.getenv('NVIDIA_API_KEY', ''), "meta/llama-3.1-70b-instruct"),
            Llm("Text Generation", "https://integrate.api.nvidia.com", os.getenv('NVIDIA_API_KEY', ''), "mistralai/mixtral-8x22b-instruct-v0.1"),
            Llm("Unknown", "https://integrate.api.nvidia.com", os.getenv('NVIDIA_API_KEY', ''), "meta/llama-3.1-8b-instruct"),
        ]
        
        complexity_router_llms = [
            Llm("Creativity", "https://integrate.api.nvidia.com", os.getenv('NVIDIA_API_KEY', ''), "meta/llama-3.1-70b-instruct"),
            Llm("Reasoning", "https://integrate.api.nvidia.com", os.getenv('NVIDIA_API_KEY', ''), "nvidia/llama-3.3-nemotron-super-49b-v1"),
            Llm("Contextual-Knowledge", "https://integrate.api.nvidia.com", os.getenv('NVIDIA_API_KEY', ''), "meta/llama-3.1-8b-instruct"),
            Llm("Few-Shot", "https://integrate.api.nvidia.com", os.getenv('NVIDIA_API_KEY', ''), "meta/llama-3.1-70b-instruct"),
            Llm("Domain-Knowledge", "https://integrate.api.nvidia.com", os.getenv('NVIDIA_API_KEY', ''), "mistralai/mixtral-8x22b-instruct-v0.1"),
            Llm("No-Label-Reason", "https://integrate.api.nvidia.com", os.getenv('NVIDIA_API_KEY', ''), "meta/llama-3.1-8b-instruct"),
            Llm("Constraint", "https://integrate.api.nvidia.com", os.getenv('NVIDIA_API_KEY', ''), "meta/llama-3.1-8b-instruct"),
        ]
        
        policies = [
            Policy("task_router", "http://router-server:8000/v2/models/task_router_ensemble/infer", task_router_llms),
            Policy("complexity_router", "http://router-server:8000/v2/models/complexity_router_ensemble/infer", complexity_router_llms)
        ]
        
        return RouterConfig(policies=policies)
    
    def detect_subject(self, query: str) -> str:
        """Detect subject for educational context"""
        query_lower = query.lower()
        subject_scores = {}
        
        for subject, patterns in self.subject_patterns.items():
            score = sum(1 for pattern in patterns if pattern in query_lower)
            if score > 0:
                subject_scores[subject] = score
        
        return max(subject_scores.items(), key=lambda x: x[1])[0] if subject_scores else 'General'
    
    def detect_difficulty(self, query: str) -> str:
        """Detect difficulty level for educational context"""
        query_lower = query.lower()
        word_count = len(query.split())
        
        if any(term in query_lower for term in ['simple', 'basic', 'what is']):
            return 'Elementary'
        elif any(term in query_lower for term in ['explain', 'how does']):
            return 'Middle School'
        elif any(term in query_lower for term in ['analyze', 'compare', 'evaluate']):
            return 'College'
        elif word_count > 20:
            return 'Graduate'
        else:
            return 'High School'
    
    async def process_educational_query(self, query: str, policy: str = "task_router", routing_strategy: str = "triton") -> Dict[str, Any]:
        """
        Process educational query using official NVIDIA LLM Router logic.
        
        Args:
            query: The educational question
            policy: Either "task_router" or "complexity_router"
            routing_strategy: Either "triton" or "manual"
        
        Returns:
            Dictionary with response and metadata
        """
        start_time = time.time()
        
        # Detect educational context
        subject = self.detect_subject(query)
        difficulty = self.detect_difficulty(query)
        
        # Prepare request in official NVIDIA LLM Router format
        request_body = {
            "model": "",  # Will be filled by router
            "messages": [
                {
                    "role": "user",
                    "content": f"You are a helpful study buddy assistant. The student is asking about {subject} at a {difficulty} level.\n\nStudent's question: {query}\n\nPlease provide a clear, educational response with step-by-step explanations appropriate for the {difficulty} level."
                }
            ],
            "max_tokens": 1024,
            "temperature": 0.7,
            "nim-llm-router": {
                "policy": policy,
                "routing_strategy": routing_strategy
            }
        }
        
        try:
            # Use official NVIDIA LLM Router core logic
            response_data, chosen_model, chosen_classifier = await self.router_core.route_request(request_body)
            
            response_time = time.time() - start_time
            
            return {
                'response': response_data['choices'][0]['message']['content'],
                'model_used': chosen_model,
                'classifier_used': chosen_classifier,
                'policy_used': policy,
                'routing_strategy': routing_strategy,
                'response_time': response_time,
                'detected_subject': subject,
                'detected_difficulty': difficulty,
                'usage': response_data.get('usage', {}),
                'raw_response': response_data
            }
            
        except Exception as e:
            logger.error(f"Error in NVIDIA LLM Router: {e}")
            return {
                'error': str(e),
                'response': f"I apologize, but I encountered an error processing your {subject} question. Please try again.",
                'model_used': 'error',
                'response_time': time.time() - start_time,
                'detected_subject': subject,
                'detected_difficulty': difficulty
            } 