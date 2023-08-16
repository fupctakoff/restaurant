import pickle
from typing import Any

import redis

from src.config import REDIS_HOST, REDIS_PORT

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)


class RedisRepository:
    def __init__(self, redis_client: redis.Redis = redis_client, ex: int = 30):
        self.redis_client = redis_client
        self.ex = ex

    def get_cache(self, name: str):
        cache = self.redis_client.get(name)
        if cache:
            return pickle.loads(cache)
        return None

    def set_cache(self, name: str, value: Any, ex=None):
        cache = self.redis_client.set(name=name, value=value, ex=(ex if ex else self.ex))
        return cache

    def del_cache(self, name: str) -> int:
        return self.redis_client.delete(name)

    def clear_cache(self, api_test_menu_id: int = None, api_test_submenu_id: int = None, target_dish_id: int = None):
        self.del_cache(name='list_of_submenus')
        self.del_cache(name=f'one_submenu_{api_test_submenu_id}')
        self.del_cache(name='list_of_menus')
        self.del_cache(name=f'one_menu_{api_test_menu_id}')
        self.del_cache(name=f'one_dish_{target_dish_id}')
        self.del_cache(name='list_of_dishes')