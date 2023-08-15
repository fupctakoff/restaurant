from fastapi import APIRouter
from starlette.responses import JSONResponse

from src.database.connect_session import session
from src.database.models import Menu, SubMenu, Dish
from src.database.pydantic_models import MenuAndSubmenuItem

router = APIRouter()


def get_menu_bone(api_test_menu_id):
    """Скелет для вывода объекта меню"""
    try:
        menu_obj = session.query(Menu).get(api_test_menu_id)
        submenus_count = session.query(SubMenu).filter(SubMenu.menu_id == api_test_menu_id).count()
        dishes_count = 0
        for i in session.query(SubMenu).filter(SubMenu.menu_id == api_test_menu_id):
            dishes_count += session.query(Dish).filter(Dish.submenu_id == i.id).count()

        return {"id": str(menu_obj.id),
                "title": menu_obj.title,
                "description": menu_obj.description,
                "submenus_count": submenus_count,
                "dishes_count": dishes_count
                }
    except:
        return JSONResponse(content={"detail": "menu not found"}, status_code=404)


@router.get('/api/v1/menus')
def get_list_menus():
    return [get_one_menu(api_test_menu_id=menu.id) for menu in session.query(Menu).all()]


@router.get('/api/v1/menus/{api_test_menu_id}')
def get_one_menu(api_test_menu_id: int):
    return get_menu_bone(api_test_menu_id)


@router.post('/api/v1/menus')
def post_menu(menu_items: MenuAndSubmenuItem):
    new_menu_obj = Menu(title=menu_items.title, description=menu_items.description)
    session.add(new_menu_obj)
    session.commit()
    return JSONResponse(content=get_menu_bone(new_menu_obj.id), status_code=201)


@router.patch('/api/v1/menus/{api_test_menu_id}')
def patch_menu(api_test_menu_id: int, menu_items: MenuAndSubmenuItem):
    try:
        patching_menu = session.query(Menu).get(api_test_menu_id)
        patching_menu.title = menu_items.title
        patching_menu.description = menu_items.description
        session.commit()
        return get_menu_bone(patching_menu.id)
    except:
        return {"detail": "menu not found"}


@router.delete('/api/v1/menus/{api_test_menu_id}')
def delete_menu(api_test_menu_id: int):
    try:
        deleting_menu = session.query(Menu).get(api_test_menu_id)
        session.delete(deleting_menu)
        session.commit()
    except:
        print('Меню не было найдено / возникла проблема с удалением')
    return {"status": True, "message": "The menu has been deleted"}
