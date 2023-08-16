from fastapi import APIRouter, Depends

from src.database.pydantic_models import MenuAndSubmenuItem
from src.services.menu_service import MenuService

router = APIRouter()


@router.get('/api/v1/menus')
def get_list_menus(response: MenuService = Depends()) -> list:
    return response.get_list_menus()


@router.get('/api/v1/menus/{api_test_menu_id}')
def get_one_menu(api_test_menu_id: int, response: MenuService = Depends()) -> dict:
    return response.get_one_menu(api_test_menu_id)


@router.post('/api/v1/menus', status_code=201)
def post_menu(menu_items: MenuAndSubmenuItem, response: MenuService = Depends()) -> dict:
    return response.post_menu(menu_items)


@router.patch('/api/v1/menus/{api_test_menu_id}')
def patch_menu(api_test_menu_id: int, menu_items: MenuAndSubmenuItem,
               response: MenuService = Depends()) -> dict:
    return response.patch_menu(api_test_menu_id, menu_items)


@router.delete('/api/v1/menus/{api_test_menu_id}')
def delete_menu(api_test_menu_id: int, response: MenuService = Depends()) -> dict:
    return response.delete_menu(api_test_menu_id)
