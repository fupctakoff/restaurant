from fastapi import FastAPI

from src.menu.menu_routers import router as router_menus
from src.menu.submenu_routers import router as router_submenus
from src.menu.dish_routers import router as router_dishes

app = FastAPI()

app.include_router(router_menus)
app.include_router(router_submenus)
app.include_router(router_dishes)