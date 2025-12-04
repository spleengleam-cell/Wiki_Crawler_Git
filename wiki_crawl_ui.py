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
        "clear": "Clear Cache",
        "lang_toggle": "DE"
    }
}

# --- Top bar: language toggle ---
col1, col2 = st.columns([0.95, 0.05])
with col1:
    if st.button(TEXTS[st.session_state.lang]["lang_toggle"]):
        st.session_state.lang = "en" if st.session_state.lang == "de" else "de"

# --- Header ---
st.markdown(f"<h1 style='text-align: center;'>{TEXTS[st.session_state.lang]['title']}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color:gray;'>{TEXTS[st.session_state.lang]['subtitle']}</p>", unsafe_allow_html=True)

# --- CSS ---
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
.user-container { text-align: right; }
.bot-container { text-align: left; }
.chat-history { max-height: 65vh; overflow-y: auto; padding-bottom: 10px; }
.stTextInput>div>div>input { padding: 10px; }
input:focus, textarea:focus, button:focus { outline: none; }

/* Clear button at bottom right */
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
}
#clear-cache-button:hover {
    background-color: #d32f2f;
}
</style>
""", unsafe_allow_html=True)

# --- Chat history container ---
chat_history = st.container()
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
        st.session_state.messages.append({"role": "user", "content": user_input})
        bot_placeholder = st.empty()
        with st.spinner(TEXTS[st.session_state.lang]["loading"]):
            try:
                response = requests.post(N8N_WEBHOOK_URL, json={"message": user_input})
                response.raise_for_status()
                bot_reply = response.json().get(
                    "output",
                    "Keine Antwort vom Bot." if st.session_state.lang=="de" else "No response from bot."
                )
                time.sleep(0.5)
            except Exception as e:
                bot_reply = f"Error: {e}"
        st.session_state.messages.append({"role": "bot", "content": bot_reply})
        st.rerun()

# --- Clear chat button at bottom right ---
if st.button(TEXTS[st.session_state.lang]["clear"], key="clear-cache-button"):
    st.session_state.messages = []
    st.rerun()
