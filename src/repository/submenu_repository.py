from starlette.responses import JSONResponse

from src.database.connect_session import session
from src.database.models import Dish, SubMenu
from src.database.pydantic_models import MenuAndSubmenuItem


class SubMenuRepository:

    def __init__(self, session=session) -> None:
        self.session = session

    @staticmethod
    def submenu_representation(api_test_submenu_id: int):
        """Скелет для вывода объекта подменю"""
        submenu_obj = session.get(SubMenu, api_test_submenu_id)
        if submenu_obj:
            dishes_count = session.query(Dish).filter(Dish.submenu_id == api_test_submenu_id).count()
            return {'id': str(submenu_obj.id),
                    'title': submenu_obj.title,
                    'description': submenu_obj.description,
                    'dishes_count': dishes_count
                    }
        return JSONResponse(content={'detail': 'submenu not found'}, status_code=404)

    @staticmethod
    def submenu_is_part_of_menu_check(api_test_menu_id: int, api_test_submenu_id: int):
        """Проверка, связан ли объект подменю с объектом меню
           :return True - если все в порядке: если значение не None - код работает дальше
        """
        submenu_query = session.query(SubMenu.id).filter(SubMenu.menu_id == api_test_menu_id)
        list_of_submenu_id = [i[0] for i in submenu_query]
        if api_test_submenu_id in list_of_submenu_id:
            return True
        return None

    def get_list_submenus(self, api_test_menu_id: int):
        submenu_query = session.query(SubMenu).filter(SubMenu.menu_id == api_test_menu_id)
        return [self.submenu_representation(api_test_submenu_id=submenu.id) for submenu in submenu_query]

    def get_one_submenu(self, api_test_submenu_id: int):
        return self.submenu_representation(api_test_submenu_id)

    def post_submenu(self, api_test_menu_id: int, submenu_items: MenuAndSubmenuItem):
        new_submenu_obj = SubMenu(**submenu_items.model_dump(), menu_id=api_test_menu_id)
        session.add(new_submenu_obj)
        session.commit()
        return self.submenu_representation(new_submenu_obj.id)

    def patch_submenu(self, api_test_submenu_id: int, submenu_items: MenuAndSubmenuItem):
        patching_submenu = session.get(SubMenu, api_test_submenu_id)
        if patching_submenu:
            patching_submenu.title = submenu_items.title
            patching_submenu.description = submenu_items.description
            session.commit()
            return self.submenu_representation(patching_submenu.id)
        return {'detail': 'submenu not found'}

    def delete_submenu(self, api_test_submenu_id: int):
        deleting_submenu = session.get(SubMenu, api_test_submenu_id)
        if deleting_submenu:
            session.delete(deleting_submenu)
            session.commit()
        return {'status': True, 'message': 'The submenu has been deleted'}
