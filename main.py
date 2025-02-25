from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Pydantic model for pet data input
class PetModel(BaseModel):
    id: int
    name: str
    age: int

# Pet class with a conventional constructor
class Pet:
    def __init__(self, id: int, name: str, age: int):
        self.id = id
        self.name = name
        self.age = age

# Simulated database
pets_db: List[Pet] = []

# Create a pet
@app.post('/pets/')
def create_pet(pet: PetModel):
    new_pet = Pet(pet.id, pet.name, pet.age)
    pets_db.append(new_pet)
    return new_pet.__dict__

# Update a pet
@app.put('/pets/{pet_id}')
def update_pet(pet_id: int, pet: PetModel):
    for index, existing_pet in enumerate(pets_db):
        if existing_pet.id == pet_id:
            pets_db[index] = Pet(pet.id, pet.name, pet.age)
            return pets_db[index].__dict__
    raise HTTPException(status_code=404, detail="Pet not found.")

# Delete a pet
@app.delete('/pets/{pet_id}')
def delete_pet(pet_id: int):
    for index, existing_pet in enumerate(pets_db):
        if existing_pet.id == pet_id:
            del pets_db[index]
            return {"message": "Pet successfully deleted."}
    raise HTTPException(status_code=404, detail="Pet not found.")

# List all pets
@app.get('/pets/')
def list_pets():
    return [pet.__dict__ for pet in pets_db]

# Get a pet by ID
@app.get('/pets/{pet_id}')
def get_pet_by_id(pet_id: int):
    for pet in pets_db:
        if pet.id == pet_id:
            return pet.__dict__
    raise HTTPException(status_code=404, detail="Pet not found.")