import http.server
import datetime
import HubController
import cgi
import socket, os 
from socketserver import BaseServer
from http.server import HTTPServer
from http.server import SimpleHTTPRequestHandler
from OpenSSL import SSL
from urllib.request import urlopen
from urllib.parse import urlparse, parse_qs
import ssl

Controller = HubController.HubController()

class HTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            self.log(self.path)
            if self.path   == "/get_door_status":
                responseText = Controller.PerformCommand(HubController.HubController.CMD_GET_DOOR_STATUS, None)
                self.send_valid_response(responseText)
                return
            elif self.path == "/get_light_status":
                responseText = Controller.PerformCommand(HubController.HubController.CMD_GET_LIGHT_STATUS, None)
                self.send_valid_response(responseText)
                return
            elif self.path == "/get_temperature_status":
                responseText = Controller.PerformCommand(HubController.HubController.CMD_GET_TEMPERATURE_STATUS, None)
                self.send_valid_response(responseText)
                return
            # TODO Using path.contains here is nasty.
            elif "/open_door" in self.path:
                query_components = parse_qs(urlparse(self.path).query)
                # TODO What if the value doesn't exist here? We should handle that.
                doorNumber = query_components["door_number"][0]
                # TODO Return an error if the door number is outside the correct range (1-4).
                print(str(doorNumber))

                # TODO The open door command return text should specify the door, and whether it was closed or opened.
                responseText = Controller.PerformCommand(HubController.HubController.CMD_OPEN_DOOR, doorNumber)
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
    server_address = ('', 8080)
    httpd = http.server.HTTPServer(server_address, HTTPRequestHandler)

    httpd.socket = ssl.wrap_socket(httpd.socket, certfile='./hub-http-server.pem', server_side=True)
    
    print('http server is running...')
    httpd.serve_forever()

#################################################################################
##### Starts the HTTP server which accepts commands from the Android phone. #####
#################################################################################
def main():
    StartServer()

if __name__ == "__main__":
    main()
