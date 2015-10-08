from http.server import BaseHTTPRequestHandler
import datetime

class HTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith('.html'):
                self.send_response(200)

                self.send_header('Content-type','text/plain')
                self.end_headers()

                responseText = "Current time: " + datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
                print("Response: " + responseText)
                self.wfile.write(bytes(responseText, "utf-8"))
                return
        except IOError:
            self.send_error(404, 'file not found')