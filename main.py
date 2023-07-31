from fastapi import FastAPI, APIRouter

from routers.menus import menu_router

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from typing import List, Dict

import models.core
from models.database import engine

models.core.Base.metadata.create_all(bind=engine)

from routers.menus import menu_router
from routers.dishes import dish_router
from routers.submenus import submenu_router



app = FastAPI()

app.include_router(menu_router)
app.include_router(dish_router)
app.include_router(submenu_router)