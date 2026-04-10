"""
Coaching Engine - Claude-based AI coaching generation
Takes parsed replay data and generates coaching reports
"""

import os
from anthropic import Anthropic

client = Anthropic()

def generate_coaching_report(parsed_data, player_rank=None):
    """
    Generate a coaching report from parsed replay data using Claude
    
    Args:
        parsed_data: dict from carball parser
        player_rank: Rank of the player being analyzed (optional)
    
    Returns:
        str: Coaching report
    """
    
    # Extract summary
    summary = parsed_data.get('summary', {})
    
    # Build context for Claude
    context = _build_coaching_context(summary, player_rank)
    
    # Coaching system prompt
    system_prompt = """You are an expert Rocket League coach. Your role is to analyze match replays and provide direct, 
specific, encouraging feedback that teaches players how to improve.

Your coaching style:
- Be specific: Reference actual plays from the match, not generalities
- Be actionable: Tell them what to practice, not just what they did wrong
- Be encouraging: Acknowledge what went well alongside improvements
- Be direct: No fluff, no data dumps. Coach-like conversation.

Structure your report as:
1. Match Summary (1-2 sentences on the result)
2. What Went Well (1-2 specific plays or patterns)
3. Top 3 Things to Improve (each with specific play reference + how to fix)
4. Practice Drill (1 focused drill to work on this week)

Keep it 400-600 words. Be human, not robotic."""

    # Call Claude
    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": context
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

def generate_qa_response(parsed_data, coaching_report, question):
    """
    Generate a Q&A response based on the match and coaching report
    
    Args:
        parsed_data: dict from carball parser
        coaching_report: str of the initial coaching report
        question: str user question
    
    Returns:
        str: Response from coach
    """
    
    summary = parsed_data.get('summary', {})
    context = _build_coaching_context(summary)
    
    system_prompt = """You are a Rocket League coach continuing a conversation about a match the player just analyzed.
You have already given them initial feedback. Now answer their specific question about their gameplay.

Be specific to THEIR replay and THEIR plays. Reference frames/times/specific decisions when possible.
Keep answers concise (200-300 words max) and actionable."""
    
    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=512,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": f"Match context:\n{context}\n\nInitial coaching report:\n{coaching_report}\n\nQuestion: {question}"
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

def _build_coaching_context(summary, player_rank=None):
    """Build match context for Claude prompt"""
    
    rank_str = f"\nPlayer Rank: {player_rank}" if player_rank else ""
    
    context = f"""
Analyze this Rocket League match:

Map: {summary.get('map', 'Unknown')}
Playlist: {summary.get('playlist', 'Unknown')}
Duration: {summary.get('duration', 0)} seconds{rank_str}

Teams:
"""
    
    for team in summary.get('teams', []):
        team_name = "Orange Team" if team.get('is_orange') else "Blue Team"
        context += f"\n{team_name}:\n"
        
        for player in team.get('players', []):
            context += f"  - {player.get('name', 'Unknown')}: "
            context += f"{player.get('goals', 0)} goals, {player.get('assists', 0)} assists, "
            context += f"{player.get('saves', 0)} saves\n"
    
    context += "\nGoals:\n"
    for goal in summary.get('goals', []):
        assist_str = f" (assist: {goal.get('assisted_by')})" if goal.get('assisted_by') else ""
        context += f"  - {goal.get('time', '?')}: {goal.get('player', 'Unknown')}{assist_str}\n"
    
    return context
