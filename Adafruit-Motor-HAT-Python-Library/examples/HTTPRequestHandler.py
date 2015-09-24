import http.server
import datetime
#import HubController
import DCTest
import cgi
import socket, os 
from socketserver import BaseServer
from http.server import HTTPServer
from http.server import SimpleHTTPRequestHandler
from OpenSSL import SSL
from urllib.request import urlopen
from urllib.parse import urlparse, parse_qs

Controller = DCTest.HubController()

class SecureHTTPServer(HTTPServer):
    def __init__(self, server_address, HandlerClass):
        BaseServer.__init__(self, server_address, HandlerClass)
        ctx = SSL.Context(SSL.SSLv23_METHOD)
        #server.pem's location (containing the server private key and
        #the server certificate).
        fpem = '/Desktop/SourceCode/Hub-Backend/Adafruit-Motor-HAT-Python-Library/examples/hub-http-server.pem'
        ctx.use_privatekey_file (fpem)
        ctx.use_certificate_file(fpem)
        self.socket = SSL.Connection(ctx, socket.socket(self.address_family,
                                                        self.socket_type))
        self.server_bind()
        self.server_activate()


class SecureHTTPRequestHandler(SimpleHTTPRequestHandler):
    def setup(self):
        self.connection = self.request
        self.rfile = socket._fileobject(self.request, "rb", self.rbufsize)
        self.wfile = socket._fileobject(self.request, "wb", self.wbufsize)


def test(HandlerClass = SecureHTTPRequestHandler,
         ServerClass = SecureHTTPServer):
    server_address = ('', 443) # (address, port)
    httpd = ServerClass(server_address, HandlerClass)
    sa = httpd.socket.getsockname()
    print ("Serving HTTPS on"), sa[0], "port", sa[1], "..."
    httpd.serve_forever()


if __name__ == '__main__':
    test()


class HTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            self.log(self.pacd /home/pi/Desktop/SourceCode/Hub-Backend/Adafruit-Motor-HAT-Python-Library/examplesth)
            if self.path   == "/get_door_status":
                responseText = Controller.PerformCommand(DCTest.HubController.CMD_GET_DOOR_STATUS)
                self.send_valid_response(responseText)
                return
            elif self.path == "/get_light_status":
                responseText = Controller.PerformCommand(DCTest.HubController.CMD_GET_LIGHT_STATUS)
                self.send_valid_response(responseText)
                return
            elif self.path == "/get_temperature_status":
                responseText = Controller.PerformCommand(DCTest.HubController.CMD_GET_TEMPERATURE_STATUS)
                self.send_valid_response(responseText)
                return

                        # TODO Using path.contains here is nasty.
            elif self.path == "/open_door":
                responseText = Controller.PerformCommand(DCTest.HubController.CMD_OPEN_DOOR)
                self.send_valid_response(responseText)
                return
            elif "/authenticate_device" in self.path:
                actual_auth_code = getCurrentAuthCode()
                
                query_components = parse_qs(urlparse(self.path).query)
                # TODO What if the value doesn't exist here? We should handle that.
                auth_code = query_components["auth_code"][0]
                print(auth_code)
                print(actual_auth_code)

                if auth_code == actual_auth_code:
                    responseText = "Success"
                else:
                    responseText = "Failure"

                self.send_valid_response(responseText)
                return
            else:
                self.send_error(400, "Unknown command supplied")
        except IOError:
            self.send_error(404, 'file not found')
        # TODO How do I handle other types of errors?

    def send_valid_response(self, responseText):
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        self.log("Response: " + responseText)
        self.wfile.write(bytes(responseText, "utf-8"))

    def log(self, message):
        print("HTTPRequestHandler::" + message)
 
    def get_time_string(self):
        return "Current time: " + datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')

def getCurrentAuthCode():
    authCode = urlopen("http://127.0.0.1:8081/get_current_auth_token").read().decode("utf-8")
    return authCode

def StartServer():
    print("Server starting...")
    #ip and port of server
    server_address = ('', 8050)
    httpd = http.server.HTTPServer(server_address, HTTPRequestHandler)
    print('http server is running...')
    httpd.serve_forever()

#################################################################################
##### Starts the HTTP server which accepts commands from the Android phone. #####
#################################################################################
def main():
    StartServer()

if __name__ == "__main__":
    main()
