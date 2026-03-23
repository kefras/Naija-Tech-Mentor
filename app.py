import streamlit as st
import google.generativeai as genai

# 1. Basic Page Info
st.set_page_config(page_title="Naija Tech Mentor", page_icon="🇳🇬")
st.title("🇳🇬 Naija Tech Mentor")
st.write("Learn Tech in simple Pidgin and Hausa!")

# 2. Connect the AI brain
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    
    # Define the Oga Tech persona
    instruct = "You are Oga Tech. Explain complex tech in Pidgin and Hausa using local Nigerian analogies."
    model = genai.GenerativeModel("gemini-1.5-flash-latest", system_instruction=instruct)

    # 3. Chat Interface
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
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

except Exception as e:
    st.error(f"Small error occur: {e}")
