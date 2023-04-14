from tempfile import NamedTemporaryFile

from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from . import crud, models, schemas
from .database import SessionLocal, engine
from paddel.enums import Side, Gender
from paddel.preprocessing.input.features import extract_video_features
from paddel import settings

models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Paddel",
    description="Documentation for the API for the PaDDeL website.",
    version="0.1",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User, tags=["users"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User], tags=["users"])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db=db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User, tags=["users"])
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/predict")
def obtain_prediction(
    video_hand: Side = Form(),
    dominant_hand: Side = Form(),
    sex: Gender = Form(),
    age: int = Form(),
    video: UploadFile = File(),
):
    file = NamedTemporaryFile()
    file_path = file.name

    contents = video.file.read()
    with open(file_path, "wb") as f:
        f.write(contents)

    (
        classic_features,
        fresh_features,
        detection_time,
    ) = extract_video_features(file_path)

    if detection_time < settings.min_detection_seconds:
        raise HTTPException(
            status_code=422, detail="Not enough hand poses detected in provided video."
        )

    return classic_features.to_dict()
