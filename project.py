from flask import Flask, redirect, render_template, request, url_for, flash 

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

@app.route('/restaurant/<int:restaurant_id>/new/', methods = ['GET','POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name = request.form['name'], restaurant_id = restaurant_id)
        session.add(newItem)
        session.commit()
        flash("Menu item added!")
        return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))
    elif request.method == 'GET':
        restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
        return render_template('newmenuitem.html',restaurant=restaurant)
    else:
        return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))

# Task 2: Create route for editMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/', methods = ['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
    if request.method == 'GET':
        item = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, id = menu_id).one()
        return render_template('editmenuitem.html', restaurant_id = restaurant_id, menu_id = menu_id,item_name=item.name)
    elif request.method == 'POST':
        item = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, id = menu_id).one()
        item.name = request.form['name']
        session.add(item)
        session.commit()
        flash("Menu item updated!")
        return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))
    else:
        return ''

# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/', methods = ['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
    if request.method == 'GET':
        restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
        item = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, id = menu_id).one() 
        return render_template('deletemenuitem.html',restaurant = restaurant, item = item) 
    elif request.method == 'POST':
        item = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, id = menu_id).one() 
        session.delete(item)
        session.commit()
        flash("Menu item deleted!")
        return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))        
    else:
        pass 

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
    app.secret_key = 'super_secret_key '
    app.debug = True
    app.run(host='0.0.0.0',port=5000)
