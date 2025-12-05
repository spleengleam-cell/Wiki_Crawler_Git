import streamlit as st
import requests
import time

# --- Configuration ---
N8N_WEBHOOK_URL = "https://fitreisen2.app.n8n.cloud/webhook/c8f9ba3d-73e8-41a7-9a83-64bde6b1c720"

# --- Page setup ---
st.set_page_config(page_title="Wiki Chatbot", page_icon="💬", layout="wide")

# --- Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "lang" not in st.session_state:
    st.session_state.lang = "de"

# --- Language Texts ---
TEXTS = {
    "de": {
        "title": "💬 Wiki Chatbot",
        "subtitle": "Stellen Sie Fragen zur Unternehmens-Wiki",
        "input": "Ihre Nachricht...",
        "send": "Senden",
        "loading": "am denken...",
        "clear": "Verlauf entfernen",
        "lang_toggle": "EN"
    },
    "en": {
        "title": "💬 Wiki Chatbot",
        "subtitle": "Ask anything about the company wiki",
        "input": "Type your message...",
        "send": "Send",
        "loading": "thinking...",
        "clear": "Clear Chat",
        "lang_toggle": "DE"
    }
}

# --- Language Toggle ---
col1, col2 = st.columns([0.95, 0.05])
with col1:
    if st.button(TEXTS[st.session_state.lang]["lang_toggle"]):
        st.session_state.lang = "en" if st.session_state.lang == "de" else "de"

# --- Header ---
st.markdown(f"<h1 style='text-align: center;'>{TEXTS[st.session_state.lang]['title']}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: gray;'>{TEXTS[st.session_state.lang]['subtitle']}</p>", unsafe_allow_html=True)

# --- CSS Animations + Style ---
st.markdown("""
<style>

@keyframes fadeInLeft {
    0% { opacity: 0; transform: translateX(-6px); }
    100% { opacity: 1; transform: translateX(0); }
}
@keyframes fadeInRight {
    0% { opacity: 0; transform: translateX(6px); }
    100% { opacity: 1; transform: translateX(0); }
}

.user-message {
    background-color: #DCF8C6;
    padding: 10px 14px;
    border-radius: 16px;
    display: inline-block;
    max-width: 70%;
    margin-bottom: 8px;
    animation: fadeInRight .25s ease-out;
    box-shadow: 0 2px 5px rgba(0,0,0,0.04);
}

.bot-message {
    background-color: #F1F0F0;
    padding: 10px 14px;
    border-radius: 16px;
    display: inline-block;
    max-width: 70%;
    margin-bottom: 8px;
    animation: fadeInLeft .25s ease-out;
    box-shadow: 0 2px 5px rgba(0,0,0,0.04);
}

.user-container { text-align: right; }
.bot-container  { text-align: left; }

.chat-history {
    max-height: 65vh;
    overflow-y: auto;
    padding-bottom: 10px;
}

/* Typing dots animation */
.typing-dots {
    width: 45px;
    display: flex;
    justify-content: space-between;
}
.typing-dots div {
    width: 8px;
    height: 8px;
    background: #bdbdbd;
    border-radius: 50%;
    animation: blink 1.4s infinite both;
}
.typing-dots div:nth-child(2) { animation-delay: .2s; }
.typing-dots div:nth-child(3) { animation-delay: .4s; }

@keyframes blink {
    0% { opacity: .3; }
    20% { opacity: 1; }
    100% { opacity: .3; }
}

/* Send button */
.stButton>button {
    transition: transform .15s ease, box-shadow .15s ease;
}
.stButton>button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

/* Clear button floating */
#clear-cache-button {
    position: fixed;
    bottom: 20px;
    right: 20px;
    background-color: #f44336;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 16px;
    cursor: pointer;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    z-index: 9999;
    transition: transform .15s ease, background .2s ease;
}
#clear-cache-button:hover {
    transform: translateY(-2px);
    background-color: #d32f2f;
}

</style>
""", unsafe_allow_html=True)

# --- Chat History ---
chat_history = st.container()
with chat_history:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"<div class='user-container'><div class='user-message'>{msg['content']}</div></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='bot-container'><div class='bot-message'>{msg['content']}</div></div>", unsafe_allow_html=True)

# --- Input ---
input_container = st.container()
with input_container:
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input(TEXTS[st.session_state.lang]["input"], key="input_field")
        send_button = st.form_submit_button(TEXTS[st.session_state.lang]["send"])

    if send_button and user_input.strip():
        # Store user message
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Placeholder for bot message
        bot_placeholder = st.empty()

        # Typing animation
        bot_placeholder.markdown("""
            <div class='bot-container'>
                <div class='bot-message'>
                    <div class='typing-dots'>
                        <div></div><div></div><div></div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Fetch from n8n
        try:
            response = requests.post(N8N_WEBHOOK_URL, json={"message": user_input})
            response.raise_for_status()
            bot_reply = response.json().get("output", "No response from bot.")
        except Exception as e:
            bot_reply = f"Error: {e}"

        time.sleep(0.5)

        # Replace dots with actual bot message
        bot_placeholder.markdown(
            f"<div class='bot-container'><div class='bot-message'>{bot_reply}</div></div>",
            unsafe_allow_html=True
        )

        st.session_state.messages.append({"role": "bot", "content": bot_reply})
        st.rerun()

# --- Clear button ---
if st.button(TEXTS[st.session_state.lang]["clear"], key="clear-cache-button"):
    st.session_state.messages = []
    st.rerun()
