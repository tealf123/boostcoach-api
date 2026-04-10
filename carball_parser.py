"""
Simplified replay parser — send raw replay bytes to Claude for analysis
"""

def parse_replay(replay_path):
    """
    Read replay file as binary and return for Claude analysis
    
    Args:
        replay_path: Path to .replay file
    
    Returns:
        dict: Replay data ready for Claude
    """
    try:
        with open(replay_path, 'rb') as f:
            replay_bytes = f.read()
        
        return {
            'status': 'success',
            'replay_bytes': replay_bytes,
            'file_size': len(replay_bytes),
            'summary': {
                'file_size_mb': len(replay_bytes) / (1024*1024)
            }
        }
    
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'message': f'Failed to read replay: {str(e)}'
        }
