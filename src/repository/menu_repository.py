from starlette.responses import JSONResponse

from src.database.connect_session import session
from src.database.models import Dish, Menu, SubMenu
from src.database.pydantic_models import MenuAndSubmenuItem


class MenuRepository:

    def __init__(self, session=session) -> None:
        self.session = session

    @staticmethod
    def menu_representation(api_test_menu_id):
        """Скелет для вывода объекта меню"""
        menu_obj = session.get(Menu, api_test_menu_id)
        if menu_obj:
            submenus_count = session.query(SubMenu).filter(SubMenu.menu_id == api_test_menu_id).count()
            dishes_count = 0
            for i in session.query(SubMenu).filter(SubMenu.menu_id == api_test_menu_id):
                dishes_count += session.query(Dish).filter(Dish.submenu_id == i.id).count()

            return {'id': str(menu_obj.id),
                    'title': menu_obj.title,
                    'description': menu_obj.description,
                    'submenus_count': submenus_count,
                    'dishes_count': dishes_count
                    }
        return JSONResponse(content={'detail': 'menu not found'}, status_code=404)

    def get_list_menus(self):
        return [self.get_one_menu(api_test_menu_id=menu.id) for menu in session.query(Menu).all()]

    def get_one_menu(self, api_test_menu_id: int):
        return self.menu_representation(api_test_menu_id)

    def post_menu(self, menu_items: MenuAndSubmenuItem):
        new_menu_obj = Menu(**menu_items.model_dump())
        # new_menu_obj = Menu(menu_items['title'], menu_items['description'])
        session.add(new_menu_obj)
        session.commit()
        return self.menu_representation(new_menu_obj.id)

    def patch_menu(self, api_test_menu_id: int, menu_items: MenuAndSubmenuItem):
        patching_menu = session.get(Menu, api_test_menu_id)
        if patching_menu:
            patching_menu.title = menu_items.title
            patching_menu.description = menu_items.description
            session.commit()
            return self.menu_representation(patching_menu.id)
        return {'detail': 'menu not found'}

    def delete_menu(self, api_test_menu_id: int):
        deleting_menu = session.get(Menu, api_test_menu_id)
        if deleting_menu:
            session.delete(deleting_menu)
            session.commit()
        return {'status': True, 'message': 'The menu has been deleted'}
