import streamlit as st
import requests


# --- Configuration ---
# Replace this with your n8n webhook URL
N8N_WEBHOOK_URL = "https://fitreisen2.app.n8n.cloud/webhook-test/c8f9ba3d-73e8-41a7-9a83-64bde6b1c720"

st.set_page_config(page_title="My n8n Chatbot", page_icon="💬")

st.title("💬 My n8n Chatbot")
st.markdown("Type a message and the bot will reply!")

# --- Session state to keep conversation ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- User input ---
user_input = st.text_input("You:", "")

if st.button("Send") or user_input:
    if user_input:
        # Add user message to conversation
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Call n8n webhook
        try:
            response = requests.post(
                N8N_WEBHOOK_URL,
                json={"message": user_input}  # Adjust depending on your webhook payload
            )
            response.raise_for_status()
            bot_reply = response.json().get("reply", "No response from bot.")
        except Exception as e:
            bot_reply = f"Error: {e}"

        # Add bot response
        st.session_state.messages.append({"role": "bot", "content": bot_reply})

# --- Display conversation ---
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**Bot:** {msg['content']}")
