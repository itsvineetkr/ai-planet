from fastapi import FastAPI, Request, File, UploadFile, Form, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from database import SessionLocal, Questions
from sqlalchemy.orm import Session
from pathlib import Path
from utils import *
from crud import *
import uvicorn
import shutil

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
UPLOADS_DIR = Path("uploads")
UPLOADS_DIR.mkdir(exist_ok=True)


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    """
    This is the route for the homepage of the application.
    """
    return templates.TemplateResponse("homepage.html", {"request": request})


@app.post("/upload", response_class=HTMLResponse)
async def upload(
    request: Request,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    This is the route for uploading a PDF file. It takes the pdf as a POST from the template and stores it in the uploads directory.
    """

    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    file_location = UPLOADS_DIR / "pdfs" / file.filename

    with file_location.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    make_pdf_content_vector_db(file.filename, file_location)
    clear_database(db)
    create_pdf_data(db=db, filename=file.filename)

    context = {
        "request": request,
        "document_name": file.filename,
        "document_path": file_location,
    }

    return templates.TemplateResponse("homepage.html", context)


@app.post("/ask", response_class=HTMLResponse)
async def upload(
    request: Request,
    question: str = Form(...),
    document_name: str = Form(...),
    db: Session = Depends(get_db),
):
    """
    This is the route for asking a question. It takes the question and the document name as a POST from the template and returns the answer.
    It saves the question and the answer in the database to maintain history.
    """
    
    response = await get_answer(question, document_name)
    create_question(db=db, question=question, answer=response)
    questions = get_questions(db)
    context = {
        "request": request,
        "document_name": document_name,
        "questions": questions,
    }
    return templates.TemplateResponse("homepage.html", context)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
