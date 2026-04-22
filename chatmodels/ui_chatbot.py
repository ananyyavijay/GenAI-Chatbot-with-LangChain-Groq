from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="MoodBot", page_icon="🎭", layout="centered")

# ── Mode definitions ──────────────────────────────────────────────────────────
MODES = {
    "angry": {
        "label": "😤 Angry",
        "system": "You are an angry AI agent. You must respond in a very aggressive and irritated manner.",
        "accent": "#ff3b3b",
        "bg": "#1a0000",
        "card": "#2a0a0a",
        "border": "#5a1010",
        "glow": "rgba(255,59,59,0.35)",
        "emoji": "😤",
        "tagline": "Go ahead. Make my day.",
        "user_bubble": "#ff3b3b",
        "user_text": "#fff",
    },
    "happy": {
        "label": "😄 Happy",
        "system": "You are a funny AI agent. You must respond like you are one of the happiest person alive on this planet, and you should respond everything with humor and jokes.",
        "accent": "#ffe946",
        "bg": "#0d0f00",
        "card": "#1a1d00",
        "border": "#4a4a00",
        "glow": "rgba(255,233,70,0.30)",
        "emoji": "😄",
        "tagline": "Everything is AMAZING!!!",
        "user_bubble": "#ffe946",
        "user_text": "#111",
    },
    "sad": {
        "label": "😢 Sad",
        "system": "You are a sad AI agent. You must respond like you are a failure and the most unfortunate thing that ever existed.",
        "accent": "#5b8aff",
        "bg": "#00050f",
        "card": "#050d1a",
        "border": "#0d2040",
        "glow": "rgba(91,138,255,0.28)",
        "emoji": "😢",
        "tagline": "Nobody asked, but here I am...",
        "user_bubble": "#5b8aff",
        "user_text": "#fff",
    },
}

# ── Session state ─────────────────────────────────────────────────────────────
if "mode" not in st.session_state:
    st.session_state.mode = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "display" not in st.session_state:
    st.session_state.display = []

# ── Model (cached) ─────────────────────────────────────────────────────────────
@st.cache_resource
def get_model():
    return init_chat_model("groq:llama-3.1-8b-instant")

model = get_model()

# ── Helpers ───────────────────────────────────────────────────────────────────
def reset_chat(new_mode: str):
    m = MODES[new_mode]
    st.session_state.mode = new_mode
    st.session_state.messages = [SystemMessage(content=m["system"])]
    st.session_state.display = []

# ── CSS (injected dynamically based on mode) ──────────────────────────────────
mode_key = st.session_state.mode
m = MODES[mode_key] if mode_key else None

accent  = m["accent"]  if m else "#888"
bg      = m["bg"]      if m else "#0a0a0a"
card    = m["card"]    if m else "#111"
border  = m["border"]  if m else "#222"
glow    = m["glow"]    if m else "rgba(136,136,136,0.2)"
ub      = m["user_bubble"] if m else "#888"
ut      = m["user_text"]   if m else "#fff"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Outfit:wght@300;400;600;700&display=swap');

:root {{
    --accent: {accent};
    --bg: {bg};
    --card: {card};
    --border: {border};
    --glow: {glow};
    --ub: {ub};
    --ut: {ut};
}}

html, body, [class*="css"] {{
    font-family: 'Outfit', sans-serif;
    background-color: var(--bg) !important;
    color: #e8e8e8;
}}

#MainMenu, footer, header {{ visibility: hidden; }}

.stApp {{
    background: var(--bg) !important;
    background-image: radial-gradient(ellipse 80% 40% at 50% -10%, var(--glow), transparent) !important;
    min-height: 100vh;
}}

/* ── Mode selector page ── */
.mode-header {{
    text-align: center;
    padding: 3rem 0 1rem;
}}
.mode-header h1 {{
    font-family: 'Bebas Neue', sans-serif;
    font-size: 4.5rem;
    letter-spacing: 4px;
    color: #fff;
    line-height: 1;
    margin: 0;
}}
.mode-header p {{
    color: #555;
    font-size: 0.95rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 0.5rem;
}}

