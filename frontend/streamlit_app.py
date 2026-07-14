import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000/api"

st.set_page_config(page_title="Networking Assistant", page_icon="🤝", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .main-header {
        font-family: 'Poppins', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        text-align: center;
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(30, 60, 114, 0.3);
    }
    
    .suggestion-box {
        font-family: 'Poppins', sans-serif;
        font-size: 1.15rem;
        font-weight: 400;
        padding: 1.2rem;
        border-radius: 12px;
        border-left: 5px solid #1e3c72;
        margin: 0.8rem 0;
        background: linear-gradient(135deg, #f0f4ff 0%, #e8edf5 100%);
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        transition: transform 0.2s;
    }
    
    .suggestion-box:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 15px rgba(30, 60, 114, 0.2);
    }
    
    .theme-box {
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 0.8rem 1.2rem;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(30, 60, 114, 0.3);
    }
    
    .stButton>button {
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #2a5298 0%, #1e3c72 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(30, 60, 114, 0.4);
    }
    
    .section-title {
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        color: #1e3c72;
        font-size: 1.5rem;
        margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🤝 Personalized Networking Assistant</h1>', unsafe_allow_html=True)

if 'suggestions' not in st.session_state:
    st.session_state.suggestions = None
if 'themes' not in st.session_state:
    st.session_state.themes = None

def generate_starters(event_desc, interests):
    try:
        r = requests.post(f"{BASE_URL}/generate-conversation", 
                         json={"event_description": event_desc, "interests": interests}, timeout=30)
        if r.status_code == 200:
            d = r.json()
            return d['themes'], d['suggestions']
    except:
        st.error("Cannot connect to backend. Start FastAPI on port 8000.")
    return None, None

def submit_feedback(suggestion, action):
    try:
        requests.post(f"{BASE_URL}/feedback", 
                     json={"suggestion": suggestion, "action": action}, timeout=10)
    except:
        pass

def fact_check_query(query):
    try:
        r = requests.post(f"{BASE_URL}/fact-check", json={"query": query}, timeout=30)
        return r.json() if r.status_code == 200 else {"result": "Error", "source_url": None}
    except:
        return {"result": "Connection error", "source_url": None}

def load_history():
    try:
        r = requests.get(f"{BASE_URL}/history", timeout=10)
        return r.json().get('history', []) if r.status_code == 200 else []
    except:
        return []

def load_feedback_history():
    try:
        r = requests.get(f"{BASE_URL}/feedback-history", timeout=10)
        return r.json().get('feedback', []) if r.status_code == 200 else []
    except:
        return []

with st.sidebar:
    st.header("📋 About")
    st.info("AI-powered assistant that generates smart conversation starters for networking events.")
    st.header("🔍 How it works")
    st.write("1. Enter event description\n2. Add your interests\n3. Generate starters\n4. Verify facts with Wikipedia")

st.subheader("🎯 Generate Conversation Starters")
with st.form("form"):
    event = st.text_area("Event Description", placeholder="e.g., AI for Sustainable Cities conference", height=100)
    interests = st.text_input("Your Interests (comma-separated)", placeholder="e.g., climate change, AI, urban planning")
    if st.form_submit_button("🚀 Generate Starters", use_container_width=True):
        if event and interests:
            interests_list = [i.strip() for i in interests.split(',') if i.strip()]
            with st.spinner("Generating..."):
                themes, suggestions = generate_starters(event, interests_list)
                if themes and suggestions:
                    st.session_state.themes = themes
                    st.session_state.suggestions = suggestions
                    st.success("✅ Ready!")
        else:
            st.error("Fill all fields")

if st.session_state.suggestions:
    st.markdown("---")
    if st.session_state.themes:
        st.subheader("🎨 Extracted Themes")
        cols = st.columns(len(st.session_state.themes))
        for i, theme in enumerate(st.session_state.themes):
            cols[i].markdown(f'<div class="theme-box">{theme}</div>', unsafe_allow_html=True)
    
    st.subheader("💬 Conversation Starters")
    for i, s in enumerate(st.session_state.suggestions):
        st.markdown(f"""
        <div class="suggestion-box">
            <strong>Starter {i+1}:</strong> {s}
        </div>
        """, unsafe_allow_html=True)
        c1, c2, _ = st.columns([1,1,8])
        with c1:
            if st.button("👍", key=f"like_{i}"):
                submit_feedback(s, "like")
                st.success("Thanks!")
        with c2:
            if st.button("👎", key=f"dislike_{i}"):
                submit_feedback(s, "dislike")
                st.info("Noted!")
        st.write("")

st.markdown("---")
st.subheader("🔍 Fact Check with Wikipedia")
q = st.text_input("Enter a topic to verify", placeholder="e.g., Machine Learning")
if st.button("🔎 Verify Fact") and q:
    with st.spinner("Checking Wikipedia..."):
        r = fact_check_query(q)
        st.success(r.get('result', 'No result'))
        if r.get('source_url'):
            st.markdown(f"[📖 Read more on Wikipedia]({r['source_url']})")

st.markdown("---")
st.subheader("📚 Recent Conversations")
history = load_history()
if history:
    for entry in reversed(history[-5:]):
        st.markdown(f"**📝 Event:** {entry.get('event_description', 'N/A')[:80]}")
        st.markdown(f"**🎨 Themes:** {', '.join(entry.get('themes', []))}")
        st.markdown("**💬 Suggestions:**")
        for j, s in enumerate(entry.get('suggestions', [])):
            st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;{j+1}. {s}")
        st.markdown(f"*{entry.get('timestamp', '')[:10]}*")
        st.markdown("---")
else:
    st.info("No history yet.")

st.markdown("---")
st.subheader("📊 Your Feedback")
feedback = load_feedback_history()
if feedback:
    for entry in reversed(feedback[-10:]):
        icon = "👍" if entry.get('action') == 'like' else "👎"
        st.markdown(f"{icon} {entry.get('suggestion', '')[:100]}...")
        st.caption(f"{entry.get('timestamp', '')[:10]}")
        st.write("---")
else:
    st.info("No feedback yet.")

st.markdown("---")
st.markdown("<p style='text-align:center;color:#666;'>Built with ❤️ using FastAPI & Streamlit</p>", unsafe_allow_html=True)