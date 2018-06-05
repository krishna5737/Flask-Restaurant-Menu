from flask import Flask, render_template,request,redirect,url_for,flash,jsonify
from sqlalchemy import create_engine
from database_setup import Base, Restaurant, MenuItem

from sqlalchemy.orm import sessionmaker
app = Flask(__name__)

#Fake Restaurants
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/Restaurant')
def showRestaurants():
    restaurant = session.query(Restaurant).all()
    return render_template('restaurants.html',restaurant=restaurant)


@app.route('/restaurant/new',methods = ['GET','POST'])
def newRestaurant():
    if request.method == "POST":
        newItem = Restaurant(name=request.form['name'])
        session.add(newItem)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newRestaurant.html')

@app.route('/restaurant/<int:restaurant_id>/edit',methods=['GET','POST'])
def editRestaurant(restaurant_id):
    restaurantToEdit = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        restaurantToEdit.name = request.form['name']
        session.add(restaurantToEdit)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('editRestaurant.html',restaurant_id=restaurant_id, restaurantToEdit=restaurantToEdit)

@app.route('/restaurant/<int:restaurant_id>/delete',methods=["GET",'POST'])
def deleteRestaurant(restaurant_id):
    restaurantToDelete = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        session.delete(restaurantToDelete)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('deleteRestaurant.html',restaurant_id=restaurant_id, restaurantToDelete=restaurantToDelete)

@app.route('/restaurant/<int:restaurant_id>/menu')
@app.route('/restaurant/<int:restaurant_id>')
def showMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    return render_template('menu.html', restaurant_id=restaurant_id,restaurant=restaurant, items=items)


@app.route('/restaurant/<int:restaurant_id>/menu/new',methods = ['GET','POST'])
def newMenuItem(restaurant_id):
    if request.method == "POST":
        newItem = MenuItem(name=request.form['name'],restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('showMenu',restaurant_id=restaurant_id))
    else:
        return render_template('newMenuItem.html',restaurant_id = restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit',methods=['GET','POST'])
def editMenuItem(restaurant_id,menu_id):
    menuItemToEdit = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        menuItemToEdit.name = request.form['name']
        session.add(menuItemToEdit)
        session.commit()
        return redirect(url_for('showMenu',restaurant_id=restaurant_id))
    else:
        return render_template('editMenuItem.html',restaurant_id=restaurant_id, menuItemToEdit=menuItemToEdit,menu_id=menu_id)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete',methods = ['GET','POST'])
def deleteMenuItem(restaurant_id,menu_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    item = session.query(MenuItem).filter_by(restaurant_id = restaurant_id,id = menu_id).one()
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        return redirect(url_for('showMenu',restaurant_id=restaurant_id))
    else:
        return render_template('deleteMenuItem.html',restaurant_id = restaurant_id, item = item, menu_id=menu_id)

if __name__ == '__main__':
    app.secret_key = 'super-secret_key'
    app.debug = True
    app.run()
