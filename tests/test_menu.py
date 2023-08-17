import pytest

from src.database.connect_session import engine, session
from src.database.models import Base, Dish, Menu, SubMenu
from src.database.pydantic_models import DishItem, MenuAndSubmenuItem
from src.repository.dish_repository import DishRepository
from src.repository.menu_repository import MenuRepository
from src.repository.submenu_repository import SubMenuRepository
from src.services.dish_service import DishService
from src.services.menu_service import MenuService
from src.services.submenu_service import SubMenuService


@pytest.fixture(scope='session', autouse=True)
def connect_and_refresh_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


class TestMenu:
    service = MenuService()
    repository = MenuRepository()

    @pytest.mark.parametrize(
        'api_test_menu_id, menu_items', [
            (1, MenuAndSubmenuItem(title='string', description='string')),
            (2, MenuAndSubmenuItem(title='string2', description='string2')),
            (3, MenuAndSubmenuItem(title='string3', description='string3')),
        ]
    )
    def test_post_menu(self, api_test_menu_id, menu_items: MenuAndSubmenuItem):
        assert self.service.post_menu(menu_items) == self.repository.menu_representation(api_test_menu_id)

    @pytest.mark.parametrize(
        'api_test_menu_id', [1, 2]
    )
    def test_get_one_menu(self, api_test_menu_id):
        assert self.service.get_one_menu(api_test_menu_id) == self.repository.menu_representation(api_test_menu_id)

    @pytest.mark.parametrize(
        'api_test_menu_id, menu_items', [
            (1, MenuAndSubmenuItem(title='patch1', description='patched1')),
            (2, MenuAndSubmenuItem(title='patch2', description='patched2')),
        ]
    )
    def test_patch_menu(self, api_test_menu_id: int, menu_items: MenuAndSubmenuItem):
        assert self.service.patch_menu(api_test_menu_id, menu_items) == self.repository.menu_representation(
            api_test_menu_id)

    def test_get_list_menus(self):
        assert self.service.get_list_menus() == [self.repository.menu_representation(api_test_menu_id=menu.id) for menu
                                                 in session.query(Menu).all()]

    @pytest.mark.parametrize(
        'api_test_menu_id', [1, 2]
    )
    def test_delete_menu(self, api_test_menu_id):
        assert self.service.delete_menu(api_test_menu_id) == {'status': True, 'message': 'The menu has been deleted'}


class TestSubMenu:
    service = SubMenuService()
    repository = SubMenuRepository()

    @pytest.mark.parametrize(
        'api_test_menu_id, api_test_submenu_id, menu_items', [
            (3, 1, MenuAndSubmenuItem(title='string', description='string')),
            (3, 2, MenuAndSubmenuItem(title='string2', description='string2')),
            (3, 3, MenuAndSubmenuItem(title='string3', description='string3')),
        ]
    )
    def test_post_submenu(self, api_test_menu_id, api_test_submenu_id, menu_items: MenuAndSubmenuItem):
        assert self.service.post_submenu(api_test_menu_id, menu_items) == self.repository.submenu_representation(
            api_test_submenu_id)

    @pytest.mark.parametrize(
        'api_test_menu_id, api_test_submenu_id', [(3, 1), (3, 2)]
    )
    def test_get_one_submenu(self, api_test_menu_id, api_test_submenu_id):
        assert self.service.get_one_submenu(api_test_menu_id,
                                            api_test_submenu_id) == self.repository.submenu_representation(
            api_test_submenu_id)

    @pytest.mark.parametrize(
        'api_test_menu_id,api_test_submenu_id, menu_items', [
            (3, 1, MenuAndSubmenuItem(title='patch1', description='patched1')),
            (3, 2, MenuAndSubmenuItem(title='patch2', description='patched2')),
        ]
    )
    def test_patch_submenu(self, api_test_menu_id, api_test_submenu_id, menu_items: MenuAndSubmenuItem):
        assert self.service.patch_submenu(api_test_menu_id, api_test_submenu_id,
                                          menu_items) == self.repository.submenu_representation(api_test_submenu_id)

    @pytest.mark.parametrize(
        'api_test_menu_id', [3]
    )
    def test_get_list_submenus(self, api_test_menu_id):
        submenu_query = session.query(SubMenu).filter(SubMenu.menu_id == api_test_menu_id)
        assert self.service.get_list_submenus(api_test_menu_id) == [
            self.repository.submenu_representation(api_test_submenu_id=submenu.id) for submenu in
            submenu_query]

    @pytest.mark.parametrize(
        'api_test_menu_id, api_test_submenu_id', [(3, 1), (3, 2)]
    )
    def test_delete_submenu(self, api_test_menu_id, api_test_submenu_id):
        assert self.service.delete_submenu(api_test_menu_id, api_test_submenu_id) == {'status': True,
                                                                                      'message': 'The submenu has been deleted'}


class TestDish:
    service = DishService()
    repository = DishRepository()

    @pytest.mark.parametrize(
        'api_test_menu_id, api_test_submenu_id, target_dish_id, dish_items', [
            (3, 3, 1, DishItem(title='string', description='string', price=1.02)),
            (3, 3, 2, DishItem(title='string2', description='string2', price=1.04)),
        ]
    )
    def test_post_dish(self, api_test_menu_id, api_test_submenu_id, target_dish_id, dish_items: DishItem):
        assert self.service.post_dish(api_test_menu_id, api_test_submenu_id,
                                      dish_items) == self.repository.dish_representation(target_dish_id)

    @pytest.mark.parametrize(
        'api_test_menu_id, api_test_submenu_id, target_dish_id', [(3, 3, 1), (3, 3, 2)]
    )
    def test_get_one_dish(self, api_test_menu_id, api_test_submenu_id, target_dish_id):
        assert self.service.get_one_dish(api_test_menu_id, api_test_submenu_id,
                                         target_dish_id) == self.repository.dish_representation(target_dish_id)

    @pytest.mark.parametrize(
        'api_test_menu_id, api_test_submenu_id, target_dish_id, dish_items', [
            (3, 3, 1, DishItem(title='patch1', description='patched1', price=1.01)),
            (3, 3, 2, DishItem(title='patch2', description='patched2', price=1.03)),
        ]
    )
    def test_patch_dish(self, api_test_menu_id, api_test_submenu_id, target_dish_id, dish_items: DishItem):
        assert self.service.patch_dish(api_test_menu_id, api_test_submenu_id, target_dish_id,
                                       dish_items) == self.repository.dish_representation(
            target_dish_id)

    @pytest.mark.parametrize(
        'api_test_menu_id, api_test_submenu_id', [(3, 3)]
    )
    def test_get_list_dishes(self, api_test_menu_id, api_test_submenu_id):
        dish_query = session.query(Dish).filter(Dish.submenu_id == api_test_submenu_id)
        assert self.service.get_list_dishes(api_test_menu_id, api_test_submenu_id) == [
            self.repository.dish_representation(dish.id) for dish in dish_query]

    @pytest.mark.parametrize(
        'api_test_menu_id, api_test_submenu_id, target_dish_id', [(3, 3, 1), (3, 3, 2)]
    )
    def test_delete_dish(self, api_test_menu_id, api_test_submenu_id, target_dish_id):
        assert self.service.delete_dish(api_test_menu_id, api_test_submenu_id, target_dish_id) == {'status': True,
                                                                                                   'message': 'The dish has been deleted'}


@pytest.fixture()
def delete_after_use():
    Base.metadata.drop_all(engine)
