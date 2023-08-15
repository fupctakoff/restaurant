from fastapi import APIRouter
from starlette.responses import JSONResponse

from src.database.connect_session import session
from src.database.models import SubMenu, Dish
from src.database.pydantic_models import MenuAndSubmenuItem

router = APIRouter()


def get_submenu_bone(submenu_id):
    """Скелет для вывода объекта подменю"""
    try:
        submenu_obj = session.query(SubMenu).get(submenu_id)
        dishes_count = session.query(Dish).filter(Dish.submenu_id == submenu_id).count()

        return {"id": str(submenu_obj.id),
                "title": submenu_obj.title,
                "description": submenu_obj.description,
                "dishes_count": dishes_count
                }
    except:
        return JSONResponse(content={"detail": "submenu not found"}, status_code=404)


def submenu_is_part_of_menu_check(api_test_menu_id, api_test_submenu_id):
    """Проверка, связан ли объект подменю с указанным объектом меню
       :return True - тк далее проверка, если значение не None - код работает дальше
    """
    submenu_query = session.query(SubMenu.id).filter(SubMenu.menu_id == api_test_menu_id)
    list_of_submenu_id = [i[0] for i in submenu_query]
    if api_test_submenu_id in list_of_submenu_id:
        return True
    return None


@router.get('/api/v1/menus/{api_test_menu_id}/submenus')
def get_list_submenus(api_test_menu_id: int):
    submenu_query = session.query(SubMenu).filter(SubMenu.menu_id == api_test_menu_id)
    return [get_submenu_bone(submenu_id=submenu.id) for submenu in submenu_query]


@router.get('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}')
def get_one_submenu(api_test_menu_id, api_test_submenu_id):
    try:
        if submenu_is_part_of_menu_check(int(api_test_menu_id), int(api_test_submenu_id)):
            return get_submenu_bone(api_test_submenu_id)
        return JSONResponse(content={"detail": "submenu not found"}, status_code=404)
    except:
        return JSONResponse(content={"detail": "submenu not found"}, status_code=404)


@router.post('/api/v1/menus/{api_test_menu_id}/submenus')
def post_submenu(api_test_menu_id: int, submenu_items: MenuAndSubmenuItem):
    new_submenu_obj = SubMenu(title=submenu_items.title, description=submenu_items.description,
                              menu_id=api_test_menu_id)
    session.add(new_submenu_obj)
    session.commit()
    return JSONResponse(content=get_submenu_bone(new_submenu_obj.id), status_code=201)


@router.patch('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}')
def patch_menu(api_test_menu_id: int, api_test_submenu_id: int, menu_items: MenuAndSubmenuItem):
    if submenu_is_part_of_menu_check(api_test_menu_id, api_test_submenu_id):
        try:
            patching_submenu = session.query(SubMenu).get(api_test_submenu_id)
            patching_submenu.title = menu_items.title
            patching_submenu.description = menu_items.description
            session.commit()
            return get_submenu_bone(patching_submenu.id)
        except:
            return {"detail": "submenu not found"}
    return {"detail": "submenu not found"}


@router.delete('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}')
def delete_submenu(api_test_menu_id, api_test_submenu_id):
    try:
        if submenu_is_part_of_menu_check(int(api_test_menu_id), int(api_test_submenu_id)):
            try:
                deleting_submenu = session.query(SubMenu).get(api_test_submenu_id)
                session.delete(deleting_submenu)
                session.commit()
            except:
                print('Подменю не было найдено / возникла проблема с удалением')
        else:
            print('Подменю не было найдено 111 / возникла проблема с удалением')
        return {"status": True, "message": "The submenu has been deleted"}
    except:
        return {"status": True, "message": "The submenu has been deleted"}
