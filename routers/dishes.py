from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from typing import List, Dict

from models.database import get_db

from models import core

#from models.schemas import Menu, MenuCreate, MenuUpdate, Message

from uuid import UUID


from starlette.status import HTTP_200_OK
from starlette.status import HTTP_201_CREATED

from services import dishes as dish_service
from models import schemas


dish_router = APIRouter(prefix='/api/v1/menus')


@dish_router.get("/{menu_id}/submenus/{submenu_id}/dishes", response_model=List[schemas.Dish])
def get_dishes(submenu_id: UUID, db: Session = Depends(get_db)):
    return dish_service.get_dishes(db, submenu_id)



@dish_router.get("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=schemas.Dish)
def create_dish(
    menu_id: UUID, submenu_id: UUID, dish: schemas.DishCreate, db: Session = Depends(get_db)
):
    return dish_service.create_dish(db, menu_id, submenu_id, dish)




@dish_router.post("/{menu_id}/submenus/{submenu_id}/dishes", response_model=schemas.Dish, status_code=201)
def create_dish(menu_id: UUID, submenu_id: UUID, dish: schemas.DishCreate, db: Session = Depends(get_db)):
    return dish_service.create_dish(db, dish, menu_id, submenu_id)



@dish_router.patch("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=schemas.Dish)
def update_dish(menu_id: UUID, submenu_id: int, dish_id: int, dish_update: schemas.DishUpdate, db: Session = Depends(get_db)):
    return dish_service.update_dish(db, dish_id=dish_id, dish_update=dish_update)


@dish_router.delete("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
def delete_dish(menu_id: UUID, submenu_id: int, dish_id: int, db: Session = Depends(get_db)):
    deleted = dish_service.delete_dish(db, dish_id=dish_id)
    if deleted:
        return {"status": True, "message": "The dish has been deleted"}
    else:
        raise HTTPException(status_code=404, detail="dish not found")

    
@dish_router.get("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=schemas.Dish)
def read_dish(menu_id: UUID, submenu_id: UUID, dish_id: UUID, db: Session = Depends(get_db)):
    dish = crud.get_dish(db, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
    if dish is None:
        raise HTTPException(status_code=404, detail="Dish not found")
    return {
        "id": dish.id,
        "title": dish.title,
        "description": dish.description,
        "price": "{:.2f}".format(dish.price)  # Format price with two decimal places
    }