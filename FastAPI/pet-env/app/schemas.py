from pydantic import BaseModel

class PetBase(BaseModel):
    name: str
    species: str
    age: int

class PetCreate(PetBase):
    pass  # PetCreate inherits from PetBase

class Pet(PetBase):
    id: int

    class Config:
        from_attributes = True  # Use 'from_attributes' instead of 'orm_mode'
