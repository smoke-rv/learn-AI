import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

# Page config
st.set_page_config(page_title="AI Prompt Studio", page_icon="✨", layout="centered")

# Load environment variables
load_dotenv()

# Get API key and validate
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("❌ API key not found!")
    st.warning("Please check your `.env` file and ensure it contains: `OPENAI_API_KEY=your_key`")
    st.stop()

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Custom CSS
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #1a1f35 0%, #2d3651 100%);
    }
    
    /* Title styling */
    .gradient-title {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(135deg, #a78bfa 0%, #60a5fa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }
    
    /* Subtitle */
    .subtitle {
        text-align: center;
        color: #94a3b8;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    
    /* Text area styling */
    .stTextArea textarea {
        background-color: #1e293b !important;
        border: 1px solid #475569 !important;
        border-radius: 12px !important;
        color: #e2e8f0 !important;
        font-size: 1rem !important;
        padding: 1rem !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #a78bfa !important;
        box-shadow: 0 0 0 1px #a78bfa !important;
    }
    
    /* Button styling */
    .stButton button {
        width: 100%;
        background: linear-gradient(135deg, #a78bfa 0%, #60a5fa 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(167, 139, 250, 0.4) !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(167, 139, 250, 0.6) !important;
    }
    
    /* Response container */
    .response-container {
        margin-top: 2rem;
        padding: 1.5rem;
        background: #1e293b;
        border-radius: 12px;
        border: 1px solid #334155;
        min-height: 150px;
        max-height: 500px;
        overflow-y: auto;
    }
    
    /* Message blocks */
    .message-block {
        margin-bottom: 1.5rem;
        padding-bottom: 1.5rem;
        border-bottom: 1px solid #334155;
    }
    
    .message-block:last-child {
        border-bottom: none;
        margin-bottom: 0;
        padding-bottom: 0;
    }
    
    .user-message {
        margin-bottom: 1rem;
    }
    
    .user-label {
        font-size: 0.875rem;
        font-weight: 600;
        color: #60a5fa;
        margin-bottom: 0.5rem;
    }
    
    .user-text {
        color: #cbd5e1;
        background: #0f172a;
        padding: 0.75rem;
        border-radius: 8px;
        border-left: 3px solid #60a5fa;
    }
    
    .ai-message {
        margin-top: 1rem;
    }
    
    .ai-label {
        font-size: 0.875rem;
        font-weight: 600;
        color: #a78bfa;
        margin-bottom: 0.5rem;
    }
    
    .ai-text {
        color: #cbd5e1;
        line-height: 1.6;
        font-size: 1rem;
    }
    
    .response-empty {
        min-height: 120px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #64748b;
        font-style: italic;
    }
    
    /* Metadata badges */
    .metadata-container {
        display: flex;
        gap: 0.75rem;
        margin-top: 0.75rem;
        flex-wrap: wrap;
    }
    
    .metadata-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.4rem 0.75rem;
        background: #334155;
        border-radius: 20px;
        font-size: 0.75rem;
        color: #cbd5e1;
    }
    
    .badge-icon {
        font-size: 0.875rem;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

def get_model_response(prompt: str) -> dict:
    """
    Calls OpenAI API and returns structured response.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        content = response.choices[0].message.content
        
        return {
            "type": "text",
            "content": content,
            "metadata": {
                "model": response.model,
                "tokens": response.usage.total_tokens
            }
        }
    except Exception as e:
        raise ValueError(f"OpenAI API Error: {str(e)}")

# Initialize session state
if 'form_key' not in st.session_state:
    st.session_state.form_key = 0
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

# Main UI
st.markdown('<h1 class="gradient-title">AI Prompt Studio</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Enter your prompt and witness the magic of AI</p>', unsafe_allow_html=True)

# Form with dynamic key for reset
with st.form(key=f'prompt_form_{st.session_state.form_key}'):
    user_prompt = st.text_area("Your Prompt:", height=120, key=f"prompt_input_{st.session_state.form_key}", label_visibility="collapsed", placeholder="Enter your prompt here...")
    submit_button = st.form_submit_button(label='✨ Generate Response')

# Handle form submission
if submit_button and user_prompt:
    with st.spinner('Waiting for response from the model...'):
        try:
            response_data = get_model_response(user_prompt)
            
            # Add to conversation history
            st.session_state.conversation_history.append({
                "user_prompt": user_prompt,
                "ai_response": response_data
            })
            
            # Reset form by incrementing key
            st.session_state.form_key += 1
            st.rerun()
            
        except ValueError as e:
            st.error(f"❌ Model Error: {e}")
            st.warning("Something went wrong. Please try again.")

elif submit_button:
    st.warning("⚠️ Don't forget to enter your prompt!")

# Display conversation history
st.markdown('<div class="response-container">', unsafe_allow_html=True)

if st.session_state.conversation_history:
    # Display all messages
    for idx, message in enumerate(st.session_state.conversation_history):
        user_prompt = message["user_prompt"]
        ai_response = message["ai_response"]
        content = ai_response.get("content")
        metadata = ai_response.get("metadata", {})
        
        st.markdown(f'''
        <div class="message-block">
            <div class="user-message">
                <div class="user-label">You:</div>
                <div class="user-text">{user_prompt}</div>
            </div>
            <div class="ai-message">
                <div class="ai-label">AI Response:</div>
                <div class="ai-text">{content}</div>
                <div class="metadata-container">
                    <div class="metadata-badge">
                        <span class="badge-icon">🤖</span>
                        <span>Model: {metadata.get("model", "N/A")}</span>
                    </div>
                    <div class="metadata-badge">
                        <span class="badge-icon">🪙</span>
                        <span>Tokens: {metadata.get("tokens", "N/A")}</span>
                    </div>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
else:
    # Empty state
    st.markdown('<div class="response-empty">Your conversation will appear here...</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)