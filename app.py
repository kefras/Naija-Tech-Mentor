import streamlit as st
import google.generativeai as genai

# 1. Setup
st.set_page_config(page_title="Naija Tech Mentor", page_icon="🇳🇬")
st.title("🇳🇬 Naija Tech Mentor")
st.write("Learn Tech in simple Pidgin and Hausa!")

# 2. AI Connection
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    
    # Simple Persona
    instruct = "You are Oga Tech. Explain tech in Pidgin/Hausa using Naija analogies."
    
    # THE FIX: We use 'gemini-pro' which is the most globally stable name
    model = genai.GenerativeModel("gemini-pro")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask me anything..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # Simplified generation call
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

except Exception as e:
    st.error(f"Oga, small issue: {e}")
