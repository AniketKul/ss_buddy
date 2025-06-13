#!/usr/bin/env python3
"""
Test script for the official NVIDIA LLM Router implementation
This script tests the exact same API format as the official NVIDIA LLM Router
"""

import os
import asyncio
import json

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

from nvidia_router_core import NVIDIARouterService

async def test_nvidia_router():
    """Test the NVIDIA LLM Router with various scenarios"""
    
    print("🧪 Testing Official NVIDIA LLM Router Implementation")
    print("=" * 60)
    
    # Check API key
    if not os.getenv('NVIDIA_API_KEY'):
        print("❌ NVIDIA_API_KEY not set. Please set your API key:")
        print("export NVIDIA_API_KEY='your-api-key-here'")
        return
    
    # Initialize router
    try:
        if os.path.exists('nvidia_router_config.yaml'):
            router = NVIDIARouterService('nvidia_router_config.yaml')
            print("✅ Loaded router with configuration file")
        else:
            router = NVIDIARouterService()
            print("✅ Loaded router with default configuration")
    except Exception as e:
        print(f"❌ Failed to initialize router: {e}")
        return
    
    # Test cases matching official NVIDIA LLM Router format
    test_cases = [
        {
            "name": "Task Router - Triton Strategy",
            "request": {
                "model": "",
                "messages": [
                    {
                        "role": "user",
                        "content": "Can you write me a song? Use as many emojis as possible."
                    }
                ],
                "max_tokens": 64,
                "stream": False,
                "nim-llm-router": {
                    "policy": "task_router",
                    "routing_strategy": "triton"
                }
            }
        },
        {
            "name": "Complexity Router - Triton Strategy",
            "request": {
                "model": "",
                "messages": [
                    {
                        "role": "user",
                        "content": "Analyze the logical steps needed to solve complex mathematical proofs."
                    }
                ],
                "max_tokens": 64,
                "stream": False,
                "nim-llm-router": {
                    "policy": "complexity_router",
                    "routing_strategy": "triton"
                }
            }
        },
        {
            "name": "Task Router - Manual Strategy",
            "request": {
                "model": "",
                "messages": [
                    {
                        "role": "user",
                        "content": "Write a Python function to implement binary search."
                    }
                ],
                "max_tokens": 64,
                "stream": False,
                "nim-llm-router": {
                    "policy": "task_router",
                    "routing_strategy": "manual",
                    "model": "Code Generation"
                }
            }
        }
    ]
    
    # Run tests
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🔍 Test {i}: {test_case['name']}")
        print("-" * 40)
        
        try:
            # Test using the router core directly (official API format)
            response_data, chosen_model, chosen_classifier = await router.router_core.route_request(test_case['request'])
            
            print(f"✅ Success!")
            print(f"   Chosen Classifier: {chosen_classifier}")
            print(f"   Chosen Model: {chosen_model}")
            print(f"   Policy: {test_case['request']['nim-llm-router']['policy']}")
            print(f"   Strategy: {test_case['request']['nim-llm-router']['routing_strategy']}")
            print(f"   Response Preview: {response_data['choices'][0]['message']['content'][:100]}...")
            
            if 'usage' in response_data:
                usage = response_data['usage']
                print(f"   Token Usage: {usage.get('prompt_tokens', 0)} prompt + {usage.get('completion_tokens', 0)} completion = {usage.get('total_tokens', 0)} total")
            
        except Exception as e:
            print(f"❌ Failed: {e}")
    
    # Test educational query processing
    print(f"\n🎓 Testing Educational Query Processing")
    print("-" * 40)
    
    educational_queries = [
        "What is photosynthesis and how does it work?",
        "Explain the Pythagorean theorem with examples",
        "Write a Python function to sort a list"
    ]
    
    for query in educational_queries:
        try:
            result = await router.process_educational_query(query, "task_router", "triton")
            
            if 'error' not in result:
                print(f"✅ Query: {query[:50]}...")
                print(f"   Subject: {result.get('detected_subject', 'Unknown')}")
                print(f"   Difficulty: {result.get('detected_difficulty', 'Unknown')}")
                print(f"   Model: {result.get('model_used', 'Unknown')}")
                print(f"   Classifier: {result.get('classifier_used', 'Unknown')}")
                print(f"   Response Time: {result.get('response_time', 0):.2f}s")
            else:
                print(f"❌ Query failed: {result['error']}")
                
        except Exception as e:
            print(f"❌ Educational query failed: {e}")
    
    print(f"\n🏁 Testing Complete!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_nvidia_router()) 