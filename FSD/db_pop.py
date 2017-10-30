from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base, Restaurant, MenuItem

engine = create_engine("sqlite:///menu.db")

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

rest1 = Restaurant(name='Sid\'s Pizzeria')
session.add(rest1)
session.commit()
#print(session.query(Restaurant).all())

item1 = MenuItem(name='Margharita', description='Some cheesy one-liner.',
	course='Entree', price="Rs.200", restaurant=rest1)
session.add(item1)
session.commit()
#print(session.query(MenuItem).all())
