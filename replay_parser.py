import requests
import json

BALLCHASING_API = "https://ballchasing.com/api"

def upload_to_ballchasing(replay_bytes, filename):
    """Upload replay to ballchasing and get parsed data"""
    try:
        # Upload to ballchasing
        files = {'file': (filename, replay_bytes)}
        r = requests.post(f"{BALLCHASING_API}/v2/upload", files=files, timeout=30)
        
        if r.status_code not in [200, 201]:
            return {'status': 'error', 'error': f'Ballchasing upload failed: {r.status_code}'}
        
        data = r.json()
        replay_id = data.get('id')
        
        if not replay_id:
            return {'status': 'error', 'error': 'No replay ID returned'}
        
        # Get parsed data
        r2 = requests.get(f"{BALLCHASING_API}/v2/replays/{replay_id}", timeout=30)
        if r2.status_code != 200:
            return {'status': 'error', 'error': f'Failed to fetch parsed data: {r2.status_code}'}
        
        parsed = r2.json()
        
        # Extract useful coaching data
        summary = {
            'teams': [],
            'duration': parsed.get('duration', 0),
            'map': parsed.get('map_code', 'Unknown'),
            'playlist': parsed.get('playlist_name', 'Unknown')
        }
        
        # Player stats
        for team_idx, team in enumerate(parsed.get('teams', [])):
            team_data = {
                'name': f"Team {team_idx + 1}",
                'players': []
            }
            for player in team.get('players', []):
                team_data['players'].append({
                    'name': player.get('name', 'Unknown'),
                    'goals': player.get('stats', {}).get('core', {}).get('goals', 0),
                    'assists': player.get('stats', {}).get('core', {}).get('assists', 0),
                    'saves': player.get('stats', {}).get('core', {}).get('saves', 0),
                    'shots': player.get('stats', {}).get('core', {}).get('shots', 0),
                })
            summary['teams'].append(team_data)
        
        return {
            'status': 'success',
            'summary': summary,
            'full_data': parsed
        }
    
    except requests.exceptions.Timeout:
        return {'status': 'error', 'error': 'Ballchasing API timeout'}
    except Exception as e:
        return {'status': 'error', 'error': str(e)}
