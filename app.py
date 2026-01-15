import uvicorn 
from fastapi import FastAPI, Request
from src.graphs.graph_builder import GraphBuilder
from src.llms.groq_llm import GroqLLM
from src.states.blog_state import Blog

import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

langsmith_api_key = os.getenv("LANGSMITH_API_KEY")

## APIs

@app.post("/blogs")
async def create_blogs(request: Request):
    data = await request.json()
    topic = data.get("topic", "")

    ## Get LLM Object
    groqllm = GroqLLM()
    llm = groqllm.get_llm()
    
    ## Get the Graph Object
    graph_builder = GraphBuilder(llm)
    
    state = None
    
    if topic:
            graph = graph_builder.setup_graph(usecase="topic")
            state = graph.invoke({"topic": topic, "current_language": "en", "blog": Blog(title="", content="")})
            # state = graph.invoke({"topic": topic})

    return {"data": state}


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
