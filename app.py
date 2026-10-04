import os
import smtplib
from email.mime.text import MIMEText
import streamlit as st
from google import genai
from google.genai import types

from prompts import SYSTEM_PROMPT, SUMMARY_REQUEST_PROMPT

# Central model definition
MODEL_NAME = "gemini-2.5-flash"

st.set_page_config(
    page_title="Snap & Study AI",
    page_icon="📚",
    layout="centered"
)


# Custom CSS for a clean, minimal UI layout
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .tagline {
        font-size: 1.1rem;
        color: #6c757d;
        margin-bottom: 1.5rem;
    }
    .stChatMessage {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)


# Gemini client is cached to avoid re-initializing on every Streamlit rerun.
@st.cache_resource
def get_gemini_client(api_key: str):
    return genai.Client(api_key=api_key)


def get_secret(key: str, default: str = "") -> str:
    """Safely retrieve a secret key from st.secrets or environment variables without raising StreamlitSecretNotFoundError."""
    try:
        if key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass
    return os.getenv(key, default)


def get_api_key():
    """Retrieve Gemini API key from secrets or environment variables."""
    return get_secret("GEMINI_API_KEY")


def init_chat_session(client):
    """Start a fresh Gemini chat session with the tutor system prompt."""
    return client.chats.create(
        model=MODEL_NAME,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT
        )
    )


def send_email(to_address: str, subject: str, body: str):
    """Send study notes through Gmail SMTP using SSL."""
    gmail_address = get_secret("GMAIL_ADDRESS")
    gmail_password = get_secret("GMAIL_APP_PASSWORD")

    if not gmail_address or not gmail_password:
        return False, "Gmail credentials not configured. Please add GMAIL_ADDRESS and GMAIL_APP_PASSWORD to .streamlit/secrets.toml."

    try:
        msg = MIMEText(body, "plain", "utf-8")
        msg["Subject"] = subject
        msg["From"] = f"Snap & Study AI <{gmail_address}>"
        msg["To"] = to_address

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(gmail_address, gmail_password)
            server.send_message(msg)

        return True, f"Study notes successfully emailed to {to_address}!"
    except Exception as error:
        return False, f"Email delivery failed: {str(error)}"


def generate_email_summary():
    """Generate study notes from the chat history and send them to the student."""
    if not st.session_state.messages:
        st.warning("No study conversation found to summarize yet.")
        return

    with st.spinner("Generating detailed study notes for email..."):
        try:
            # Ask Gemini to summarize the session history
            response = st.session_state.chat.send_message(SUMMARY_REQUEST_PROMPT)
            summary_text = response.text

            subject = f"📚 Snap & Study AI — Study Notes for {st.session_state.name}"
            success, message = send_email(
                to_address=st.session_state.email,
                subject=subject,
                body=summary_text
            )

            if success:
                st.success(message)
            else:
                st.error(message)
        except Exception as error:
            st.error(f"Failed to generate study summary: {str(error)}")


# -----------------------------------------------------------------------------
# ONBOARDING FLOW
# -----------------------------------------------------------------------------
if "onboarded" not in st.session_state:
    st.session_state.onboarded = False

if not st.session_state.onboarded:
    st.markdown("<div class='main-header'>📚 Snap & Study AI</div>", unsafe_allow_html=True)
    st.markdown("<div class='tagline'>Upload it. Understand it. Master it.</div>", unsafe_allow_html=True)
    st.divider()

    st.subheader("Welcome! Let's set up your profile")
    st.write("Enter your details to start your AI-powered study session.")

    with st.form("onboarding_form"):
        name_input = st.text_input("Your Name", placeholder="e.g. Alex Student")
        email_input = st.text_input("Your Email", placeholder="e.g. alex@example.com")
        submitted = st.form_submit_button("Start Studying 🚀", use_container_width=True)

        if submitted:
            if not name_input.strip():
                st.error("Please enter your name.")
            elif not email_input.strip() or "@" not in email_input:
                st.error("Please enter a valid email address.")
            else:
                api_key = get_api_key()
                if not api_key:
                    st.error("Gemini API Key is missing. Please configure GEMINI_API_KEY in secrets.toml or environment variables.")
                else:
                    try:
                        client = get_gemini_client(api_key)
                        chat_session = init_chat_session(client)

                        st.session_state.name = name_input.strip()
                        st.session_state.email = email_input.strip()
                        st.session_state.messages = []
                        st.session_state.chat = chat_session
                        st.session_state.onboarded = True
                        st.rerun()
                    except Exception as error:
                        st.error(f"Could not connect to Gemini API: {str(error)}")
    st.stop()


