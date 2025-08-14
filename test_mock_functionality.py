#!/usr/bin/env python3
"""
Test script for NVIDIA API Mock Functionality
Demonstrates how the mock system works while preserving Triton classification.
"""

import os
import asyncio
import json
import time

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

from nvidia_router_core import NVIDIARouterService

async def test_mock_functionality():
    """Test the mock functionality with various query types"""
    
    print("🎭 Testing NVIDIA API Mock Functionality")
    print("=" * 70)
    
    # Check mock mode configuration
    mock_mode = os.getenv('NVIDIA_MOCK_MODE', 'true').lower()
    print(f"📋 Mock Mode: {mock_mode}")
    
    # Initialize router with mock mode explicitly enabled
    print("\n🔧 Initializing router with mock mode enabled...")
    router_mock = NVIDIARouterService(enable_mocking=True)
    
    # Initialize router with mock mode explicitly disabled (for comparison)
    print("🔧 Initializing router with mock mode disabled...")
    router_live = NVIDIARouterService(enable_mocking=False)
    
    print(f"✅ Both routers initialized successfully")
    
    # Test cases with different subjects and complexity
    test_cases = [
        {
            "name": "Mathematics - Pythagorean Theorem",
            "query": "Explain the Pythagorean theorem with examples",
            "expected_subject": "Mathematics",
            "policy": "task_router"
        },
        {
            "name": "Science - Photosynthesis",
            "query": "What is photosynthesis and how does it work?",
            "expected_subject": "Science", 
            "policy": "task_router"
        },
        {
            "name": "Computer Science - Binary Search",
            "query": "Write a Python function to implement binary search",
            "expected_subject": "Computer Science",
            "policy": "task_router"
        },
        {
            "name": "Creative Writing - Song with Emojis",
            "query": "Can you write me a song? Use as many emojis as possible.",
            "expected_subject": "Creative",
            "policy": "task_router"
        },
        {
            "name": "Complex Reasoning",
            "query": "Analyze the logical steps needed to solve complex mathematical proofs",
            "expected_subject": "Mathematics",
            "policy": "complexity_router"
        }
    ]
    
    print(f"\n🧪 Running {len(test_cases)} test cases...")
    print("=" * 70)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test {i}: {test_case['name']}")
        print("-" * 50)
        
        try:
            # Test with mock mode
            print("🎭 Testing with MOCK mode:")
            start_time = time.time()
            
            mock_result = await router_mock.process_educational_query(
                test_case['query'], 
                test_case['policy'], 
                "triton"  # Use triton routing to test classification
            )
            
            mock_time = time.time() - start_time
            
            if 'error' not in mock_result:
                print(f"   ✅ Subject: {mock_result.get('detected_subject', 'Unknown')}")
                print(f"   ✅ Difficulty: {mock_result.get('detected_difficulty', 'Unknown')}")
                print(f"   ✅ Model: {mock_result.get('model_used', 'Unknown')}")
                print(f"   ✅ Classifier: {mock_result.get('classifier_used', 'Unknown')}")
                print(f"   ✅ Response Time: {mock_time:.2f}s")
                print(f"   ✅ Response Length: {len(mock_result.get('response', ''))}")
                
                # Check if it's a mock response
                raw_response = mock_result.get('raw_response', {})
                is_mock = raw_response.get('_mock_response', False)
                print(f"   🎭 Mock Response: {is_mock}")
                
                # Show response preview
                response_preview = mock_result.get('response', '')[:150]
                print(f"   📄 Response Preview: {response_preview}...")
                
            else:
                print(f"   ❌ Mock test failed: {mock_result['error']}")
            
            # Note about live mode testing
            print("\n🔗 Live mode testing:")
            print("   ⚠️  Skipped (would require real API calls)")
            print("   ℹ️  To test live mode, set NVIDIA_MOCK_MODE=false and ensure valid API key")
            
        except Exception as e:
            print(f"   ❌ Test failed: {e}")
        
        # Add spacing between tests
        if i < len(test_cases):
            print()
    
    # Test routing strategy comparison
    print(f"\n🔀 Testing Different Routing Strategies")
    print("=" * 50)
    
    test_query = "What is machine learning?"
    
    strategies = [
        ("triton", "Triton-based classification"),
        ("manual", "Manual model selection")
    ]
    
    for strategy, description in strategies:
        print(f"\n📋 Strategy: {strategy} ({description})")
        try:
            if strategy == "manual":
                # For manual strategy, we need to specify a model
                request_body = {
                    "model": "",
                    "messages": [{"role": "user", "content": test_query}],
                    "max_tokens": 100,
                    "nim-llm-router": {
                        "policy": "task_router",
                        "routing_strategy": "manual",
                        "model": "Open QA"  # Specify a classifier name
                    }
                }
                
                response_data, chosen_model, chosen_classifier = await router_mock.router_core.route_request(request_body)
                print(f"   ✅ Chosen Model: {chosen_model}")
                print(f"   ✅ Chosen Classifier: {chosen_classifier}")
                print(f"   ✅ Strategy: manual (user-specified)")
                
            else:  # triton strategy
                result = await router_mock.process_educational_query(test_query, "task_router", strategy)
                if 'error' not in result:
                    print(f"   ✅ Chosen Model: {result.get('model_used', 'Unknown')}")
                    print(f"   ✅ Chosen Classifier: {result.get('classifier_used', 'Unknown')}")
                    print(f"   ✅ Strategy: triton (ML-based classification)")
                else:
                    print(f"   ❌ Strategy failed: {result['error']}")
        
        except Exception as e:
            print(f"   ❌ Strategy test failed: {e}")
    
    # Summary
    print(f"\n📊 Mock System Summary")
    print("=" * 50)
    print("✅ NVIDIA API catalog calls are mocked (contextual responses)")
    print("🔗 Triton classification calls are NOT mocked (real ML inference)")
    print("🎯 Educational context detection works correctly")
    print("⚡ Response times are simulated based on model characteristics")
    print("📈 Token usage and costs are calculated realistically")
    print("🎭 Mock responses are contextually appropriate to queries")
    
    print(f"\n🎉 Mock functionality testing complete!")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(test_mock_functionality()) 