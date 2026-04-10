import os
from anthropic import Anthropic
import json

def generate_coaching_report(parsed_data):
    """Generate coaching from parsed replay data"""
    try:
        # Format data for Claude
        context = f"""Match Data:
- Duration: {parsed_data.get('duration', 0)} seconds
- Map: {parsed_data.get('map', 'Unknown')}
- Playlist: {parsed_data.get('playlist', 'Unknown')}

Teams:
"""
        for team in parsed_data.get('teams', []):
            context += f"\n{team['name']}:\n"
            for player in team.get('players', []):
                context += f"  - {player['name']}: {player['goals']} goals, {player['assists']} assists, {player['saves']} saves, {player['shots']} shots\n"
        
        message = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY')).messages.create(
            model="claude-haiku-4-5",
            max_tokens=1024,
            system="""You are a Rocket League coach. Analyze the match data and provide:
1. Match Overview (who won, key stats)
2. What Went Well (positive patterns)
3. Top 3 Improvements (specific, actionable)
4. Practice Drill (one focused drill)

Be direct, specific, encouraging. 300-500 words.""",
            messages=[
                {
                    "role": "user",
                    "content": f"Analyze this Rocket League match and provide coaching:\n\n{context}"
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
