"""
   Copyright 2015 - Ivan Dortulov

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from http_request import HttpRequest
from queue import Queue
import urllib.parse
import os
import re


class RequestHandler(object):
	
	def __init__(self, server, client_socket, client_address):
		print("[DEBUG] Handler created for %s." % str(client_address))
		self.server = server
		self.socket = client_socket
		self.client_address = client_address
		
		self.input_buffer = b""
		self.output_buffer = b""
		
		self.request_queue = Queue()
		self.current_request = None
		
		self.should_close = False
		
	def on_data_received(self, data):
		print("[DEBUG] Processing data from %s." % str(self.client_address))
		self.input_buffer += data
		
		idx = self.input_buffer.find(b"\r\n\r\n")
		if idx >= 0:
			print("[DEBUG] Detected request from %s. " % str(self.client_address))
			
			request_string = self.input_buffer[:idx + 4]
			self.input_buffer = self.input_buffer[idx + 4:]
			
			request = HttpRequest(request_string)
			self.request_queue.put(request)
	
	def init_request(self, request):
		print("[DEBUG] Initializing request from %s.", str(self.client_address))
		
		if request.request_method == "GET" or request.request_method == "POST":
			print("[DEBUG] Request from %s for %s." % (str(self.client_address),
				request.request_path))
			
			# We are registering a user
			if request.request_path.find("/register") == 0:
				print("[DEBUG] %s is registering a user." % str(self.client_address))
				
				idx = request.request_path.find("?")
				if idx >= 0:
					raw = request.request_path[idx + 1:].split("&")
					for p in raw:
						param = re.match("(.*)=(.*)", urllib.parse.unquote(p))
						print(param.group(1), param.group(2))
						
						cursor = self.server.db_connection.cursor()
						cur.execute("""SELECT 1 FROM users WHERE fb_id = """)
					
		self.current_request = request
	
	def process_current_request(self):
		if self.current_request is None:
			if not self.request_queue.empty():
				print("[DEBUG] Processing next request from %s." % str(self.client_address))
				request = self.request_queue.get()
				request.processing = True
				self.init_request(request)
		else:
			if self.current_request.processing:
				self.process_request()
			else:
				print("[DEBUG] Request from %s processed." % str(self.client_address))
				del self.current_request
				self.current_request = None
				
	def process_request(self):
		pass
