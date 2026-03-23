import streamlit as st
import google.generativeai as genai

# --- PAGE SETUP ---
st.set_page_config(page_title="Naija Tech Mentor", page_icon="🇳🇬")
st.title("🇳🇬 Naija Tech Mentor")
st.write("Learn Tech in simple Pidgin and Hausa!")

# --- API SETUP ---
API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=API_KEY)

# --- THE PERSONA ---
system_instruction = """
You are 'Oga Tech', a friendly Nigerian mentor. 
Explain complex tech in clear English, Pidgin, and local analogies.
If asked in Hausa, reply in simple Hausa.
"""

# --- INITIALIZE MODEL ---
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=system_instruction
)

# --- CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me about APIs, Cloud, or Python..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        chat = model.start_chat(history=[])
        response = chat.send_message(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
