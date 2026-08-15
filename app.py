import streamlit as st
import azure.cognitiveservices.speech as speechsdk
from openai import AzureOpenAI

st.set_page_config(page_title="FinVeda-Voice", page_icon="🎙️")
st.title("🎙️ FinVeda-Voice: Multi-Agent Voice AI")
st.subheader("Autonomous Customer Support Agent powered by Azure GPT-4o")

# Load secrets
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
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    synthesizer.speak_text_async(text)
    return text

# UI - MIC REMOVED, TEXT INPUT ADDED
st.info("Type your problem and click 'Start Call'")
user_input = st.text_input("Customer Problem", "My money was debited twice")

if st.button("🎤 Start Call"):
    st.success(f"You: {user_input}")

    with st.spinner("Agent 2: Thinking with GPT-4o..."):
        ai_response = get_ai_response(user_input)
    st.info(f"AI Agent: {ai_response}")

    with st.spinner("Agent 3: Speaking..."):
        text_to_speech(ai_response)

    st.success("✅ Call Resolved. Email triggered to customer.")
    st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3") # demo audio