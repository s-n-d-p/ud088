from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

class WebServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith("/hello") :
            self.send_response(200);
            self.send_header('Content-type','text/html')
            self.end_headers()
            message = '<html><body>Hello!</body></html>'
            self.wfile.write(message)
        else:
            self.send_error(404,'File not found %s' % self.path)

    def do_post(self):
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