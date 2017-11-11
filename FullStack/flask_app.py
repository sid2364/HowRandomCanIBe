from flask import Flask, render_template, request, url_for, redirect, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///menu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)

@app.route("/")
@app.route("/restaurants/")
def showRestaurants():
	restaurants = session.query(Restaurant).all()
	items = session.query(MenuItem).all()
	return render_template("restaurants.html", restaurants = restaurants, items = items)

@app.route("/restaurants/<int:restaurant_id>/")
def showRestaurant(restaurant_id=1):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
	return render_template("restaurant.html", restaurant = restaurant, items = items)

@app.route("/restaurants/<int:restaurant_id>/new", methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == 'POST':
		newItem = MenuItem(
			name=request.form['menu_item'], 
			price=request.form['price'], 
			description=request.form['description'], 
			restaurant_id=restaurant.id
			)
		flash("New menu item, " + request.form['menu_item'] + ", added!!") 
		# should really be done after commit
		session.add(newItem)
		session.commit()
		return redirect(url_for('showRestaurant', restaurant_id=restaurant.id))
	else:
		return render_template("new_menu_item.html", restaurant = restaurant)

@app.route("/restaurants/<int:restaurant_id>/<int:menu_id>/edit", methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	menu_item = session.query(MenuItem).filter_by(id = menu_id).one()
	if request.method == 'POST':
		flash("Menu item, " + menu_item.name + ", has been changed to " + request.form['menu_item'] + "!")
		# should really be done after commit
		menu_item.name = request.form['menu_item']
		menu_item.price = request.form['price']
		menu_item.description = request.form['description']
		session.commit()
		return redirect(url_for('showRestaurant', restaurant_id=restaurant.id))
	else:
		return render_template('edit_menu_item.html', restaurant=restaurant, menu_item=menu_item)

@app.route("/restaurants/<int:restaurant_id>/<int:menu_id>/delete", methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	menu_item = session.query(MenuItem).filter_by(id = menu_id).one()
	if request.method == 'POST':
		flash("Menu item, " + menu_item.name + ", deleted!")
		# should really be done after commit
		session.query(MenuItem).filter_by(id=menu_item.id).delete()
		session.commit()
		return redirect(url_for('showRestaurant', restaurant_id=restaurant.id))
	else:
		return render_template('delete_menu_item.html', restaurant=restaurant, menu_item=menu_item)

@app.route("/restaurants/<int:restaurant_id>/menu/json", methods=['GET'])
def getRestaurantJSON(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	menu_items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id).all()
	return jsonify(MenuItemsInThisRestaurant=[item.serialize for item in menu_items])

@app.route("/restaurants/<int:restaurant_id>/menu/<int:menu_id>/json", methods=['GET'])
def getMenuItemJSON(restaurant_id, menu_id):
	menu_item = session.query(MenuItem).filter_by(id = menu_id).one()
	return jsonify(MenuItemsInThisRestaurant=menu_item.serialize)

if __name__ == "__main__":
	app.secret_key = "poop"
	app.debug = True
	app.run(host = "0.0.0.0", port = 5000)