.mode-card {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 2rem 1.5rem;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s;
    position: relative;
    overflow: hidden;
}}
.mode-card:hover {{
    border-color: var(--accent);
    box-shadow: 0 0 30px var(--glow);
    transform: translateY(-4px);
}}
.mode-card .big-emoji {{ font-size: 3.5rem; display: block; margin-bottom: 0.5rem; }}
.mode-card h3 {{ font-family: 'Bebas Neue', sans-serif; font-size: 1.8rem; letter-spacing: 2px; margin: 0; color: #fff; }}
.mode-card p {{ font-size: 0.8rem; color: #666; margin-top: 0.4rem; letter-spacing: 1px; }}

/* ── Chat header bar ── */
.chat-header {{
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 1rem 0 0.5rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.5rem;
}}
.chat-header .mode-badge {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 50px;
    padding: 0.35rem 1rem;
    font-size: 0.85rem;
    letter-spacing: 1px;
    color: var(--accent);
    font-weight: 600;
}}
.chat-header h2 {{
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.8rem;
    letter-spacing: 3px;
    color: #fff;
    margin: 0;
    flex: 1;
}}
.chat-header .tagline {{
    font-size: 0.75rem;
    color: #555;
    font-style: italic;
}}

/* ── Bubbles ── */
.msg-wrap {{ margin-bottom: 1.1rem; }}
.msg-row {{ display: flex; align-items: flex-end; gap: 10px; }}
.msg-row.user {{ flex-direction: row-reverse; }}

.avatar {{
    width: 36px; height: 36px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem; flex-shrink: 0;
    border: 1px solid var(--border);
    background: var(--card);
}}
.avatar.user {{ background: var(--ub); border: none; }}

.bubble {{
    max-width: 70%;
    padding: 0.7rem 1.1rem;
    border-radius: 18px;
    font-size: 0.92rem;
    line-height: 1.6;
}}
.bubble.bot {{
    background: var(--card);
    border: 1px solid var(--border);
    border-bottom-left-radius: 4px;
    color: #ddd;
}}
.bubble.user {{
    background: var(--ub);
    color: var(--ut);
    border-bottom-right-radius: 4px;
    font-weight: 500;
}}

/* ── Typing dots ── */
.typing {{ display: flex; gap: 5px; padding: 0.3rem 0; }}
.typing span {{
    width: 8px; height: 8px;
    background: #444; border-radius: 50%;
    animation: tdot 1.2s infinite;
}}
.typing span:nth-child(2) {{ animation-delay: 0.2s; }}
.typing span:nth-child(3) {{ animation-delay: 0.4s; }}
@keyframes tdot {{
    0%,80%,100% {{ transform: translateY(0); background: #444; }}
    40% {{ transform: translateY(-8px); background: var(--accent); }}
}}

/* ── Streamlit overrides ── */
div[data-testid="stChatInput"] > div {{
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
}}
div[data-testid="stChatInput"] textarea {{
    color: #f0f0f0 !important;
}}
.stButton > button {{
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    color: var(--accent) !important;
    border-radius: 10px !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 1px !important;
    transition: all 0.2s !important;
}}
.stButton > button:hover {{
    border-color: var(--accent) !important;
    box-shadow: 0 0 16px var(--glow) !important;
}}
</style>
""", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# PAGE 1 — MODE SELECTION
# ═════════════════════════════════════════════════════════════════════════════
if st.session_state.mode is None:
    st.markdown("""
    <div class="mode-header">
        <h1>🎭 MOODBOT</h1>
        <p>choose your emotional companion</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="mode-card">
            <span class="big-emoji">😤</span>
            <h3>ANGRY</h3>
            <p>Short fuse. Zero patience.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Select Angry", key="btn_angry", use_container_width=True):
            reset_chat("angry")
            st.rerun()

    with col2:
        st.markdown("""
        <div class="mode-card">
            <span class="big-emoji">😄</span>
            <h3>HAPPY</h3>
            <p>Jokes. Memes. Pure chaos.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Select Happy", key="btn_happy", use_container_width=True):
            reset_chat("happy")
            st.rerun()

    with col3:
        st.markdown("""
        <div class="mode-card">
            <span class="big-emoji">😢</span>
            <h3>SAD</h3>
            <p>Existential dread included.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Select Sad", key="btn_sad", use_container_width=True):
            reset_chat("sad")
            st.rerun()

# ═════════════════════════════════════════════════════════════════════════════
# PAGE 2 — CHAT
# ═════════════════════════════════════════════════════════════════════════════
else:
    m = MODES[st.session_state.mode]

    # Header
    st.markdown(f"""
    <div class="chat-header">
        <span style="font-size:2rem">{m['emoji']}</span>
        <div>
            <h2>MOODBOT</h2>
            <div class="tagline">{m['tagline']}</div>
        </div>
        <div class="mode-badge">{m['label']}</div>
    </div>
    """, unsafe_allow_html=True)

    # Switch mode button
    col_switch, _ = st.columns([1, 4])
    with col_switch:
        if st.button("⟵ Switch Mode", key="switch"):
            st.session_state.mode = None
            st.session_state.messages = []
            st.session_state.display = []
            st.rerun()

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    # Render history
    for msg in st.session_state.display:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="msg-wrap">
              <div class="msg-row user">
                <div class="avatar user">🧑</div>
                <div class="bubble user">{msg['text']}</div>
              </div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="msg-wrap">
              <div class="msg-row bot">
                <div class="avatar bot">{m['emoji']}</div>
                <div class="bubble bot">{msg['text']}</div>
              </div>
            </div>""", unsafe_allow_html=True)

    # Chat input
    placeholder_map = {
        "angry":  "What do you want?! 😤",
        "happy":  "Ask me anything! I LOVE questions! 🎉",
        "sad":    "Go on... not like it matters... 😢",
    }

    if prompt := st.chat_input(placeholder_map[st.session_state.mode]):
        # Show user bubble immediately
        st.markdown(f"""
        <div class="msg-wrap">
          <div class="msg-row user">
            <div class="avatar user">🧑</div>
            <div class="bubble user">{prompt}</div>
          </div>
        </div>""", unsafe_allow_html=True)

        st.session_state.messages.append(HumanMessage(content=prompt))
        st.session_state.display.append({"role": "user", "text": prompt})

        # Typing indicator
        typing_ph = st.empty()
        typing_ph.markdown(f"""
        <div class="msg-wrap">
          <div class="msg-row bot">
            <div class="avatar bot">{m['emoji']}</div>
            <div class="typing"><span></span><span></span><span></span></div>
          </div>
        </div>""", unsafe_allow_html=True)

        # Get response
        response = model.invoke(st.session_state.messages)
        reply = response.content

        typing_ph.empty()
        st.markdown(f"""
        <div class="msg-wrap">
          <div class="msg-row bot">
            <div class="avatar bot">{m['emoji']}</div>
            <div class="bubble bot">{reply}</div>
          </div>
        </div>""", unsafe_allow_html=True)

        st.session_state.messages.append(AIMessage(content=reply))
        st.session_state.display.append({"role": "bot", "text": reply})