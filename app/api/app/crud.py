from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    query = db.query(models.User).filter(models.User.id == user_id)
    user = query.first()
    if user:
        query.delete()
        db.commit()
        return user
    return None


def add_model(db: Session, model_name: str, path: str):
    db_model = models.Model(name=model_name, path=path)
    db.add(db_model)
    db.commit()
    return db_model

def get_model_by_name(db: Session, name: str):
    return db.query(models.Model).filter(models.Model.name == name).first()

def get_model(db: Session, model_id: int):
    return db.query(models.Model).filter(models.Model.id == model_id).first()

def get_models(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Model).offset(skip).limit(limit).all()
