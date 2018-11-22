from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

class WebServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/hello") :
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
            else:
                pass 
        except IOError:
            self.send_error(404,'File not found %s' % self.path)


    def do_POST(self):
        try:
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
                print message
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