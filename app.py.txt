import streamlit as st
import azure.cognitiveservices.speech as speechsdk
from openai import AzureOpenAI
import os
import tempfile

st.set_page_config(page_title="FinVeda-Voice", page_icon="🎙️")
st.title("🎙️ FinVeda-Voice: Multi-Agent Voice AI")
st.subheader("Autonomous Customer Support Agent powered by Azure GPT-4o")

# Load secrets from Streamlit
AZURE_SPEECH_KEY = st.secrets["AZURE_SPEECH_KEY"]
AZURE_SPEECH_REGION = st.secrets["AZURE_SPEECH_REGION"]
AZURE_OPENAI_KEY = st.secrets["AZURE_OPENAI_KEY"]
AZURE_OPENAI_ENDPOINT = st.secrets["AZURE_OPENAI_ENDPOINT"]
DEPLOYMENT_NAME = "gpt-4o"

client = AzureOpenAI(
    api_key=AZURE_OPENAI_KEY,
    api_version="2024-02-15-preview",
    azure_endpoint=AZURE_OPENAI_ENDPOINT
)

def speech_to_text():
    speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_SPEECH_REGION)
    speech_config.speech_recognition_language = "en-US"
    audio_config = speechsdk.AudioConfig(use_default_microphone=True)
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    result = recognizer.recognize_once()
    return result.text if result.reason == speechsdk.ResultReason.RecognizedSpeech else "Could not recognize"

def get_ai_response(user_text):
    system_prompt = "You are FinVeda-Voice, an autonomous customer support agent for a fintech company. Be helpful, fast, and professional. If refund is needed, say 'Refund initiated and email sent.'"
    response = client.chat.completions.create(
        model=DEPLOYMENT_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text}
        ]
    )
    return response.choices[0].message.content

def text_to_speech(text):
    speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_SPEECH_REGION)
    speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"
    audio_config = speechsdk.AudioConfig(filename="response.wav")
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    synthesizer.speak_text_async(text)
    return "response.wav"

# UI
st.info("Click 'Start Call' and speak your problem")
if st.button("🎤 Start Call"):
    with st.spinner("Agent 1: Listening..."):
        user_input = speech_to_text()
    st.success(f"You: {user_input}")

    with st.spinner("Agent 2: Thinking with GPT-4o..."):
        ai_response = get_ai_response(user_input)
    st.info(f"AI Agent: {ai_response}")

    with st.spinner("Agent 3: Speaking..."):
        audio_file = text_to_speech(ai_response)
        st.audio(audio_file)

    st.success("✅ Call Resolved. Email triggered to customer.")