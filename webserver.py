import cgi
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

from connection import session
from database_setup import MenuItem, Restaurant


class WebServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants") :
                self.send_response(200);
                self.send_header('Content-type','text/html')
                self.end_headers()
                message = '<html><body>'
                message += 'LIST OF RESTAURANTS!' 
                message += '<ul>'
                restaurants = session.query(Restaurant).all()
                for resturant in restaurants:
                    editLink = '/restaurant/' + str(resturant.id) + '/edit'
                    deleteLink = '/restaurant/' + str(resturant.id) + '/delete'
                    message += '<li>' + str(resturant.name) + ": <a href='" + str(editLink) +  "'>" + "Edit</a> <a href='" + str(deleteLink) + "'> Delete</a></li>"
                message += '</ul>'
                message += "Add a <a href='/resturants/new'>new</a> restaurant?"
                message += '</body></html>'
                self.wfile.write(message)
            elif self.path.endswith("/hello"):
                self.send_response(200);
                self.send_header('Content-type','text/html')
                self.end_headers()
                message = '<html><body>'
                message += 'Hello!' 
                message += '''
                            <form method='POST' enctype='multipart/form-data' action='/hello'>
                                <h2>What would you like me to say?</h2>
                                <input name="message" type="text" >
                                <input type="submit" value="Submit"> 
                            </form>
                            ''' 
                message += '</body></html>'
                self.wfile.write(message)
            elif self.path.endswith('/new'):
                self.send_response(200);
                self.send_header('Content-type','text/html')
                self.end_headers()
                message = '<html><body>'
                message += 'Add a new restaurant!' 
                message += '''
                            <form method='POST' enctype='multipart/form-data' action='/restaurants/new'>
                                <h2>Enter name of the restaurant</h2>
                                <input name="restaurant_name" type="text" >
                                <input type="submit" value="Submit"> 
                            </form>
                            ''' 
                message += '</body></html>'
                self.wfile.write(message)
            elif self.path.endswith('/edit'):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                id = int(self.path.split('/')[2])
                q = session.query(Restaurant).get(id)
                message = '<html><body>'
                message += 'Renaming restaurant.' 
                message += '''
                            <form method='POST' enctype='multipart/form-data' action='/restaurant/''' + str(id) +'''/edit'>
                                <h2>Enter new name for ''' + q.name + '''</h2>
                                <input name="restaurant_name" type="text" >
                                <input type="submit" value="Submit"> 
                            </form>
                            ''' 
                message += '</body></html>'
                self.wfile.write(message)
            elif self.path.endswith('/delete'):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                id = int(self.path.split('/')[2])
                q = session.query(Restaurant).get(id)
                message = '<html><body>'
                message += 'Deleting restaurant.' 
                message += '''
                            <form method='POST' enctype='multipart/form-data' action='/restaurant/''' + str(id) +'''/delete'>
                                <h2>Type `YES` to confirm</h2>
                                <input name="delete" type="text" >
                                <input type="submit" value="Submit"> 
                            </form>
                            ''' 
                message += '</body></html>'
                self.wfile.write(message)
            else:
                pass 
        except IOError:
            self.send_error(404,'File not found %s' % self.path)


    def do_POST(self):
        try:
            if self.path.endswith('/hello'):
                self.send_response(301)
                self.end_headers()
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile,pdict)
                    messageContent = fields.get('message')
                    message = '<html><body>'
                    message += 'You wrote: ' + str(messageContent[0])
                    message += '''
                                <form method='POST' enctype='multipart/form-data' action='/hello'>
                                    <h2>What would you like me to say?</h2>
                                    <input name="message" type="text" >
                                    <input type="submit" value="Submit"> 
                                </form>
                                ''' 
                    message += '</body></html>'
                    self.wfile.write(message)
            elif self.path.endswith('/new'):
                self.send_response(301)
                self.end_headers()
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile,pdict)
                    messageContent = fields.get('restaurant_name')
                    newRestaurant = Restaurant(name = messageContent[0])
                    session.add(newRestaurant)
                    session.commit()
                    message = '<html><body>'
                    message += 'Added: ' + str(messageContent[0]) + ' to the restaurant database'
                    message += '</body></html>'
                    self.wfile.write(message)
            elif self.path.endswith('/edit'):
                self.send_response(301)
                self.end_headers()
                id = int(self.path.split('/')[2])
                q = session.query(Restaurant).get(id)
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile,pdict)
                    messageContent = fields.get('restaurant_name')
                    q.name = messageContent[0]
                    session.add(q)
                    session.commit()
                    message = '<html><body>'
                    message += 'Updated'
                    message += '</body></html>'
                    self.wfile.write(message)
            elif self.path.endswith('/delete'):
                self.send_response(301)
                self.end_headers()
                id = int(self.path.split('/')[2])
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile,pdict)
                    messageContent = fields.get('delete')
                    message = '<html><body>'                    
                    if messageContent[0] == 'YES':
                        q = session.query(Restaurant).get(id)
                        session.delete(q)
                        session.commit()
                        message += 'Deleted'
                    else:
                        message += 'Could not delete'
                    message += '</body></html>'
                    self.wfile.write(message)
        except IOError:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('',port),WebServerHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        server.socket.close()

if __name__ == "__main__":
    main()