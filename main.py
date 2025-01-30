from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from services.qa_service import get_answer, preload_models  # Import preload function

# FastAPI app definition with lifespan event handler
app = FastAPI(lifespan=preload_models)

# Pydantic model for incoming request
class QuestionRequest(BaseModel):
    question: str

# Serve static files (CSS, JS, HTML)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Root endpoint to serve the chatbot interface (index.html)
@app.get("/", response_class=HTMLResponse)
async def root():
    with open("static/index.html", "r") as f:
        return HTMLResponse(content=f.read())

@app.post("/get-answer/")
async def get_answer_endpoint(req: QuestionRequest):
    answer = get_answer(req.question)
    return {"answer": answer}
