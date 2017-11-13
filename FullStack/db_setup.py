import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Restaurant(Base):
	__tablename__ = 'restaurant'
	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	@property
	def serialize(self):
		return {
			'id': self.id,
			'name': self.name,
		}


class MenuItem(Base):
	__tablename__ = 'menu_item'
	name = Column(String(50), nullable=False)
	id = Column(Integer, primary_key=True)
	description = Column(String(250))
	price = Column(String(8))
	course = Column(String(50))
	restaurant_id = Column(Integer, ForeignKey('restaurant.id'))

	restaurant = relationship(Restaurant)
	@property
	def serialize(self):
		return {
			'id': self.id,
			'name': self.name,
			'price': self.price,
			'description': self.description,
			'course': self.course,
			'restaurant_id': self.restaurant_id,
		}

engine = create_engine("sqlite:///menu.db")

Base.metadata.create_all(engine)