import streamlit as st
import google.generativeai as genai
import os

# 1. PAGE CONFIG
st.set_page_config(
    page_title="FinVeda-Voice: Multi-Agent Voice AI",
    page_icon="🎤",
    layout="wide"
)

# 2. SETUP API KEY
GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY", os.getenv("GOOGLE_API_KEY"))

if not GOOGLE_API_KEY:
    st.error("⚠️ GOOGLE_API_KEY not found. Please add it to Streamlit Secrets.")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)

# 3. SYSTEM PROMPT FOR AGENT
SYSTEM_PROMPT = """
You are FinVeda-Voice, an autonomous customer support agent for a fintech company.
Your job is to be empathetic, helpful, and solve customer problems quickly.
Keep responses short, clear, and professional. Max 3-4 sentences.
If you don't know, say you will escalate to a human agent.
"""

# 4. FUNCTION TO GET AI RESPONSE
@st.cache_data
def get_ai_response(user_text):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(SYSTEM_PROMPT + "\n\nCustomer: " + user_text)
        return response.text
    except Exception as e:
        return f"Sorry, I encountered an error: {e}"

# 5. UI DESIGN
st.title("🎤 FinVeda-Voice: Multi-Agent Voice AI")
st.markdown("An autonomous customer support agent powered by Google Gemini 1.5 Flash")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Customer Issue")
    user_input = st.text_area("Describe your problem:", 
                              placeholder="e.g. My money was debited twice but order failed",
                              height=150)
    
    if st.button("Start Call", type="primary"):
        if user_input:
            with st.spinner("AI Agent is thinking..."):
                ai_response = get_ai_response(user_input)
            
            st.subheader("Agent Response")
            st.success(ai_response)
        else:
            st.warning("Please enter your issue first.")

with col2:
    st.subheader("Try Examples")
    examples = [
        "My money was debited twice",
        "UPI payment failed but amount deducted", 
        "I can't login to my account"
    ]
    for ex in examples:
        if st.button(ex):
            st.session_state.user_input = ex
            st.rerun()

st.markdown("---")
st.caption("Built with Streamlit + Python + Google Gemini | FinVeda-Voice v1.0")