import http.server
import datetime
import HubController
import cgi
from urllib.request import urlopen
from urllib.parse import urlparse, parse_qs

Controller = HubController.HubController()

class HTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            self.log(self.path)
            if self.path   == "/get_door_status":
                responseText = Controller.PerformCommand(HubController.HubController.CMD_GET_DOOR_STATUS)
                self.send_valid_response(responseText)
                return
            elif self.path == "/get_light_status":
                responseText = Controller.PerformCommand(HubController.HubController.CMD_GET_LIGHT_STATUS)
                self.send_valid_response(responseText)
                return
            elif self.path == "/get_temperature_status":
                responseText = Controller.PerformCommand(HubController.HubController.CMD_GET_TEMPERATURE_STATUS)
                self.send_valid_response(responseText)
                return
                        # TODO Using path.contains here is nasty.
            elif self.path == "/open_door":
                responseText = Controller.PerformCommand(HubController.HubController.CMD_OPEN_DOOR)
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
