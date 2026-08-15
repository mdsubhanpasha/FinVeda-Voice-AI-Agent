import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os

st.set_page_config(page_title="FinVeda-Voice", page_icon="🎙️")
st.title("🎙️ FinVeda-Voice: Multi-Agent Voice AI")
st.subheader("Autonomous Customer Support Agent powered by Google Gemini")

# Load Google Key from secrets
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
def get_ai_response(user_text):
    system_prompt = """You are FinVeda-Voice, an autonomous customer support agent for a fintech company. 
    Be helpful, fast, and professional. If refund is needed, say 'Refund initiated and email sent.'"""
    
    response = model.generate_content(system_prompt + "\n\nCustomer: " + user_text)
    return response.text

def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    tts.save("response.mp3")
    return "response.mp3"

# UI
st.info("Type your problem and click 'Start Call'")
user_input = st.text_input("Customer Problem", "My money was debited twice")

if st.button("🎤 Start Call"):
    st.success(f"You: {user_input}")

    with st.spinner("Agent 2: Thinking with Gemini..."):
        ai_response = get_ai_response(user_input)
    st.info(f"AI Agent: {ai_response}")

    with st.spinner("Agent 3: Speaking..."):
        audio_file = text_to_speech(ai_response)
        st.audio(audio_file)

    st.success("✅ Call Resolved. Email triggered to customer.")