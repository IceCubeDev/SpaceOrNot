"""
   Copyright 2015 Ivan Dortulov

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

from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse


class Satellite(BaseHTTPRequestHandler):

	def do_GET(self):
		parsed_path = urlparse(self.path)
		message_parts = [
			'CLIENT VALUES:',
			'client_address=%s (%s)' % (self.client_address,
										self.address_string()),
			'command=%s' % self.command,
			'path=%s' % self.path,
			'real_path=%s' % parsed_path.path,
			'request_version=%s' % self.request_version,
			'',
			'SERVER VALUES:',
			'server_version=%s' % self.server_version,
			'sys_version=%s' % self.sys_version,
			'protocol_version=%s' % self.protocol_version,
			'',
			'HEADERS RECEIVED:',
		]
		
		for name, value in sorted(self.headers.items()):
			message_parts.append('%s=%s' % (name, value.rstrip()))
		message_parts.append('')
		message = '\r\n'.join(message_parts)
		self.send_response(200)
		self.end_headers()
		self.wfile.write(message.encode())
		return
