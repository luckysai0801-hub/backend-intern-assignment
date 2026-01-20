from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import Base, engine
from . import models, schemas, auth

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Backend Intern Assignment API", version="1.0")

@app.post("/api/v1/register")
def register(user: schemas.UserCreate, db: Session = Depends(auth.get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=auth.hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully"}

@app.post("/api/v1/login")
def login(user: schemas.UserLogin, db: Session = Depends(auth.get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not auth.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = auth.create_access_token({"user_id": db_user.id})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/api/v1/tasks")
def create_task(
    task: schemas.TaskCreate,
    current_user=Depends(auth.get_current_user),
    db: Session = Depends(auth.get_db)
):
    new_task = models.Task(
        title=task.title,
        description=task.description,
        owner_id=current_user.id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@app.get("/api/v1/tasks")
def get_tasks(
    current_user=Depends(auth.get_current_user),
    db: Session = Depends(auth.get_db)
):
    return db.query(models.Task).filter(models.Task.owner_id == current_user.id).all()
