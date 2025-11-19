import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# Load the environment variables from your .env file
load_dotenv()

# 1. Initialize the ChatOpenAI client
llm = ChatOpenAI(
    # The 'model_name' must match the model you are serving with vLLM
    model_name="Qwen/Qwen2.5-32B-Instruct", 
    
    # The base_url and api_key are automatically read from the
    # OPENAI_API_BASE and OPENAI_API_KEY environment variables.
    # You could also set them explicitly here:
    # openai_api_base="http://localhost:8000/v1",
    # openai_api_key="dummy",
    
    temperature=0.7,
    max_tokens=32700
)

# 2. Define your prompt (using the correct chat format)
messages = [
    HumanMessage(content="reverse the word: Onomatopoeia, give an EXACT answer")
]

# 3. Invoke the model
print("Sending request to vLLM...")
response = llm.invoke(messages)

print("\nResponse from Qwen:")
print(response.content)

