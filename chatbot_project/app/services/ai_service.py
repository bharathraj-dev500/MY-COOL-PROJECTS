# app/services/ai_service.py

import os
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

# Set your OpenAI API Key (IMPORTANT)
os.environ["OPENAI_API_KEY"] = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
 # Replace with your API Key

# Create the ChatGPT model
chat_model = ChatOpenAI(
    model="gpt-3.5-turbo",  # Correct field name: model
    temperature=0.7
)

# Setup memory for storing conversation history
memory = ConversationBufferMemory()

# Setup conversation chain
conversation = ConversationChain(
    llm=chat_model,
    memory=memory,
    verbose=True
)

def get_ai_response(question: str) -> str:
    try:
        result = conversation.invoke({"input": question})
        return result["response"]
    except Exception as e:
        return f"Error: {str(e)}"  # Return error message to help with debugging
