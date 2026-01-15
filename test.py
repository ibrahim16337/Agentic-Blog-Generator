import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
load_dotenv()

print("CWD:", os.getcwd())



groq_api_key =  os.getenv("GROQ_API_KEY")
print(groq_api_key)