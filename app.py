import streamlit as st
import google.generativeai as genai

# --- PAGE SETUP ---
st.set_page_config(page_title="Naija Tech Mentor", page_icon="🇳🇬")
st.title("🇳🇬 Naija Tech Mentor")
st.write("Learn Tech in simple Pidgin and Hausa!")

# --- API SETUP ---
API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=API_KEY)

# Using the most stable model name
model = genai.GenerativeModel('gemini-1.5-flash-latest')

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Ask me about APIs, Data, or Python..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # We build the "Naija Persona" directly into the request here
    instruction = (
        "You are a friendly Nigerian tech mentor. Explain the following "
        "concept using a mix of clear English, Nigerian Pidgin, and "
        "relatable Nigerian analogies. If asked in Hausa, respond in Hausa. "
        f"Concept: {prompt}"
    )

    try:
        response = model.generate_content(instruction)
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Oga, small error occur: {e}")
