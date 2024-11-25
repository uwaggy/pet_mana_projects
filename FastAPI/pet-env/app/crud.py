from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas

# Create multiple pets
def create_pet(db: Session, pet: schemas.PetCreate):
    db_pet = models.Pet(name=pet.name, species=pet.species, age=pet.age)
    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)
    return db_pet
# Get all pets with optional pagination (skip/limit)
def get_pets(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Pet).offset(skip).limit(limit).all()

# Get a specific pet by ID
def get_pet(db: Session, pet_id: int):
    db_pet = db.query(models.Pet).filter(models.Pet.id == pet_id).first()
    if db_pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")
    return db_pet

# Update a pet's details by ID
def update_pet(db: Session, pet_id: int, pet: schemas.PetCreate):
    db_pet = db.query(models.Pet).filter(models.Pet.id == pet_id).first()
    if db_pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")
    db_pet.name = pet.name
    db_pet.species = pet.species
    db_pet.age = pet.age
    db.commit()
    db.refresh(db_pet)
    return db_pet

# Delete a pet by ID
def delete_pet(db: Session, pet_id: int):
    db_pet = db.query(models.Pet).filter(models.Pet.id == pet_id).first()
    if db_pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")
    db.delete(db_pet)
    db.commit()
    return db_pet
