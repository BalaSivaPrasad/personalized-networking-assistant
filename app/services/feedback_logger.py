import json
from pathlib import Path
from datetime import datetime

FEEDBACK_FILE = Path(__file__).parent.parent.parent / "data" / "feedback.json"

def log_feedback(data: dict):
    FEEDBACK_FILE.parent.mkdir(parents=True, exist_ok=True)
    if 'timestamp' not in data:
        data['timestamp'] = datetime.now().isoformat()
    
    feedback = load_feedback()
    feedback.append(data)
    with open(FEEDBACK_FILE, 'w') as f:
        json.dump(feedback, f, indent=2)

def load_feedback():
    FEEDBACK_FILE.parent.mkdir(parents=True, exist_ok=True)
    if FEEDBACK_FILE.exists():
        with open(FEEDBACK_FILE, 'r') as f:
            return json.load(f)
    return []