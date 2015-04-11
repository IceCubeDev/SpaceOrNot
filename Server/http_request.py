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

import re


class HttpRequest(object):
	
	def __init__(self, request_string):
		
		self.request_method = ""
		self.request_path = ""
		self.request_version = ""
		self.headers = {}
		
		self.processing = False
		
		self.from_string(request_string)
		
	def from_string(self, request_string):
		lines = request_string.split(b"\r\n")
		
		for line in lines:
			# This is the request line
			request_line = re.match(b"(.*) (.*) HTTP/(.*)", line)
			
			if request_line is not None:
				self.request_method = request_line.group(1).upper().decode()
				self.request_path = request_line.group(2).decode()
				self.request_version = request_line.group(3).decode()
				
				print(self.request_method, self.request_path, self.request_version)
				
			else:
				header = re.match(b"(.*): (.*)", line)
				if header is not None:
					self.headers[header.group(1).decode()] = header.group(2).decode()
					print(header.group(1).decode(), header.group(2).decode())
