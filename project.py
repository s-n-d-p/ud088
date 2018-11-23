from flask import Flask

from connection import session
from database_setup import MenuItem, Restaurant

app = Flask(__name__)

@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    q = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = q.id) 
    output = ''
    for i in items:
        output += i.name + '<br>'
        output += i.price + '<br>'
        output += i.description + '<br>'
        output += '<br>'
    return output

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
