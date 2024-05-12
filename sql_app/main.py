from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.post("/items/", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db=db, item=item)

@app.get("/users/", response_model=list[schemas.User])
def read_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_all_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/items/", response_model=list[schemas.Item])
def read_all_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.read_all_items(db, skip=skip, limit=limit)
    return items

@app.get("/users/{user_id}/items/", response_model=list[schemas.Item])
def read_items_by_user(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items_by_user_id(db, user_id=user_id, skip=skip, limit=limit)
    return items

@app.get("/items/{item_id}", response_model=schemas.Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item_by_id(db, item_id=item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put("/items/{item_id}", response_model=schemas.Item)
def update_item(item_id: int, item_update: schemas.ItemUpdate, db: Session = Depends(get_db)):
    updated_item = crud.update_item(db=db, item_id=item_id, item_update=item_update)
    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item

@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    updated_user = crud.update_user(db=db, user_id=user_id, user_update=user_update)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@app.delete("/items/{item_id}", response_model=schemas.Item)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.delete_item(db, item_id=item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.delete_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
