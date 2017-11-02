from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///menu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

def getAllRestaurants():
	session = DBSession()
	restaurants = session.query(Restaurant).all()
	return restaurants

def getNameOfRestaurantFromID(id_):
	session = DBSession()
	restaurant = session.query(Restaurant).filter_by(id=id_).one()
	return restaurant.name

def deleteRestaurantFromID(id_):
	session = DBSession()
	session.query(Restaurant).filter_by(id=id_).delete()
	session.commit()
	return

def updateNameForID(id_, name):
	session = DBSession()
	new_restaurant = session.query(Restaurant).filter_by(id=int(id_)).one() 
	new_restaurant.name = name
	session.add(new_restaurant)
	session.commit()
	return

def createNew(name_):
	session = DBSession()
	restaurant = Restaurant(name = name_[0]) # a list is passed! why?
	session.add(restaurant)
	session.commit()
	return
