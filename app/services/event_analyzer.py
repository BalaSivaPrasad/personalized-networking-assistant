import logging

logger = logging.getLogger(__name__)

DEFAULT_LABELS = [
    "Artificial Intelligence", "Machine Learning", "Data Science",
    "Climate Change", "Sustainability", "Urban Planning", "Smart Cities",
    "Healthcare", "Blockchain", "Education", "Technology", "Innovation",
    "Entrepreneurship", "Digital Transformation", "Cybersecurity",
    "Cloud Computing", "Internet of Things", "Robotics", "Biotechnology", "Fintech"
]

def extract_event_themes(event_description: str, candidate_labels: list = None) -> list:
    if candidate_labels is None:
        candidate_labels = DEFAULT_LABELS
    
    event_lower = event_description.lower()
    scored_themes = []
    
    for label in candidate_labels:
        label_lower = label.lower()
        keywords = label_lower.split()
        score = sum(1 for keyword in keywords if keyword in event_lower)
        if score > 0:
            scored_themes.append((label, score))
    
    scored_themes.sort(key=lambda x: x[1], reverse=True)
    top_themes = [theme for theme, score in scored_themes[:3]]
    
    if not top_themes:
        top_themes = ["Technology", "Innovation", "Networking"]
    
    return top_themes