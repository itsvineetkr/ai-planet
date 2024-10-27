from sqlalchemy import delete
from sqlalchemy.orm import Session
from database import Questions, PDFs

# Create a question
def create_question(db: Session, question: str, answer: str):
    db_question = Questions(question=question, answer=answer)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

# Retrieve all questions
def get_questions(db: Session):
    return db.query(Questions).all()

# Retrieve a question by ID
def get_question(db: Session, question_id: int):
    return db.query(Questions).filter(Questions.id == question_id).first()

# Update a question
def update_question(db: Session, question_id: int, question: str, answer: str):
    db_question = db.query(Questions).filter(Questions.id == question_id).first()
    if db_question:
        db_question.question = question
        db_question.answer = answer
        db.commit()
        db.refresh(db_question)
        return db_question
    return None

# Delete a question by ID
def delete_question(db: Session, question_id: int):
    db_question = db.query(Questions).filter(Questions.id == question_id).first()
    if db_question:
        db.delete(db_question)
        db.commit()
        return db_question
    return None

# Clear the database of all questions
def clear_database(db: Session):
    db.execute(delete(Questions))
    db.commit()

# Create a PDF data
def create_pdf_data(db: Session, filename: str):
    db_pdf = PDFs(filename=filename)
    db.add(db_pdf)
    db.commit()
    db.refresh(db_pdf)
    return db_pdf