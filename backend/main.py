import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from src.agent.advanced_agent import run_hakuba_agent


app = FastAPI(title="ROSSI STAR AI BACKEND")

print("Start Backend...")
agent_app = run_hakuba_agent()
print("Backend Started!")


class ChatRequest(BaseModel):
    query: str
    thread_id: str


class ChatResponse(BaseModel):
    answer: str


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    config = {"configurable": {"thread_id": request.thread_id}}
    inputs = {"messages": [("user", request.query)]}

    try:
        result = agent_app.invoke(inputs, config=config)
        final_answer = result["messages"][-1].content
        return ChatResponse(answer=final_answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))