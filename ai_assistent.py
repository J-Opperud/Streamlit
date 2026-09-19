import os
import streamlit as st
from openai import OpenAI



# Page configuration
# -------------------------------------------------------
st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="wide"
    )



# Context options
# -------------------------------------------------------
CONTEXT_OPTIONS = {
    "Include Python expertise": (
        "You are an expert Python developer. "
        "Provide Python examples when appropriate and follow modern Python best practices."
        ),
    "Include web development context": (
        "You are knowledgeable about web development, including HTML, CSS, "
        "JavaScript, APIs, frontend frameworks, and backend development."
        ),
    "Include AI/ML context": (
        "You are knowledgeable about artificial intelligence and machine learning. "
        "Explain AI/ML concepts clearly and provide practical examples when useful."
        ),
    }



# Session state
# -------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []



# Sidebar
# -------------------------------------------------------
with st.sidebar:
    st.title(" Assistant Settings")

    system_prompt = st.text_area(
        "System Prompt",
        value=(
            "You are a helpful AI assistant. "
            "Give clear, accurate, and concise answers."
            ),
        height=150,
        )

    st.subheader("Context")

    selected_context = []

    for context_name in CONTEXT_OPTIONS:
        checked = st.checkbox(context_name)

        if checked:
            selected_context.append(context_name)

    st.divider()

    if st.button(" Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    # Check whether an OpenAI API key exists.
    api_key = os.getenv("OPENAI_API_KEY")

    if api_key:
        st.success("OpenAI API key detected")
    else:
        st.info("No API key detected — using mock responses")



# Build the complete system prompt
# -------------------------------------------------------
full_system_prompt = system_prompt

if selected_context:
    full_system_prompt += "\n\nAdditional context:\n"

    for context_name in selected_context:
        full_system_prompt += (
            f"- {context_name}: {CONTEXT_OPTIONS[context_name]}\n"
            )



# Main interface
# -------------------------------------------------------
st.title(" AI Assistant")
st.caption("Customizable AI chat with history and context controls")



# Re-render chat history
# -------------------------------------------------------
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"]
        )



# Chat input
# -------------------------------------------------------
user_input = st.chat_input("Ask me anything...")


if user_input:

    # Add user message to history
    st.session_state.messages.append(
            {
            "role": "user",
            "content": user_input,
            }
        )

    # Immediately display the user's message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate assistant response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            
            # Real OpenAI API
            # -----------------------------------------------
            if api_key:

                try:
                    client = OpenAI(api_key=api_key)

                    response = client.responses.create(
                        model="gpt-5.6-luna",
                        instructions=full_system_prompt,
                        input=st.session_state.messages,
                        )

                    assistant_response = response.output_text

                except Exception as e:
                    assistant_response = (
                        f" OpenAI API error: {str(e)}"
                        )

            
            # Mock response if no API key
            # -----------------------------------------------
            else:

                context_text = (
                    ", ".join(selected_context)
                    if selected_context
                    else "no additional context"
                    )

                assistant_response = (
                    "### Mock AI Response\n\n"
                    f"You asked: **{user_input}**\n\n"
                    f"**System prompt:** {system_prompt}\n\n"
                    f"**Selected context:** {context_text}\n\n"
                    "This is a mock response because no "
                    "`OPENAI_API_KEY` was found. Add an OpenAI API "
                    "key to generate real AI responses."
                    )

            st.markdown(assistant_response)

    # Save assistant response
    st.session_state.messages.append(
            {
            "role": "assistant",
            "content": assistant_response,
            }
        )
