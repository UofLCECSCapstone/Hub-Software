import http.server
import datetime
import HubController

class HTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            print(self.path)
            if self.path   == "/get_door_status":
                HubController.PushCommand(HubController.CMD_GET_DOOR_STATUS)
                self.send_response(200)
                self.send_header('Content-type','text/plain')
                self.end_headers()
                responseText = "Current time: " + datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
                print("Response: " + responseText)
                self.wfile.write(bytes(responseText, "utf-8"))
                return
            elif self.path == "/get_light_status":
                HubController.PushCommand(HubController.CMD_GET_LIGHT_STATUS)
                self.send_response(200)
                self.send_header('Content-type','text/plain')
                self.end_headers()
                responseText = "Current time: " + datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
                print("Response: " + responseText)
                self.wfile.write(bytes(responseText, "utf-8"))
                return
            elif self.path == "/get_temperature_status":
                HubController.PushCommand(HubController.CMD_GET_TEMPERATURE_STATUS)
                self.send_response(200)
                self.send_header('Content-type','text/plain')
                self.end_headers()
                responseText = "Current time: " + datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
                print("Response: " + responseText)
                self.wfile.write(bytes(responseText, "utf-8"))
                return
            else:
                self.send_error("TODO Throw some kind of undefined command error here.")
        except IOError:
            self.send_error(404, 'file not found')
        # TODO How do I handle other types of errors?

def StartServer():
    print("Server starting...")
    #ip and port of server
    #by default http server port is 80
    server_address = ('127.0.0.1', 80)
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