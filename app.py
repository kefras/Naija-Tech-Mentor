import streamlit as st
import google.generativeai as genai

# ----------------------------
# CONFIG
# ----------------------------
st.set_page_config(page_title="Naija Tech Mentor", page_icon="🇳🇬")

st.title("🇳🇬 Naija Tech Mentor")
st.write("Your AI tutor for WAEC & JAMB (Pidgin + Hausa)")

# ----------------------------
# API SETUP
# ----------------------------
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)

    model = genai.GenerativeModel("gemini-1.5-flash")

    # ----------------------------
    # CHAT HISTORY
    # ----------------------------
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # ----------------------------
    # USER INPUT
    # ----------------------------
    if prompt := st.chat_input("Ask your question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            full_prompt = f"""
            You are Oga Tech, a Nigerian tutor.

            Explain this in simple Pidgin English and a bit of Hausa.
            Use real-life Nigerian examples.

            Question: {prompt}
            """

            response = model.generate_content(full_prompt)

            reply = response.text if hasattr(response, "text") else str(response)

            st.markdown(reply)

            st.session_state.messages.append({
                "role": "assistant",
                "content": reply
            })

except Exception as e:
    st.error(f"Oga, small issue: {e}")
