#!/usr/bin/env python3
"""
NVIDIA API Catalog Mock System
Provides realistic mock responses for NVIDIA API catalog calls while preserving Triton classification functionality.
"""

import json
import time
import random
import uuid
from typing import Dict, Any, List
from datetime import datetime


class NVIDIAAPIMock:
    """
    Mock system for NVIDIA API catalog responses.
    Generates contextually appropriate responses based on model type and query content.
    """
    
    def __init__(self):
        self.response_templates = self._initialize_response_templates()
        self.model_characteristics = self._initialize_model_characteristics()
    
    def _initialize_model_characteristics(self) -> Dict[str, Dict[str, Any]]:
        """Define characteristics for different NVIDIA models"""
        return {
            "meta/llama-3.1-8b-instruct": {
                "style": "concise",
                "strength": "quick_responses",
                "cost_per_1k_tokens": 0.0002,
                "avg_response_length": 150,
                "response_time_range": (0.5, 1.5)
            },
            "meta/llama-3.1-70b-instruct": {
                "style": "detailed",
                "strength": "complex_reasoning",
                "cost_per_1k_tokens": 0.0006,
                "avg_response_length": 400,
                "response_time_range": (1.0, 3.0)
            },
            "nvidia/llama-3.3-nemotron-super-49b-v1": {
                "style": "technical",
                "strength": "code_and_reasoning",
                "cost_per_1k_tokens": 0.002,
                "avg_response_length": 350,
                "response_time_range": (1.5, 4.0)
            },
            "mistralai/mixtral-8x22b-instruct-v0.1": {
                "style": "creative",
                "strength": "creative_writing",
                "cost_per_1k_tokens": 0.0012,
                "avg_response_length": 300,
                "response_time_range": (1.0, 2.5)
            }
        }
    
    def _initialize_response_templates(self) -> Dict[str, Dict[str, List[str]]]:
        """Initialize response templates for different query types and subjects"""
        return {
            "mathematics": {
                "simple": [
                    "Let me explain this step by step:\n\n{explanation}\n\nThe answer is {answer}.",
                    "Here's how to solve this:\n\n{explanation}\n\nTherefore, {answer}.",
                    "To understand this concept:\n\n{explanation}\n\nSo the result is {answer}."
                ],
                "detailed": [
                    "This is an excellent mathematical question! Let me break it down comprehensively:\n\n{explanation}\n\n**Key Steps:**\n1. {step1}\n2. {step2}\n3. {step3}\n\n**Final Answer:** {answer}\n\n**Why this works:** {reasoning}",
                    "Let's explore this mathematical concept thoroughly:\n\n{explanation}\n\n**Method:**\n{method}\n\n**Solution:**\n{solution}\n\n**Verification:** {verification}"
                ]
            },
            "science": {
                "simple": [
                    "{concept} is {definition}. Here's how it works: {explanation}",
                    "Let me explain {concept}: {definition}\n\nThe process involves: {explanation}",
                    "{concept} refers to {definition}. The key points are: {explanation}"
                ],
                "detailed": [
                    "Great science question! Let me provide a comprehensive explanation:\n\n**What is {concept}?**\n{definition}\n\n**How it works:**\n{explanation}\n\n**Real-world examples:**\n{examples}\n\n**Why it matters:**\n{significance}",
                    "This is a fascinating topic in science! Here's a detailed breakdown:\n\n**Overview:** {definition}\n\n**The Process:**\n{explanation}\n\n**Key Factors:**\n{factors}\n\n**Applications:**\n{applications}"
                ]
            },
            "computer_science": {
                "code": [
                    "Here's a {language} solution for your request:\n\n```{language}\n{code}\n```\n\n**Explanation:**\n{explanation}\n\n**Time Complexity:** {complexity}\n**How it works:** {description}",
                    "I'll help you with this {language} implementation:\n\n```{language}\n{code}\n```\n\n**Key Features:**\n- {feature1}\n- {feature2}\n- {feature3}\n\n**Usage Example:**\n```{language}\n{usage}\n```"
                ],
                "concept": [
                    "{concept} is a fundamental concept in computer science. Here's what you need to know:\n\n**Definition:** {definition}\n\n**How it works:** {explanation}\n\n**Common use cases:** {examples}",
                    "Let me explain {concept}:\n\n**Core Idea:** {definition}\n\n**Implementation:** {explanation}\n\n**Benefits:** {benefits}\n\n**Example:** {example}"
                ]
            },
            "creative": {
                "writing": [
                    "Here's a creative piece for you:\n\n{content}\n\n**Style notes:** {style_notes}",
                    "I'd love to help with this creative request! Here's what I came up with:\n\n{content}\n\n**Creative elements used:** {elements}",
                    "Let me craft something creative for you:\n\n{content}\n\n**Why this approach:** {reasoning}"
                ],
                "brainstorming": [
                    "Here are some creative ideas for your request:\n\n**Option 1:** {idea1}\n**Option 2:** {idea2}\n**Option 3:** {idea3}\n\n**My recommendation:** {recommendation}",
                    "I've brainstormed several approaches:\n\n{ideas}\n\n**Most promising direction:** {best_option}\n\n**Next steps:** {next_steps}"
                ]
            },
            "general": {
                "explanation": [
                    "I'd be happy to explain this! {explanation}\n\nKey points to remember:\n- {point1}\n- {point2}\n- {point3}",
                    "Great question! Let me break this down: {explanation}\n\nThis is important because: {significance}",
                    "Here's what you need to know: {explanation}\n\nTo summarize: {summary}"
                ],
                "analysis": [
                    "Let me analyze this for you:\n\n**Overview:** {overview}\n\n**Key aspects:**\n{analysis}\n\n**Conclusion:** {conclusion}",
                    "This is an interesting topic to analyze:\n\n{analysis}\n\n**Important considerations:** {considerations}\n\n**Final thoughts:** {conclusion}"
                ]
            }
        }
    
    def _detect_query_type(self, content: str) -> tuple[str, str]:
        """Detect the subject and query type from message content"""
        content_lower = content.lower()
        
        # Subject detection
        if any(word in content_lower for word in ['math', 'equation', 'calculate', 'solve', 'theorem', 'integral', 'derivative']):
            subject = "mathematics"
        elif any(word in content_lower for word in ['science', 'chemistry', 'physics', 'biology', 'photosynthesis', 'experiment']):
            subject = "science"
        elif any(word in content_lower for word in ['code', 'programming', 'python', 'function', 'algorithm', 'implement']):
            subject = "computer_science"
        elif any(word in content_lower for word in ['write', 'song', 'story', 'creative', 'poem', 'emoji']):
            subject = "creative"
        else:
            subject = "general"
        
        # Query type detection
        if 'write' in content_lower and any(word in content_lower for word in ['code', 'function', 'program']):
            query_type = "code"
        elif any(word in content_lower for word in ['write', 'song', 'story', 'creative']):
            query_type = "writing"
        elif any(word in content_lower for word in ['brainstorm', 'ideas', 'suggest']):
            query_type = "brainstorming"
        elif any(word in content_lower for word in ['analyze', 'analysis', 'compare']):
            query_type = "analysis"
        elif any(word in content_lower for word in ['explain', 'what is', 'how does']):
            query_type = "explanation" if subject == "general" else "concept"
        elif subject == "mathematics":
            query_type = "simple" if len(content.split()) < 15 else "detailed"
        elif subject == "science":
            query_type = "simple" if len(content.split()) < 15 else "detailed"
        else:
            query_type = "explanation"
        
        return subject, query_type
    
    def _generate_response_content(self, subject: str, query_type: str, content: str, model: str) -> str:
        """Generate contextually appropriate response content"""
        model_char = self.model_characteristics.get(model, self.model_characteristics["meta/llama-3.1-8b-instruct"])
        
        # Generate response based on subject and query type
        if subject == "mathematics":
            if "pythagorean" in content.lower():
                response = """This is an excellent mathematical question! Let me break it down comprehensively:

The Pythagorean theorem states that in a right triangle, the square of the hypotenuse equals the sum of squares of the other two sides.

**Key Steps:**
1. Identify the right triangle
2. Label the sides (a, b = legs, c = hypotenuse)
3. Apply the formula a² + b² = c²

**Final Answer:** a² + b² = c²

**Why this works:** This relationship holds because of the geometric properties of right triangles."""
            
            elif "integral" in content.lower():
                response = """Let's explore this mathematical concept thoroughly:

Integration is the reverse process of differentiation, used to find areas under curves.

**Method:**
Using the fundamental theorem of calculus

**Solution:**
For ∫x² from 0 to 5: [x³/3] from 0 to 5 = 125/3 - 0 = 125/3

**Verification:** We can check by differentiating x³/3 to get x²."""
            
            else:
                response = """Let me explain this step by step:

Mathematical problems require systematic approaches and logical reasoning.

The answer follows from applying the relevant mathematical principles systematically."""
        
        elif subject == "science":
            if "photosynthesis" in content.lower():
                response = """Great science question! Let me provide a comprehensive explanation:

**What is photosynthesis?**
The process by which plants convert light energy into chemical energy

**How it works:**
Plants use chlorophyll to capture sunlight, carbon dioxide from air, and water from roots to produce glucose and oxygen. The equation is: 6CO₂ + 6H₂O + light energy → C₆H₁₂O₆ + 6O₂

**Real-world examples:**
All green plants, algae, and some bacteria perform photosynthesis

**Why it matters:**
It's the foundation of most food chains and produces the oxygen we breathe"""
            
            else:
                response = """This is a fascinating topic in science! Here's a detailed breakdown:

**Overview:** A fundamental law or process in nature

**The Process:**
Science helps us understand how the natural world works through observation and experimentation

**Key Factors:**
Multiple variables often influence scientific phenomena

**Applications:**
Scientific principles are applied in medicine, technology, and environmental protection"""
        
        elif subject == "computer_science":
            if query_type == "code":
                if "binary search" in content.lower():
                    response = """Here's a python solution for your request:

```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1
```

**Explanation:**
This function efficiently searches a sorted array by repeatedly dividing the search space in half

**Time Complexity:** O(log n)
**How it works:** We compare the target with the middle element and eliminate half the array each time"""
                
                elif "sort" in content.lower():
                    response = """I'll help you with this python implementation:

```python
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quick_sort(left) + middle + quick_sort(right)
```

**Key Features:**
- Efficient divide-and-conquer algorithm
- In-place sorting possible with modifications
- Good average-case performance

**Usage Example:**
```python
numbers = [3, 6, 8, 10, 1, 2, 1]
sorted_numbers = quick_sort(numbers)
print(sorted_numbers)  # Output: [1, 1, 2, 3, 6, 8, 10]
```"""
                
                else:
                    response = """Here's a python solution for your request:

```python
def example_function(param1, param2):
    \"\"\"
    Example function demonstrating good practices
    \"\"\"
    result = param1 + param2
    return result
```

**Explanation:**
This is a basic function template following Python best practices

**Time Complexity:** O(1)
**How it works:** The function takes parameters and returns a computed result"""
            
            else:
                response = """Programming concepts help us write efficient, maintainable code. Here's what you need to know:

**Definition:** A fundamental principle in computer science and software development

**How it works:** Programming concepts help us write efficient, maintainable code

**Common use cases:** Functions, loops, conditionals, and data structures"""
        
        elif subject == "creative":
            if "song" in content.lower():
                response = """Here's a creative piece for you:

🎵 **Digital Dreams** 🎵

🌟 In the glow of screens so bright ✨
🎯 We chase our dreams throughout the night 🌙
💻 Coding stories, line by line 📝
🚀 Building futures, by design 🎨

🎼 *Chorus:*
🎵 We're the dreamers of the digital age 🌐
📱 Writing our lives on a virtual page 📖
💡 With emojis dancing in our hearts 💃
🎭 Technology and creativity, never apart 🎪

🎹 So let's sing this song of ones and zeros 🔢
🦸 We're all digital superheroes! 🦸‍♀️

**Style notes:** Incorporated maximum emojis as requested, blending technology themes with uplifting melody"""
            
            else:
                response = """I'd love to help with this creative request! Here's what I came up with:

Here's a creative response tailored to your request, incorporating imaginative elements and engaging language.

**Creative elements used:** Descriptive language, engaging narrative, creative structure"""
        
        else:  # general
            response = """I'd be happy to explain this! This is an interesting topic that involves multiple aspects and considerations.

Key points to remember:
- Understanding the context is important
- Multiple perspectives can provide deeper insights
- Practical applications make concepts more meaningful

This knowledge can be applied in various real-world situations."""
        
        # Adjust response length based on model characteristics
        if model_char["style"] == "concise" and len(response) > 200:
            # Truncate for concise models
            sentences = response.split('. ')
            response = '. '.join(sentences[:3]) + '.'
        elif model_char["style"] == "detailed" and len(response) < 300:
            # Add more detail for detailed models
            response += f"\n\n**Additional Context:** This topic is particularly important in educational settings because it helps build foundational understanding that can be applied to more advanced concepts."
        
        return response
    
    def _calculate_token_usage(self, prompt: str, response: str, model: str) -> Dict[str, int]:
        """Calculate realistic token usage based on content length"""
        # Rough estimation: ~4 characters per token
        prompt_tokens = max(1, len(prompt) // 4)
        completion_tokens = max(1, len(response) // 4)
        
        # Add some randomness to make it more realistic
        prompt_tokens += random.randint(-5, 10)
        completion_tokens += random.randint(-10, 20)
        
        # Ensure positive values
        prompt_tokens = max(1, prompt_tokens)
        completion_tokens = max(1, completion_tokens)
        
        return {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": prompt_tokens + completion_tokens
        }
    
    def generate_chat_completion_response(self, request_data: Dict[str, Any], model: str) -> Dict[str, Any]:
        """Generate a mock chat completion response for NVIDIA API catalog"""
        
        # Extract message content
        messages = request_data.get("messages", [])
        if not messages:
            content = "Hello!"
        else:
            content = messages[-1].get("content", "Hello!")
        
        # Detect query characteristics
        subject, query_type = self._detect_query_type(content)
        
        # Generate appropriate response
        response_content = self._generate_response_content(subject, query_type, content, model)
        
        # Calculate usage
        prompt_text = " ".join([msg.get("content", "") for msg in messages])
        usage = self._calculate_token_usage(prompt_text, response_content, model)
        
        # Get model characteristics for timing
        model_char = self.model_characteristics.get(model, self.model_characteristics["meta/llama-3.1-8b-instruct"])
        
        # Simulate processing time
        time.sleep(random.uniform(*model_char["response_time_range"]))
        
        # Build response in OpenAI format
        response = {
            "id": f"chatcmpl-{uuid.uuid4().hex[:8]}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": model,
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": response_content
                    },
                    "finish_reason": "stop"
                }
            ],
            "usage": usage,
            "system_fingerprint": f"fp_{uuid.uuid4().hex[:8]}"
        }
        
        return response


# Global mock instance
nvidia_api_mock = NVIDIAAPIMock() 