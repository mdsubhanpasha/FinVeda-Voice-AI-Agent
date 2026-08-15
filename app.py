import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="FinVeda-Voice: AI Support Agent", page_icon="🎤", layout="wide")

try:
    OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=OPENROUTER_API_KEY)
except:
    st.error("⚠️ OPENROUTER_API_KEY not found. Please add it to Streamlit Secrets.")
    st.stop()

SYSTEM_PROMPT = """You are FinVeda-Voice, an autonomous customer support agent for a fintech company. Be empathetic, helpful, and solve problems quickly. Keep responses short, clear, and professional. Max 3-4 sentences."""

def get_ai_response(user_text):
    try:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(st.session_state.messages)
        messages.append({"role": "user", "content": user_text})

        response = client.chat.completions.create(
            model="google/gemini-flash-1.5", # FIXED - NO :free
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Sorry, I encountered an error: {e}. Please try again."

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🎤 FinVeda-Voice")
st.markdown("An autonomous customer support agent powered by **OpenRouter + Gemini 1.5 Flash**")

col1, col2 = st.columns([3, 1])

with col1:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]): st.markdown(message["content"])

    if prompt := st.chat_input("Describe your problem..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("AI Agent is thinking..."): response = get_ai_response(prompt)
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

with col2:
    st.subheader("Try These Issues")
    examples = ["My money was debited twice", "UPI payment failed but amount deducted", "I can't login to my account", "Transaction stuck for 2 hours", "Wrong amount deducted", "Refund not received yet", "My card is blocked", "KYC verification failed", "App is crashing on payment", "I was charged extra fee"]
    for ex in examples:
        if st.button(ex, use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": ex})
            with st.spinner("AI Agent is thinking..."): response = get_ai_response(ex)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.markdown("---")
st.caption("Built with Streamlit + Python + OpenRouter | FinVeda-Voice v1.4")