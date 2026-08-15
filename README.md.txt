# FinVeda-Voice: Multi-Agent Voice AI Customer Support

Autonomous Voice AI Agent that handles customer calls end-to-end using Azure GPT-4o.

## Architecture: 3-Agent System
1. **STT Agent**: Azure Speech SDK for real-time Speech-to-Text
2. **Brain Agent**: Azure GPT-4o for reasoning and problem solving
3. **TTS + Action Agent**: Azure Neural Voice + Automated Email

## Demo
Customer: "My money was debited twice"
AI: "Refund initiated sir. Check your email."

## Tech Stack
Python, Streamlit, Azure OpenAI, Azure Speech SDK

## How to Run
1. Clone repo
2. `pip install -r requirements.txt`
3. Add Azure keys to `.streamlit/secrets.toml`
4. `streamlit run app.py`

Built for the future of Customer Support. #VoiceAI #MultiAgent #Azure
