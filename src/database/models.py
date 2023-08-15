from sqlalchemy import Column, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Menu(Base):
    __tablename__ = 'menus'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    description = Column(String)
    submenus = relationship('SubMenu', backref='menu', cascade='all, delete')

    def __repr__(self):
        return f'menu instance id: {self.id}, title:{self.title}'


class SubMenu(Base):
    __tablename__ = 'submenus'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    description = Column(String)
    menu_id = Column(Integer, ForeignKey('menus.id'))
    dish = relationship('Dish', backref='submenu', cascade='all, delete')

    def __repr__(self):
        return f'submenu instance id: {self.id}, title:{self.title}'


class Dish(Base):
    __tablename__ = 'dishes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    description = Column(String)
    submenu_id = Column(Integer, ForeignKey('submenus.id'))
    price = Column(Numeric(15, 2))

    def __repr__(self):
        return f'dish instance id: {self.id}, title:{self.title}, price: {self.price}'