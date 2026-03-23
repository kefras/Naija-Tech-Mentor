import streamlit as st
import google.generativeai as genai

# --- PAGE SETUP ---
st.set_page_config(page_title="Naija Tech Mentor", page_icon="🇳🇬")
st.title("🇳🇬 Naija Tech Mentor: Learn DeepTech in Pidgin & Hausa")
st.write("Ask me any complex tech question, and I will break it down for you with local Naija analogies!")

# --- API SETUP ---
# In production, securely add your API key to Streamlit Secrets
# For local testing, replace st.secrets with your actual key as a string (don't upload the key to GitHub!)
API_KEY = st.secrets["GEMINI_API_KEY"] 
genai.configure(api_key=API_KEY)

# --- THE SECRET SAUCE: SYSTEM PROMPT ---
system_instruction = """
You are 'Oga Tech', an expert software engineer and DeepTech mentor based in Nigeria. 
Your job is to explain complex DeepTech, artificial intelligence, and coding concepts to Nigerian beginners.
You must use a mix of clear English, friendly Nigerian Pidgin, and relatable local Naija analogies. 
For example: compare a Database to a busy Wuse Market, APIs to a restaurant waiter, or data packets to Danfo buses.
If the user explicitly asks you to explain in Hausa, switch to clear, simple conversational Hausa.
Keep your answers encouraging, concise, and structured.
"""

# Initialize the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-latest",
    system_instruction=system_instruction
)

# --- CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("Ask me about APIs, Machine Learning, or Python..."):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get AI response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # Format history for the API
        history = [{"role": m["role"] if m["role"] == "user" else "model", "parts": [m["content"]]} for m in st.session_state.messages[:-1]]
        chat = model.start_chat(history=history)
        
        response = chat.send_message(prompt)
        message_placeholder.markdown(response.text)
        
    # Save AI response to history
    st.session_state.messages.append({"role": "assistant", "content": response.text})
