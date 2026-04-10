import os
from anthropic import Anthropic
import base64

def generate_coaching_report(replay_bytes, filename="replay.replay"):
    try:
        replay_b64 = base64.b64encode(replay_bytes).decode('utf-8')[:500]
        
        message = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY')).messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=1024,
            system="""You are a Rocket League coach. Analyze this replay and provide:
1. Match Overview
2. What Went Well  
3. Top 3 Improvements
4. Practice Drill

Be direct, specific, encouraging. 400-600 words.""",
            messages=[
                {
                    "role": "user",
                    "content": f"Analyze this Rocket League replay ({filename}, {len(replay_bytes)} bytes) and provide coaching."
                }
            ]
        )
        
        return {
            'status': 'success',
            'report': message.content[0].text
        }
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'report': None
        }

def generate_qa_response(coaching_report, question):
    try:
        message = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY')).messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=512,
            system="You are a Rocket League coach answering questions. Be concise and specific.",
            messages=[
                {
                    "role": "user",
                    "content": f"""Coaching report:\n{coaching_report}\n\nQuestion: {question}"""
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
