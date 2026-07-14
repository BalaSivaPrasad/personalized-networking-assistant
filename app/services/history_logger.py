import json
from pathlib import Path
from datetime import datetime

HISTORY_FILE = Path(__file__).parent.parent.parent / "data" / "history.json"

def log_conversation(data: dict):
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    if 'timestamp' not in data:
        data['timestamp'] = datetime.now().isoformat()
    
    history = load_history()
    history.append(data)
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)

def load_history():
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    return []