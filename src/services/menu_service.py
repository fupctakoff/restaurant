import pickle

from src.repository.menu_repository import MenuRepository
from src.repository.redis_repository import RedisRepository


class MenuService:
    repository = MenuRepository()
    cache_repository = RedisRepository()

    def get_list_menus(self) -> list:
        cache = self.cache_repository.get_cache(name='list_of_menus')
        if cache is not None:
            return cache
        response = self.repository.get_list_menus()
        new_cache = pickle.dumps(response)
        self.cache_repository.set_cache(name='list_of_menus', value=new_cache, ex=40)
        # time.sleep(4)
        return response

    def get_one_menu(self, api_test_menu_id: int) -> dict:
        cache = self.cache_repository.get_cache(name=f'one_menu_{api_test_menu_id}')
        if cache is not None:
            return cache
        response = self.repository.get_one_menu(api_test_menu_id)
        new_cache = pickle.dumps(response)
        self.cache_repository.set_cache(name=f'one_menu_{api_test_menu_id}', value=new_cache, ex=40)
        return response

    def post_menu(self, menu_items) -> dict:
        response = self.repository.post_menu(menu_items)
        new_cache = pickle.dumps(response)
        self.cache_repository.set_cache(name=f'one_menu_{response["id"]}', value=new_cache)
        self.cache_repository.del_cache(name='list_of_menus')
        return response

    def patch_menu(self, api_test_menu_id: int, menu_items) -> dict:
        response = self.repository.patch_menu(api_test_menu_id, menu_items)
        new_cache = pickle.dumps(response)
        self.cache_repository.set_cache(name=f'one_menu_{api_test_menu_id}', value=new_cache)
        self.cache_repository.del_cache(name='list_of_menus')
        return response

    def delete_menu(self, api_test_menu_id: int) -> dict:
        self.cache_repository.clear_cache(api_test_menu_id)
        return self.repository.delete_menu(api_test_menu_id)
