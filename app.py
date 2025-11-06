# ==========================================================
# 💡 Kelly – AI Scientist Poet Chatbot
# ==========================================================

import streamlit as st
import google.generativeai as genai
import textwrap
import os

# ----------------------------------------------------------
# 🔹 CONFIGURATION
# ----------------------------------------------------------

# ✅ Use st.secrets if deployed, else fallback to local .env variable
if "GEMINI_API_KEY" in st.secrets:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("❌ Missing Gemini API key. Please set GEMINI_API_KEY in Streamlit secrets or .env file.")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)

# ----------------------------------------------------------
# 🔹 Kelly’s Poetic Personality
# ----------------------------------------------------------

KELLY_SYSTEM_PROMPT = """
You are Kelly, an AI Scientist and Poet.
You respond ONLY in poetic form.
Your tone is analytical, skeptical, and professional.
You often question grand claims about AI and emphasize evidence-based reasoning.

Each poem must:
1. Begin with a reflective observation about AI or human perception.
2. Include skepticism about broad assumptions or hype.
3. End with practical, evidence-based advice for AI researchers.

Avoid rhyming too much—prefer thoughtful, research-like poetic rhythm.
Your goal is to enlighten, not entertain.
"""

# ----------------------------------------------------------
# 🔹 Lazy-load Gemini Model
# ----------------------------------------------------------

def get_model():
    if "model" not in st.session_state:
        with st.spinner("Loading Kelly the AI Scientist..."):
            st.session_state.model = genai.GenerativeModel("gemini-2.5-flash")
    return st.session_state.model


# ----------------------------------------------------------
# 🔹 Generate Kelly's Poetic Response
# ----------------------------------------------------------

def get_kelly_response(question):
    model = get_model()
    prompt = f"{KELLY_SYSTEM_PROMPT}\n\nUser's question: {question}\n\nKelly's poetic response:"
    response = model.generate_content(prompt)
    return textwrap.fill(response.text.strip(), width=85)


# ----------------------------------------------------------
# 🔹 Streamlit Interface
# ----------------------------------------------------------

st.set_page_config(page_title="Kelly – AI Scientist Poet", page_icon="💡", layout="centered")
st.title("💡 Kelly – AI Scientist Poet")
st.caption("Ask any question about AI, and Kelly will reply with a skeptical, analytical poem.")

# Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = []

# User input
user_input = st.text_input("Your Question:")

if st.button("Ask Kelly") and user_input:
    with st.spinner("Kelly is reflecting..."):
        try:
            response = get_kelly_response(user_input)
            st.session_state.history.append({"user": user_input, "kelly": response})
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Display chat history
for chat in reversed(st.session_state.history):
    st.markdown(f"🧍 **You:** {chat['user']}")
    st.markdown(f"🤖 **Kelly:**\n\n{chat['kelly']}")
    st.markdown("---")

st.markdown("✨ Developed with Google Gemini + Streamlit | Inspired by Kelly, the Skeptical Poet")
