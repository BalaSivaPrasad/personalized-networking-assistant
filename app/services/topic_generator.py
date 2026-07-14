import random

TEMPLATES = [
    "I noticed this event focuses on {theme1}. What aspects of {theme1} interest you most?",
    "Given your interest in {interest1}, how do you see it connecting with {theme2}?",
    "What developments in {theme1} do you find most exciting right now?",
    "I see you're interested in {interest1}. Have you worked on any projects related to {theme2}?",
    "How do you think {theme1} will evolve in the next few years?",
    "What brings you to this event? I'm particularly interested in {theme1}.",
    "Have you seen any interesting applications of {interest1} in {theme2} recently?",
    "What's your take on the intersection of {theme1} and {interest1}?",
]

def generate_topics(themes: list, interests: list) -> list:
    random.seed(42)
    theme1 = themes[0] if themes else "technology"
    theme2 = themes[1] if len(themes) > 1 else theme1
    interest1 = interests[0] if interests else "innovation"
    
    selected = random.sample(TEMPLATES, 3)
    return [t.format(theme1=theme1, theme2=theme2, interest1=interest1) for t in selected]