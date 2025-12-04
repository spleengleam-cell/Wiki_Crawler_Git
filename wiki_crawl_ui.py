import streamlit as st
import requests

# --- Configuration ---
N8N_WEBHOOK_URL = "https://fitreisen2.app.n8n.cloud/webhook/c8f9ba3d-73e8-41a7-9a83-64bde6b1c720"

# --- Page setup ---
st.set_page_config(page_title="Wiki Chatbot", page_icon="💬")
st.markdown("<h1 style='text-align: center;'>💬 Wiki Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color:gray;'>Ask anything about the company wiki</p>", unsafe_allow_html=True)

# --- Session state ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- CSS for chat bubbles ---
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
input:focus, textarea:focus, button:focus {
    outline: none;
}
</style>
""", unsafe_allow_html=True)

# --- User input ---
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message...")
    submit_button = st.form_submit_button("Send")

if submit_button and user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Call n8n webhook
    try:
        response = requests.post(
            N8N_WEBHOOK_URL,
            json={"message": user_input}
        )
        response.raise_for_status()
        bot_reply = response.json().get("output", "No response from bot.")
    except Exception as e:
        bot_reply = f"Error: {e}"
    
    # Add bot response
    st.session_state.messages.append({"role": "bot", "content": bot_reply})

# --- Display conversation ---
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='user-container'><div class='user-message'>{msg['content']}</div></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-container'><div class='bot-message'>{msg['content']}</div></div>", unsafe_allow_html=True)
