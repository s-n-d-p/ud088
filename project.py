from flask import Flask, render_template, url_for

from connection import session
from database_setup import MenuItem, Restaurant

app = Flask(__name__)

@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id) 
    return render_template('menu.html',restaurant=restaurant,items=items)
    

# Task 1: Create route for newMenuItem function here

@app.route('/restaurant/<int:restaurant_id>/new/')
def newMenuItem(restaurant_id):
    return "page to create a new menu item. Task 1 complete!"

# Task 2: Create route for editMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/')
def editMenuItem(restaurant_id, menu_id):
    return "page to edit a menu item. Task 2 complete!"

# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/')
def deleteMenuItem(restaurant_id, menu_id):
    return "page to delete a menu item. Task 3 complete!"

@app.route('/hello')
def hello_world():
    q = session.query(Restaurant).first()
    items = session.query(MenuItem).filter_by(restaurant_id = q.id) 
    output = ''
    for i in items:
        output += i.name + '<br>'
        output += i.price + '<br>'
        output += i.description + '<br>'
        output += '<br>'
    return output

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0',port=5000)
