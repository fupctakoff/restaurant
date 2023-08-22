import pickle
from typing import Any

from starlette.responses import JSONResponse

from src.repository.redis_repository import RedisRepository
from src.repository.submenu_repository import SubMenuRepository


class SubMenuService:
    repository = SubMenuRepository()
    cache_repository = RedisRepository()

    def get_list_submenus(self, api_test_menu_id: int) -> list[Any]:
        cache = self.cache_repository.get_cache(name='list_of_submenus')
        if cache is not None:
            return cache  # type: ignore
        response = self.repository.get_list_submenus(api_test_menu_id)
        new_cache = pickle.dumps(response)
        self.cache_repository.set_cache(name='list_of_submenus', value=new_cache, ex=40)
        return response

    def get_one_submenu(self, api_test_menu_id: int, api_test_submenu_id: int) -> dict:
        cache = self.cache_repository.get_cache(name=f'one_submenu_{api_test_submenu_id}')
        if cache is not None:
            return cache
        if self.repository.submenu_is_part_of_menu_check(int(api_test_menu_id), int(api_test_submenu_id)):
            response = self.repository.submenu_representation(api_test_submenu_id)
        else:
            response = JSONResponse(content={'detail': 'submenu not found'}, status_code=404)
        new_cache = pickle.dumps(response)
        self.cache_repository.set_cache(name=f'one_submenu_{api_test_submenu_id}', value=new_cache, ex=40)
        return response

    def post_submenu(self, api_test_menu_id: int, submenu_items) -> dict:
        response = self.repository.post_submenu(api_test_menu_id, submenu_items)
        new_cache = pickle.dumps(response)
        self.cache_repository.clear_cache(api_test_menu_id)
        self.cache_repository.set_cache(name=f'one_submenu_{response["id"]}', value=new_cache)
        return response

    def patch_submenu(self, api_test_menu_id: int, api_test_submenu_id: int, submenu_items) -> dict:
        if self.repository.submenu_is_part_of_menu_check(api_test_menu_id, api_test_submenu_id):
            response = self.repository.patch_submenu(api_test_submenu_id, submenu_items)
        else:
            response = {'detail': 'submenu not found'}
        new_cache = pickle.dumps(response)
        self.cache_repository.set_cache(name=f'one_submenu_{api_test_submenu_id}', value=new_cache)
        self.cache_repository.del_cache(name='list_of_submenus')
        return response

    def delete_submenu(self, api_test_menu_id: int, api_test_submenu_id: int) -> dict:
        self.cache_repository.clear_cache(api_test_menu_id, api_test_submenu_id)
        if self.repository.submenu_is_part_of_menu_check(int(api_test_menu_id), int(api_test_submenu_id)):
            return self.repository.delete_submenu(api_test_submenu_id)
        return {'status': True, 'message': 'The submenu has been deleted'}
