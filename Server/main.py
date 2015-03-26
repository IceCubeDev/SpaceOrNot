from http.server import HTTPServer
from satellite import *


def main():
	print("Hello, world!");
	
	server_address = (("localhost", 8999))
	handler_class = Satellite
	httpd = HTTPServer(server_address, handler_class)
	httpd.serve_forever()
	
	
if __name__ == "__main__":
	main()
