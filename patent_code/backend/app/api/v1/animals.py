from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from backend.app.core.deps import get_db, get_current_user
from backend.app.schemas.animal import AnimalCreate, AnimalRead
from backend.app.services.animal_service import create_animal, get_animal, list_animals_for_owner, update_animal, delete_animal
from backend.app.models.animal import Animal
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/", response_model=AnimalRead)
def create(payload: AnimalCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    data = payload.dict()
    animal = create_animal(db, owner_id=user.id, data=data)
    return animal


@router.get("/", response_model=list[AnimalRead])
def list_my(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return list_animals_for_owner(db, user.id)


@router.get("/{animal_id}", response_model=AnimalRead)
def read(animal_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    animal = get_animal(db, animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail="Not found")
    if animal.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return animal


@router.put("/{animal_id}", response_model=AnimalRead)
def update(animal_id: int, payload: AnimalCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    animal = get_animal(db, animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail="Not found")
    if animal.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return update_animal(db, animal, payload.dict())


@router.delete("/{animal_id}")
def remove(animal_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    animal = get_animal(db, animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail="Not found")
    if animal.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    delete_animal(db, animal)
    return {"detail": "deleted"}


@router.post("/{animal_id}/photo")
def upload_photo(animal_id: int, file: UploadFile = File(...), db: Session = Depends(get_db), user=Depends(get_current_user)):
    animal = get_animal(db, animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail="Not found")
    if animal.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    content = file.file.read()
    # simple save
    from backend.app.services.health_service import save_document

    doc = save_document(db, animal_id=animal_id, filename=file.filename, content_type=file.content_type, data=content, store_in_db=False, storage_dir="storage")
    animal.photo = doc.file_path
    db.add(animal)
    db.commit()
    db.refresh(animal)
    return {"detail": "uploaded", "path": doc.file_path}
