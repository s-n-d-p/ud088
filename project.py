from flask import Flask, render_template, request, redirect, url_for, flash
from connection import session
from database_setup import Restaurant, MenuItem

app = Flask(__name__)

@app.route('/')
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('showrestaurants.html',restaurants = restaurants)

@app.route('/restaurants/<int:restaurant_id>/menu')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
    return render_template(
        'menu.html', restaurant=restaurant, items=items)


@app.route('/restaurants/<int:restaurant_id>/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], description=request.form[
                           'description'], price=request.form['price'], course=request.form['course'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash("new menu item created!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
        return render_template('newmenuitem.html', restaurant = restaurant)


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit',
           methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['price']:
            editedItem.price = request.form['price']    
        session.add(editedItem)
        session.commit()
        flash("Menu Item has been edited")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template(
            'editmenuitem.html', restaurant_id=restaurant_id, item=editedItem)


# DELETE MENU ITEM SOLUTION
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete',
           methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("Menu Item has been deleted")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
        return render_template('deletemenuitem.html', restaurant = restaurant ,item=itemToDelete)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)