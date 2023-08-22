import pickle

from starlette.responses import JSONResponse

from src.repository.dish_repository import DishRepository
from src.repository.redis_repository import RedisRepository
from src.repository.submenu_repository import SubMenuRepository


class DishService:
    repository = DishRepository()
    cache_repository = RedisRepository()

    def get_list_dishes(self, api_test_menu_id: int, api_test_submenu_id: int) -> list:
        cache = self.cache_repository.get_cache(name='list_of_dishes')
        if cache is not None:
            return cache
        if SubMenuRepository.submenu_is_part_of_menu_check(api_test_menu_id, api_test_submenu_id):
            response = self.repository.get_list_dishes(api_test_submenu_id)
        else:
            response = []
        new_cache = pickle.dumps(response)
        self.cache_repository.set_cache(name='list_of_dishes', value=new_cache)
        return response

    def get_one_dish(self, api_test_menu_id: int, api_test_submenu_id: int, target_dish_id: int) -> dict:
        cache = self.cache_repository.get_cache(name=f'one_dish_{target_dish_id}')
        if cache is not None:
            return cache
        if self.repository.dish_is_part_of_submenu_check(api_test_menu_id, api_test_submenu_id, target_dish_id):
            response = self.repository.dish_representation(target_dish_id)
        else:
            response = JSONResponse(content={'detail': 'dish not found'}, status_code=404)
        new_cache = pickle.dumps(response)
        self.cache_repository.set_cache(name=f'one_dish_{target_dish_id}', value=new_cache)
        return response

    def post_dish(self, api_test_menu_id: int, api_test_submenu_id: int, dish_items: int) -> dict:
        if SubMenuRepository.submenu_is_part_of_menu_check(api_test_menu_id, api_test_submenu_id):
            response = self.repository.post_dish(api_test_submenu_id, dish_items)
        else:
            response = {'error': 'некорректный ввод меню и подменю'}
        new_cache = pickle.dumps(response)
        self.cache_repository.clear_cache(api_test_menu_id, api_test_submenu_id)
        self.cache_repository.set_cache(name=f'one_dish_{response["id"]}', value=new_cache)
        return response

    def patch_dish(self, api_test_menu_id: int, api_test_submenu_id: int, target_dish_id: int, dish_items) -> dict:
        if self.repository.dish_is_part_of_submenu_check(api_test_menu_id, api_test_submenu_id, target_dish_id):
            response = self.repository.patch_dish(target_dish_id, dish_items)
        else:
            response = {'detail': 'dish not found'}
        new_cache = pickle.dumps(response)
        self.cache_repository.set_cache(name=f'one_dish_{target_dish_id}', value=new_cache)
        self.cache_repository.del_cache(name='list_of_dishes')
        return response

    def delete_dish(self, api_test_menu_id: int, api_test_submenu_id: int, target_dish_id: int) -> dict:
        self.cache_repository.clear_cache(api_test_menu_id, api_test_submenu_id, target_dish_id)
        if self.repository.dish_is_part_of_submenu_check(api_test_menu_id, api_test_submenu_id, target_dish_id):
            return self.repository.delete_dish(target_dish_id)
        return {'status': True, 'message': 'The dish has been deleted'}
