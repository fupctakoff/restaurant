from fastapi import APIRouter, Depends

from src.database.pydantic_models import MenuAndSubmenuItem
from src.services.submenu_service import SubMenuService

router = APIRouter()


@router.get('/api/v1/menus/{api_test_menu_id}/submenus')
def get_list_submenus(api_test_menu_id: int, response: SubMenuService = Depends()) -> list:
    return response.get_list_submenus(api_test_menu_id)


@router.get('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}')
def get_one_submenu(api_test_menu_id: int, api_test_submenu_id: int, response: SubMenuService = Depends()) -> dict:
    return response.get_one_submenu(api_test_menu_id, api_test_submenu_id)


@router.post('/api/v1/menus/{api_test_menu_id}/submenus', status_code=201)
def post_submenu(api_test_menu_id: int, submenu_items: MenuAndSubmenuItem,
                 response: SubMenuService = Depends()) -> dict:
    return response.post_submenu(api_test_menu_id, submenu_items)


@router.patch('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}')
def patch_submenu(api_test_menu_id: int, api_test_submenu_id: int, submenu_items: MenuAndSubmenuItem,
                  response: SubMenuService = Depends()) -> dict:
    return response.patch_submenu(api_test_menu_id, api_test_submenu_id, submenu_items)


@router.delete('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}')
def delete_submenu(api_test_menu_id, api_test_submenu_id, response: SubMenuService = Depends()) -> dict:
    return response.delete_submenu(api_test_menu_id, api_test_submenu_id)
