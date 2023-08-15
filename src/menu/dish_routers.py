from fastapi import APIRouter
from starlette.responses import JSONResponse

from src.database.connect_session import session
from src.database.models import Dish
from src.database.pydantic_models import DishItem
from src.menu.submenu_routers import submenu_is_part_of_menu_check

router = APIRouter()


def get_dish_bone(dish_id):
    """Скелет для вывода объекта блюдо"""
    try:
        dish_obj = session.query(Dish).get(dish_id)
        return {"id": str(dish_obj.id),
                "title": dish_obj.title,
                "description": dish_obj.description,
                "price": str(dish_obj.price)
                }
    except:
        return JSONResponse(content={"detail": "dish not found"}, status_code=404)


def dish_is_part_of_submenu_check(api_test_menu_id: int, api_test_submenu_id: int, target_dish_id: int):
    """Проверка, связан ли объект подменю с указанным объектом подменю, с вызовом функции проверки для подменю соответственно
       :return True - тк далее проверка, если значение не None - код работает дальше
    """
    if submenu_is_part_of_menu_check(api_test_menu_id, api_test_submenu_id):
        print('1234132')
        dish_query = session.query(Dish.id).filter(Dish.submenu_id == api_test_submenu_id)
        list_of_dish_id = [i[0] for i in dish_query]
        if target_dish_id in list_of_dish_id:
            return True
    return None


@router.get('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes')
def get_list_dishes(api_test_menu_id: int, api_test_submenu_id: int):
    if submenu_is_part_of_menu_check(api_test_menu_id, api_test_submenu_id):
        dish_query = session.query(Dish).filter(Dish.submenu_id == api_test_submenu_id)
        return [get_dish_bone(dish.id) for dish in dish_query]
    return []


@router.get('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/{target_dish_id}')
def get_one_dish(api_test_menu_id: int, api_test_submenu_id: int, target_dish_id: int):
    if dish_is_part_of_submenu_check(api_test_menu_id, api_test_submenu_id, target_dish_id):
        return get_dish_bone(target_dish_id)
    return JSONResponse(content={"detail": "dish not found"}, status_code=404)


@router.post('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes')
def post_dish(api_test_menu_id: int, api_test_submenu_id: int, dish_items: DishItem):
    if submenu_is_part_of_menu_check(api_test_menu_id, api_test_submenu_id):
        new_dish_obj = Dish(title=dish_items.title, description=dish_items.description, price=dish_items.price,
                            submenu_id=api_test_submenu_id)
        session.add(new_dish_obj)
        session.commit()
        return JSONResponse(content=get_dish_bone(new_dish_obj.id), status_code=201)
    return {'error': 'некорректный ввод меню и подменю'}


@router.patch('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/{target_dish_id}')
def patch_dish(api_test_menu_id: int, api_test_submenu_id: int, target_dish_id: int, dish_items: DishItem):
    if dish_is_part_of_submenu_check(api_test_menu_id, api_test_submenu_id, target_dish_id):
        try:
            patching_dish = session.query(Dish).get(target_dish_id)
            patching_dish.title = dish_items.title
            patching_dish.description = dish_items.description
            patching_dish.price = dish_items.price
            session.commit()
            return get_dish_bone(patching_dish.id)
        except:
            return {"detail": "dish not found"}
    return {"detail": "dish not found"}


@router.delete('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/{target_dish_id}')
def delete_submenu(api_test_menu_id: int, api_test_submenu_id: int, target_dish_id: int):
    if dish_is_part_of_submenu_check(api_test_menu_id, api_test_submenu_id, target_dish_id):
        try:
            deleting_dish = session.query(Dish).get(target_dish_id)
            session.delete(deleting_dish)
            session.commit()
        except:
            print('Возникла проблема с удалением')
    else:
        print('Блюдо не было найдено')
    return {"status": True, "message": "The dish has been deleted"}
