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
    return db.query(models.Model).order_by(models.Model.id.asc()).offset(skip).limit(limit).all()

def delete_model(db: Session, model_id: int):
    query = db.query(models.Model).filter(models.Model.id == model_id)
    model = query.first()
    if model:
        query.delete()
        db.commit()
        return model
    return None

def get_selected_model(db: Session):
    return db.query(models.Model).filter(models.Model.selected == True).first()

def select_model(db: Session, model_id: int):
    previous_selected_model = get_selected_model(db)
    if previous_selected_model:
        previous_selected_model.selected = None
        db.commit()

    selected_model = get_model(db, model_id)
    selected_model.selected = True
    db.commit()

    return selected_model