# -----------------------------------------------------------------------------
# MAIN APPLICATION INTERFACE
# -----------------------------------------------------------------------------
api_key = get_api_key()
if not api_key:
    st.error("Gemini API Key missing. Please check your configuration.")
    st.stop()

# Ensure chat session exists
if "chat" not in st.session_state or st.session_state.chat is None:
    try:
        client = get_gemini_client(api_key)
        st.session_state.chat = init_chat_session(client)
    except Exception as error:
        st.error(f"Failed to initialize Gemini session: {str(error)}")
        st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []


# SIDEBAR
with st.sidebar:
    st.title("📚 Snap & Study AI")
    st.caption("Upload it. Understand it. Master it.")
    st.divider()

    st.markdown(f"**Student:** {st.session_state.name}")
    st.markdown(f"**Email:** {st.session_state.email}")
    st.divider()

    st.subheader("🎯 Study Mode")
    study_mode = st.selectbox(
        "Choose focus mode:",
        options=[
            "💬 Direct Answer",
            "📖 Explain Concept",
            "🧩 Solve Step-by-Step",
            "💻 Explain Code & Fix Errors",
            "🧠 Simplify (Like I'm 5)",
            "📝 Generate Short Notes",
            "🎯 Interview Questions",
            "📚 Generate Examples",
            "🔄 Explain Again (Different Way)"
        ],
        help="Selecting a study mode tailors how Gemini structures its responses."
    )

    st.divider()

    if st.button("📧 Email Study Notes", use_container_width=True, type="secondary"):
        generate_email_summary()

    if st.button("🗑️ Clear Chat", use_container_width=True):
        try:
            client = get_gemini_client(api_key)
            st.session_state.chat = init_chat_session(client)
            st.session_state.messages = []
            st.toast("Chat history cleared!", icon="🧹")
            st.rerun()
        except Exception as error:
            st.error(f"Failed to reset chat: {str(error)}")


# HEADER
st.markdown("<div class='main-header'>📚 Snap & Study AI</div>", unsafe_allow_html=True)
st.caption("Ask questions, upload handwritten notes, textbook photos, code, or diagrams for instant help.")


# RENDER CHAT HISTORY
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if "image_bytes" in msg and msg["image_bytes"]:
            st.image(msg["image_bytes"], caption="Uploaded Study Material", use_container_width=True)
        if msg.get("content"):
            st.markdown(msg["content"])


# CHAT INPUT WITH FILE UPLOAD
user_input = st.chat_input(
    "Ask a study question or upload an image...",
    accept_file=True,
    file_type=["jpg", "jpeg", "png", "webp"]
)

if user_input:
    prompt_text = user_input.text.strip() if hasattr(user_input, "text") and user_input.text else ""
    files = user_input.files if hasattr(user_input, "files") and user_input.files else []

    if not prompt_text and not files:
        st.warning("Please enter a question or upload an image.")
        st.stop()

    # Apply study mode modifier if active
    final_prompt = prompt_text
    if study_mode != "💬 Direct Answer":
        mode_prefix = f"[{study_mode}] "
        final_prompt = mode_prefix + prompt_text if prompt_text else f"Please perform: {study_mode}"

    parts = []
    image_bytes_to_store = None

    # Handle image attachment
    if files:
        uploaded_file = files[0]
        image_bytes = uploaded_file.getvalue()
        image_bytes_to_store = image_bytes

        image_part = types.Part.from_bytes(
            data=image_bytes,
            mime_type=uploaded_file.type
        )
        parts.append(image_part)

        # Default prompt for image if user didn't type text
        if not final_prompt:
            final_prompt = "Analyze this study material image and explain it clearly step by step."

    if final_prompt:
        parts.append(final_prompt)

    # Store user message in display history
    st.session_state.messages.append({
        "role": "user",
        "content": prompt_text if prompt_text else "Uploaded an image for analysis.",
        "image_bytes": image_bytes_to_store
    })

    # Render immediate user message UI
    with st.chat_message("user"):
        if image_bytes_to_store:
            st.image(image_bytes_to_store, caption="Uploaded Study Material", use_container_width=True)
        if prompt_text:
            st.markdown(prompt_text)

    # Call Gemini & stream/render response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing and thinking..."):
            try:
                response = st.session_state.chat.send_message(parts)
                assistant_reply = response.text

                st.markdown(assistant_reply)

                # Store assistant response in history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": assistant_reply
                })
            except Exception as error:
                error_msg = f"Sorry, I encountered an error processing your request: {str(error)}"
                st.error(error_msg)
