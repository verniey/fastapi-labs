from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from typing import List, Dict

from models.database import get_db

from models import core

from typing import List, Optional

from starlette.status import HTTP_200_OK
from starlette.status import HTTP_201_CREATED

from services import dishes as dish_service
from models import schemas
from models import core as models
from fastapi.encoders import jsonable_encoder  # Import the jsonable_encoder function
from typing import List, Optional
from uuid import UUID

dish_router = APIRouter(prefix='/api/v1/menus')


# @dish_router.get("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=schemas.Dish)
# def get_dish_3(menu_id: UUID, submenu_id: UUID, dish_id: UUID, db: Session = Depends(get_db)):
#     dish = dish_service.get_dish(db, submenu_id, dish_id)  # Pass submenu_id along with dish_id
    
#     return dish


@dish_router.post("/{menu_id}/submenus/{submenu_id}/dishes", response_model=schemas.Dish, status_code=201)
def create_dish(menu_id: UUID, submenu_id: UUID, dish: schemas.DishCreate, db: Session = Depends(get_db)):
    return dish_service.create_dish(db, dish, submenu_id)


@dish_router.patch("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=schemas.Dish)
def update_dish(
    dish_update: schemas.DishUpdate,
    db: Session = Depends(get_db),
    submenu_id: Optional[UUID] = None,
    dish_id: Optional[UUID] = None
):
    # if submenu_id is None or dish_id is None:
    #     # Handle the case when either submenu_id or dish_id is None (null)
    #     # You can raise an HTTPException or handle it based on your application logic.
    #     raise HTTPException(status_code=422, detail="Submenu_id or dish_id cannot be null")

    return dish_service.update_dish(db, dish_id, dish_update)




# @dish_router.delete("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
# def delete_dish_3(menu_id: UUID, submenu_id: UUID, dish_id: UUID, db: Session = Depends(get_db)):
#     db_dish = db.query(models.Dish).filter(models.Dish.id == dish_id).first()
#     if db_dish:
#         db.delete(db_dish)
#         db.commit()
#         return {"status": True, "message": "The dish has been deleted"}

#     return {"status": False, "message": "dish not found"}

    
@dish_router.get("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=schemas.Dish, status_code=HTTP_200_OK)
def get_dish(menu_id: UUID, submenu_id: UUID, dish_id: Optional[UUID], db: Session = Depends(get_db)):

    dish = dish_service.get_dish(db, submenu_id=submenu_id, dish_id=dish_id)
    if dish is None:
        raise HTTPException(status_code=404, detail="dish not found")
    
    return dish



@dish_router.get("/{menu_id}/submenus/{submenu_id}/dishes", response_model=List[schemas.Dish])
def get_dishes(menu_id: UUID, submenu_id: Optional[UUID] = None, db: Session = Depends(get_db)):
    dishes = dish_service.get_dishes(db, submenu_id=submenu_id)
    return dishes


@dish_router.patch("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=schemas.Dish)
def update_dish_2(
    menu_id: UUID,
    submenu_id: UUID,
    dish_id: UUID,
    dish_update: schemas.DishUpdate,
    db: Session = Depends(get_db)
):
    db_dish = db.query(models.Dish).filter(models.Dish.id == dish_id).first()
    if not db_dish:
        raise HTTPException(status_code=404, detail="Dish not found")

    # Check if the Dish is linked to a Submenu
    if db_dish.submenu_id is None:
        raise HTTPException(status_code=400, detail="Dish cannot be linked directly to a Menu")

    for key, value in dish_update.dict(exclude_unset=True).items():
        setattr(db_dish, key, value)

    # Check if the Dish is already linked to another Submenu
    if 'submenu_id' in dish_update and dish_update.submenu_id != db_dish.submenu_id:
        existing_dish = db.query(models.Dish).filter(models.Dish.submenu_id == dish_update.submenu_id).first()
        if existing_dish:
            raise HTTPException(status_code=400, detail="Dish already exists in another Submenu")

    db.commit()
    db.refresh(db_dish)
    return db_dish


@dish_router.delete("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
def delete_dish(menu_id: UUID, submenu_id: UUID, dish_id: UUID, db: Session = Depends(get_db)):
    db_dish = db.query(models.Dish).filter(models.Dish.id == dish_id).first()
    if db_dish:
        db.delete(db_dish)
        db.commit()
        return {"status": True, "message": "The dish has been deleted"}

    return {"status": False, "message": "dish not found"}
