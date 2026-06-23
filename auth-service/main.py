from fastapi import FastAPI, Depends 
from prometheus_fastapi_instrumentator import Instrumentator
from sqlalchemy.orm import Session

from security import (
    create_access_token, 
    verify_token, 
    hash_password,
    verify_password )

from database import engine, get_db
from models import Base,User
from schemas import UserCreate, UserLogin

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="GreenOps Auth Service",
    description="Service d'authentification de GreenOps",
    version="1.0.0"
) 

Instrumentator().instrument(app).expose(app)

@app.get("/", tags=["Health"])
def root():
    return{"message": "Auth Service Runing"}

@app.post("/register", tags=["Authentification"])
def register(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(
        User.name == user.name
        ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Nom d‘utilisateur déjà utilisé"
     )

    new_user = User(
        username=user.username,
        password=hash_password(user.password)
)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)


    return {
     "message": "Utilisateur créé",
     "id": new_user.id
    }

@app.post("/login", tags=["Authentification"])
def login(user: UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(
        User.username == user.username
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="Utilisateur introuvable"
        )

    if not verify_password(
        user.password, db_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Mot de passe incorrect"
        )

    token = create_access_token(
        {"sub": db_user.username}
    )

    return {
        "message": "Connexion réussie",
        "access_token": token
    }

@app.get("/profile", tags=["Authentification"])
def profile(token: str):

    payload = verify_token(token)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Token invalide"
        )

    return {
        "username": payload["sub"]
    }

@app.get("/users", tags=["Users"])
def get_users(db: Session = Depends(get_db)):

    users = db.query(User).all()

    return [
        {
            "id": user.id,
            "username": user.username
        }
        for user in users
    ]

