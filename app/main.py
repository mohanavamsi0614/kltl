from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from app.langchain_integration.prompt_processor import PromptProcessor

app = FastAPI(title="ANALYTICS ENGINE API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

prompt_processor = PromptProcessor()

class PromptRequest(BaseModel):
    prompt: str

@app.post("/prompt")
async def process_prompt(request: PromptRequest):
    try:
        result = prompt_processor.process(request.prompt)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
