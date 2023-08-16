from fastapi import APIRouter, Depends

from src.database.pydantic_models import DishItem
from src.services.dish_service import DishService

router = APIRouter()


@router.get('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes')
def get_list_dishes(api_test_menu_id: int, api_test_submenu_id: int, response: DishService = Depends()) -> list:
    return response.get_list_dishes(api_test_menu_id, api_test_submenu_id)


@router.get('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/{target_dish_id}')
def get_one_dish(api_test_menu_id: int, api_test_submenu_id: int, target_dish_id: int,
                 response: DishService = Depends()) -> dict:
    return response.get_one_dish(api_test_menu_id, api_test_submenu_id, target_dish_id)


@router.post('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes', status_code=201)
def post_dish(api_test_menu_id: int, api_test_submenu_id: int, dish_items: DishItem,
              response: DishService = Depends()) -> dict:
    return response.post_dish(api_test_menu_id, api_test_submenu_id, dish_items)


@router.patch('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/{target_dish_id}')
def patch_dish(api_test_menu_id: int, api_test_submenu_id: int, target_dish_id: int, dish_items: DishItem,
               response: DishService = Depends()) -> dict:
    return response.patch_dish(api_test_menu_id, api_test_submenu_id, target_dish_id, dish_items)


@router.delete('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/{target_dish_id}')
def delete_dish(api_test_menu_id: int, api_test_submenu_id: int, target_dish_id: int,
                response: DishService = Depends()) -> dict:
    return response.delete_dish(api_test_menu_id, api_test_submenu_id, target_dish_id)
