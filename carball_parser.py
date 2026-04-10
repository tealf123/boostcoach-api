"""
Carball Replay Parser Wrapper
Handles .replay file parsing and data extraction
"""

import json
from carball.json_parser import JSONParser
from carball.analysis.utils.pandas_manager import PandasManager

def parse_replay(replay_path):
    """
    Parse a Rocket League replay file using Carball
    
    Args:
        replay_path: Path to .replay file
    
    Returns:
        dict: Parsed match data with summary and key events
    """
    try:
        # Initialize parser
        parser = JSONParser(replay_path)
        
        # Get basic metadata
        game = parser.game
        
        # Extract summary data
        summary = {
            'teams': [],
            'goals': [],
            'duration': game.length,
            'map': game.map,
            'playlist': game.playlist,
        }
        
        # Team and player data
        for team in game.teams:
            team_data = {
                'name': team.name or f'Team {team.is_orange + 1}',
                'is_orange': team.is_orange,
                'players': []
            }
            
            for player in team.players:
                player_data = {
                    'name': player.name,
                    'id': player.id,
                    'rank': player.rank if hasattr(player, 'rank') else None,
                    'goals': player.goal_count,
                    'assists': player.assists,
                    'saves': player.saves,
                    'shots': player.shots,
                    'boost_usage': player.boost_usage if hasattr(player, 'boost_usage') else 0,
                }
                team_data['players'].append(player_data)
            
            summary['teams'].append(team_data)
        
        # Goal events
        for goal in game.goals:
            goal_data = {
                'frame': goal.frame_number,
                'time': goal.time,
                'player': goal.player.name if goal.player else 'Unknown',
                'team': goal.team,
                'assisted_by': goal.assisted_by.name if goal.assisted_by else None,
            }
            summary['goals'].append(goal_data)
        
        return {
            'status': 'success',
            'summary': summary,
            'raw_data': json.dumps(summary, default=str)
        }
    
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'message': f'Failed to parse replay: {str(e)}'
        }
