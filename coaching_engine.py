import os
from anthropic import Anthropic

def generate_coaching_report(replay_bytes, filename="replay.replay"):
    try:
        message = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY')).messages.create(
            model="claude-haiku-4-5",
            max_tokens=1024,
            system="""You are a Rocket League coach analyzing replays. Provide:
1. Match Overview
2. What Went Well  
3. Top 3 Improvements
4. Practice Drill

Be direct and specific. 300-500 words.""",
            messages=[
                {
                    "role": "user",
                    "content": f"Rocket League replay uploaded ({filename}). Provide general coaching advice for improvement."
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
            'error': str(e)
        }

def generate_qa_response(coaching_report, question):
    try:
        message = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY')).messages.create(
            model="claude-haiku-4-5",
            max_tokens=512,
            system="You are a Rocket League coach. Answer briefly and specifically.",
            messages=[
                {
                    "role": "user",
                    "content": f"Report:\n{coaching_report}\n\nQ: {question}"
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
