from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas, database

# Create tables if they don't exist (only once at startup)
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Server is running!"}

# Create a single pet (existing endpoint)
@app.post("/pets/", response_model=schemas.Pet)
def create_pet(pet: schemas.PetCreate, db: Session = Depends(get_db)):
    return crud.create_pet(db=db, pet=pet)

# Create multiple pets (new endpoint)
@app.post("/pets/create_multiple/", response_model=list[schemas.Pet])
def create_pets(pets: list[schemas.PetCreate], db: Session = Depends(get_db)):
    created_pets = []
    for pet in pets:
        try:
            created_pet = crud.create_pet(db=db, pet=pet)
            created_pets.append(created_pet)
        except Exception as e:
            # Log the exception or handle accordingly
            raise HTTPException(status_code=400, detail=f"Error creating pet: {str(e)}")
    return created_pets

# Get all pets with pagination
@app.get("/pets/", response_model=list[schemas.Pet])
def read_pets(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    pets = crud.get_pets(db, skip=skip, limit=limit)
    return pets

# Get a specific pet by ID
@app.get("/pets/{pet_id}", response_model=schemas.Pet)
def read_pet(pet_id: int, db: Session = Depends(get_db)):
    db_pet = crud.get_pet(db, pet_id=pet_id)
    if db_pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")
    return db_pet

# Update an existing pet
@app.put("/pets/{pet_id}", response_model=schemas.Pet)
def update_pet(pet_id: int, pet: schemas.PetCreate, db: Session = Depends(get_db)):
    db_pet = crud.update_pet(db, pet_id=pet_id, pet=pet)
    if db_pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")
    return db_pet

# Delete a pet by ID
@app.delete("/pets/{pet_id}", response_model=schemas.Pet)
def delete_pet(pet_id: int, db: Session = Depends(get_db)):
    db_pet = crud.delete_pet(db, pet_id=pet_id)
    if db_pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")
    return db_pet
