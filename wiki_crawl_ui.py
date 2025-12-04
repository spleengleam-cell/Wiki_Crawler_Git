import streamlit as st
import requests
import time

# --- Configuration ---
N8N_WEBHOOK_URL = "https://fitreisen2.app.n8n.cloud/webhook/c8f9ba3d-73e8-41a7-9a83-64bde6b1c720"

# --- Page setup ---
st.set_page_config(page_title="Wiki Chatbot", page_icon="💬", layout="wide")

# --- Session state ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "lang" not in st.session_state:
    st.session_state.lang = "de"  # default German

# --- Language dictionary ---
TEXTS = {
    "de": {
        "title": "💬 Wiki Chatbot",
        "subtitle": "Stellen Sie Fragen zur Unternehmens-Wiki",
        "input": "Ihre Nachricht...",
        "send": "Senden",
        "loading": "am denken..."
    },
    "en": {
        "title": "💬 Wiki Chatbot",
        "subtitle": "Ask anything about the company wiki",
        "input": "Type your message...",
        "send": "Send",
        "loading": "thinking..."
    }
}

# --- Top buttons: Language toggle + Clear chat ---
col1, col2 = st.columns([0.8, 0.2])
with col1:
    if st.button("EN" if st.session_state.lang == "de" else "DE"):
        st.session_state.lang = "en" if st.session_state.lang == "de" else "de"
with col2:
    if st.button("🗑️ Chat löschen"):
        st.session_state.messages = []

# --- Header ---
st.markdown(f"<h1 style='text-align: center;'>{TEXTS[st.session_state.lang]['title']}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color:gray;'>{TEXTS[st.session_state.lang]['subtitle']}</p>", unsafe_allow_html=True)

# --- CSS for chat bubbles + scrollable chat history + sticky input ---
st.markdown("""
<style>
.user-message {
    background-color: #DCF8C6;
    padding: 8px 12px;
    border-radius: 15px;
    display: inline-block;
    max-width: 70%;
    margin-bottom: 5px;
}
.bot-message {
    background-color: #F1F0F0;
    padding: 8px 12px;
    border-radius: 15px;
    display: inline-block;
    max-width: 70%;
    margin-bottom: 5px;
}
.user-container {
    text-align: right;
}
.bot-container {
    text-align: left;
}
.chat-history {
    max-height: 65vh;
    overflow-y: auto;
    padding-bottom: 10px;
}
.stTextInput>div>div>input {
    padding: 10px;
}
input:focus, textarea:focus, button:focus {
    outline: none;
}
</style>
""", unsafe_allow_html=True)

# --- Chat history container ---
chat_history = st.container()

# --- Display conversation ---
with chat_history:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"<div class='user-container'><div class='user-message'>{msg['content']}</div></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='bot-container'><div class='bot-message'>{msg['content']}</div></div>", unsafe_allow_html=True)

# --- Input form pinned at the bottom ---
input_container = st.container()
with input_container:
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input(TEXTS[st.session_state.lang]["input"], key="input_field")
        submit_button = st.form_submit_button(TEXTS[st.session_state.lang]["send"])

    if submit_button and user_input:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Placeholder for bot reply
        bot_placeholder = st.empty()
        
        # Show spinner while waiting for bot response
        with st.spinner(TEXTS[st.session_state.lang]["loading"]):
            try:
                response = requests.post(
                    N8N_WEBHOOK_URL,
                    json={"message": user_input}
                )
                response.raise_for_status()
                bot_reply = response.json().get(
                    "output",
                    "Keine Antwort vom Bot." if st.session_state.lang=="de" else "No response from bot."
                )
                time.sleep(0.5)
            except Exception as e:
                bot_reply = f"Error: {e}"
        
        # Add bot response
        st.session_state.messages.append({"role": "bot", "content": bot_reply})
        
        # Rerun to display updated chat
        st.rerun()
