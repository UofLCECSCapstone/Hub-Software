import http.server
import datetime
import HubController

Controller = HubController.HubController()

class HTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            self.log(self.path)
            if self.path   == "/get_door_status":
                Controller.PushCommand(HubController.HubController.CMD_GET_DOOR_STATUS)
                responseText = "Current time: " + datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
                self.send_valid_response(responseText)
                return
            elif self.path == "/get_light_status":
                Controller.PushCommand(HubController.HubController.CMD_GET_LIGHT_STATUS)
                responseText = "Current time: " + datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
                self.send_valid_response(responseText)
                return
            elif self.path == "/get_temperature_status":
                Controller.PushCommand(HubController.HubController.CMD_GET_TEMPERATURE_STATUS)
                responseText = "Current time: " + datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
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


def StartServer():
    print("Server starting...")
    #ip and port of server
    server_address = ('127.0.0.1', 8080)
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
