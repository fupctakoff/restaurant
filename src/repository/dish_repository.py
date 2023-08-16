from starlette.responses import JSONResponse

from src.database.connect_session import session
from src.database.models import Dish
from src.database.pydantic_models import DishItem
from src.repository.submenu_repository import SubMenuRepository


class DishRepository:

    def __init__(self, session=session) -> None:
        self.session = session

    @staticmethod
    def dish_representation(dish_id: int):
        """Скелет для вывода объекта блюдо"""
        dish_obj = session.get(Dish, dish_id)
        if dish_obj:
            return {'id': str(dish_obj.id),
                    'title': dish_obj.title,
                    'description': dish_obj.description,
                    'price': str(dish_obj.price)
                    }
        return JSONResponse(content={'detail': 'dish not found'}, status_code=404)

    @staticmethod
    def dish_is_part_of_submenu_check(api_test_menu_id: int, api_test_submenu_id: int, target_dish_id: int):
        """Проверка, связан ли объект подменю с указанным объектом подменю, с вызовом функции проверки для подменю соответственно
           :return True если все в порядке: если значение не None - код работает дальше
        """
        if SubMenuRepository.submenu_is_part_of_menu_check(api_test_menu_id, api_test_submenu_id):
            dish_query = session.query(Dish.id).filter(Dish.submenu_id == api_test_submenu_id)
            list_of_dish_id = [i[0] for i in dish_query]
            if target_dish_id in list_of_dish_id:
                return True
        return None

    def get_list_dishes(self, api_test_submenu_id: int):
        dish_query = session.query(Dish).filter(Dish.submenu_id == api_test_submenu_id)
        return [self.dish_representation(dish.id) for dish in dish_query]

    def get_one_dish(self, target_dish_id: int):
        return self.dish_representation(target_dish_id)

    def post_dish(self, api_test_submenu_id: int, dish_items: DishItem):
        new_dish_obj = Dish(**dish_items.model_dump(), submenu_id=api_test_submenu_id)
        # new_dish_obj = Dish(title=dish_items.title, description=dish_items.description, price=dish_items.price, submenu_id=api_test_submenu_id)
        session.add(new_dish_obj)
        session.commit()
        return self.dish_representation(new_dish_obj.id)

    def patch_dish(self, target_dish_id: int, dish_items: DishItem):
        patching_dish = session.get(Dish, target_dish_id)
        if patching_dish:
            patching_dish.title = dish_items.title
            patching_dish.description = dish_items.description
            patching_dish.price = dish_items.price
            session.commit()
            return self.dish_representation(patching_dish.id)
        return {'detail': 'dish not found'}

    def delete_dish(self, target_dish_id: int):
        deleting_dish = session.get(Dish, target_dish_id)
        if deleting_dish:
            session.delete(deleting_dish)
            session.commit()
        return {'status': True, 'message': 'The dish has been deleted'}
