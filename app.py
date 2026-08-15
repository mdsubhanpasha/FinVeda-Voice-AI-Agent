import streamlit as st
from openai import OpenAI

# 1. OPENROUTER CLIENT SETUP
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=OPENROUTER_API_KEY,
)

# 2. FUNCTION TO GET AI RESPONSE
def get_ai_response(user_text):
    try:
        response = client.chat.completions.create(
            model="google/gemini-2.0-flash-exp:free", # OpenRouter lo Gemini free model
            messages=[
                {"role": "system", "content": "You are FinVeda-Voice, an autonomous customer support agent for a fintech company. Be helpful and short."},
                {"role": "user", "content": user_text}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

# 3. REST OF YOUR STREAMLIT UI CODE SAME UNTUNDI
st.title("🎤 FinVeda-Voice")
user_input = st.text_area("Describe your problem:")
if st.button("Start Call"):
    if user_input:
        with st.spinner("AI Agent is thinking..."):
            ai_response = get_ai_response(user_input)
        st.success(ai_response)