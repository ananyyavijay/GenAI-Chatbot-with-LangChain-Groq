# GenAI Chatbot using LangChain

A conversational AI chatbot built using LangChain and an LLM API to generate context-aware responses. Supports different response modes using prompt-based instructions.

## Features
- Context-aware conversations using message history  
- Multiple response modes (angry, happy, sad)  
- Prompt-based behavior control  
- Continuous chat interaction  

## Tech Stack
- Python 
- LangChain  
- LLM API (Groq / OpenAI)

## How It Works
- Uses system prompts to define chatbot behavior  
- Maintains conversation using message objects  
- Processes user input in a loop and generates responses via LLM  

## Status
🚧 Under development – improving memory handling, prompts, and response quality  

## Run Locally
```bash
pip install -r requirements.txt
python ui_chatbot.py
