AI Assistant
## overview
A Streamlit chat application that supports customizable system prompts, context controls, chat history, and optional OpenAI API integration.

Using the OpenAI API

The app can use the real OpenAI API when an API key is provided.

## Install dependencies
pip install -r requirements.txt

## Create an OpenAI API key

Create an API key from the OpenAI API platform and keep it private.

## Set your API key

Windows PowerShell:

$env:OPENAI_API_KEY="your-api-key-here"


macOS/Linux:

export OPENAI_API_KEY="your-api-key-here"

## Run the application
streamlit run ai_assistant.py


When OPENAI_API_KEY is detected, the application sends the system prompt, selected context, and chat history to OpenAI to generate responses.

If no API key is available, the application uses the built-in mock response instead.
