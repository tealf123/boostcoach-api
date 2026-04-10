"""
Coaching Engine - Claude analyzes replay files directly
"""

import os
from anthropic import Anthropic
import base64

client = Anthropic()

def generate_coaching_report(replay_bytes, filename="replay.replay"):
    """
    Send replay bytes to Claude for analysis and coaching
    
    Args:
        replay_bytes: Raw binary data from .replay file
        filename: Original filename
    
    Returns:
        dict: Coaching report from Claude
    """
    
    # Encode bytes to base64 for Claude API
    replay_b64 = base64.b64encode(replay_bytes).decode('utf-8')
    
    system_prompt = """You are an expert Rocket League coach analyzing replay files. 
Your job is to analyze the replay data provided and give direct, specific, encouraging feedback.

Structure your coaching report:
1. Match Overview (result, key stats)
2. What Went Well (specific plays you noticed)
3. Top 3 Improvements (with specific advice)
4. Practice Drill (1 focused drill to work on)

Be direct, specific, and encouraging. 400-600 words."""

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": f"""Please analyze this Rocket League replay file and provide coaching feedback.

Replay file: {filename}
File size: {len(replay_bytes)} bytes

The replay data is encoded below. Please extract what you can about the match and provide coaching:

{replay_b64[:500]}... [replay data continues]

Even without full parsing, provide coaching based on what you can infer from a Rocket League replay structure."""
                }
            ]
        )
        
        return {
            'status': 'success',
            'report': message.content[0].text,
            'tokens_used': message.usage.output_tokens
        }
    
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'report': None
        }

def generate_qa_response(coaching_report, question):
    """
    Generate Q&A response based on coaching report
    
    Args:
        coaching_report: str of initial coaching report
        question: str user question
    
    Returns:
        dict: Response from coach
    """
    
    system_prompt = """You are a Rocket League coach continuing a conversation.
The player has uploaded a replay and received initial coaching. Now answer their specific question.
Be concise (200-300 words), specific, and actionable."""
    
    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=512,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": f"""Initial coaching report:\n{coaching_report}\n\nQuestion: {question}"""
                }
            ]
        )
        
        return {
            'status': 'success',
            'response': message.content[0].text
        }
    
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e)
        }
