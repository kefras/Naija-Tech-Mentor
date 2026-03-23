import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Naija Tech Mentor", page_icon="🇳🇬")
st.title("🇳🇬 Naija Tech Mentor")
st.write("Learn Tech in simple Pidgin and Hausa!")

try:
    API_KEY = "your_api_key_here"  # or st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)

    instruct = "You are Oga Tech. Explain tech in Pidgin/Hausa using Naija analogies."

    model = genai.GenerativeModel("gemini-1.5-flash")

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
            full_prompt = f"{instruct}\n\nUser: {prompt}"
            response = model.generate_content(full_prompt)

            reply = response.text if hasattr(response, "text") else str(response)

            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})

except Exception as e:
    st.error(f"Oga, small issue: {e}")
