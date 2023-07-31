from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from typing import List, Dict

from models.database import get_db

from models import core
from uuid import UUID

#from models.schemas import Menu, MenuCreate, MenuUpdate, Message



from starlette.status import HTTP_200_OK
from starlette.status import HTTP_201_CREATED

from services import menus as menu_service
from models import schemas


menu_router = APIRouter(prefix='/api/v1/menus')

@menu_router.get("/", response_model=List[schemas.Menu])
def get_menus(db: Session = Depends(get_db)):
    return menu_service.get_menus(db)


@menu_router.get("/{menu_id}", response_model=schemas.Menu)
def get_menu(menu_id: UUID, db: Session = Depends(get_db)):
    menu = menu_service.get_menu(db, menu_id)
    if menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    return menu

@menu_router.post("/", response_model=schemas.Menu, status_code=HTTP_201_CREATED)
def create_menu(menu: schemas.MenuCreate, db: Session = Depends(get_db)) -> JSONResponse:
    new_menu = menu_service.create_menu(db, menu)
    
    return new_menu

@menu_router.patch("/{menu_id}", response_model=schemas.Menu)
def update_menu(menu_id: UUID, menu_update: schemas.MenuUpdate, db: Session = Depends(get_db)):
    db_menu = menu_service.update_menu(db, menu_id, menu_update)
    if db_menu:
        return db_menu
    else:
        raise HTTPException(status_code=404, detail="Menu not found")


@menu_router.delete("/{menu_id}")
def delete_menu(menu_id: UUID, db: Session = Depends(get_db)):
    response = menu_service.delete_menu(db, menu_id)
    if response:
        # Return a 200 status code when the menu is successfully deleted
        return {"status": True, "message": "The menu has been deleted"}
    else:
        raise HTTPException(status_code=404, detail="menu not found")