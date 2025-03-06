import streamlit as st
from ConversationManager import ConversationManager

st.title("AI Chatbot")

if 'chat_manager' not in st.session_state:
    st.session_state['chat_manager'] = ConversationManager()
chat_manager = st.session_state['chat_manager']

st.sidebar.header("Chatbot Settings")
temp = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7, 0.1)
max_tokens = st.sidebar.slider("Max Tokens Per Message", 50, 500, 150, 10)
total_max_tokens = st.sidebar.slider("Max Tokens in History", 500, 5000, 2000, 100)

persona = st.sidebar.selectbox("Select Chatbot Persona", ["Default", "Friendly", "Professional", "Custom"])
if persona == "Custom":
    custom_message = st.sidebar.text_area("Enter Custom System Message")
    if st.sidebar.button("Set Custom Message") and custom_message:
        chat_manager.set_custom_system_message(custom_message)
else:
    chat_manager.set_persona(persona)

if 'conversation_history' not in st.session_state:
    st.session_state['conversation_history'] = []

user_input = st.text_input("Type your message...")
if user_input:
    response = chat_manager.chat_completion(user_input, temp, max_tokens, total_max_tokens)
    st.session_state['conversation_history'].append({"role": "user", "content": user_input})
    st.session_state['conversation_history'].append({"role": "assistant", "content": response})

for message in st.session_state['conversation_history']:
    with st.container():
        st.write(f"{message['role']}: {message['content']}")

if st.sidebar.button("Reset Chat History"):
    chat_manager.reset_conversation_history()
    st.session_state['conversation_history'] = []
    st.experimental_rerun()
