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

import socket
import select
import errno
import sys
import time
import os
from request_handler import RequestHandler


class Satellite(object):

	CHUNK_SIZE = 1024

	def __init__(self):
		
		self.server_address = ()
		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_socket.setblocking(False)
		
		self.connections = []
		
		self.input_list = [self.server_socket]
		self.output_list = []
		
		self.running = False
		
		path = os.path.dirname(os.path.realpath(__file__))
		self.server_variables = {"document_root": path}
		
	def bind_server(self, server_address, server_port):
		self.server_address = (server_address, server_port)
		
		try:
			self.server_socket.bind(self.server_address)
			self.server_socket.listen(5)
		except socket.error as ex:
			print("[ERROR] The server is taking a selfie: ", str(ex.args[1]))
		
			sys.exit(-1)
		else:
			print("[DEBUG] Listening on %s." % str(self.server_address))
			self.running = True
			
	def run_server(self):
		while self.running:
			(read, write, error) = select.select(self.input_list, 
				self.output_list, self.input_list, 0)
			
			for conn in self.connections:
				conn.process_current_request()
				
			for read_sock in read:
				if read_sock is self.server_socket:
					# New connection
					try:
						(client_socket, client_address) = self.server_socket.accept()
					except socket.error as ex:
						print("[WARN] Unable to accept connection.")
					else:
						print("[DEBUG] Connection accepted.", 
							client_address)
						
						client_socket.setblocking(False)
						self.input_list.append(client_socket)
					
						handler = RequestHandler(self, client_socket, client_address)
						self.connections.append(handler)
					
				else:
					# Data is being received
					conn = self.find_connection(read_sock)
					
					if conn is None:
						print("[WARN] Unbound socket.")
						self.close_socket(read_sock)
						
					try:
						recv_data = read_sock.recv(Satellite.CHUNK_SIZE)
					except socket.error as ex:
						error = ex.args[0]
						
						if error == errno.EAGAIN or error == errno.EWOULDBLOCK:
							print("[DEBUG] EAGAIN/EWOULDBLOCK on %s." % 
								conn.client_address)
							continue
						
						print("[WARN] Error receiving data: ", str(ex.args[1])) 
					else:
						if len(recv_data) == 0:
							self.close_connection(conn)
							
						else:
							print("[DEBUG] Received %d bytes of data from %s" %
								(len(recv_data), conn.client_address))
							conn.on_data_received(recv_data)
							
			for error_sock in error:
				self.close_socket(error_sock)
				print("[WARN] Socket error.")
				self.close_socket(error_sock)
				
			for conn in self.connections:
				if len(conn.output_buffer) > 0:
					try:
						data = conn.output_buffer[:Satellite.CHUNK_SIZE]
						sent = conn.socket.send(data)
					except socket.error as ex:
						print("[WARN] Error receiving from %d", 
							conn.client_address)
					else:
						print("[DEBUG] Received %d bytes from %s.",
							(sent, conn.client_address))		
				elif conn.should_close:
					self.close_connection(conn)
					
			time.sleep(0.050)
	
	def find_connection(self, sock):
		for conn in self.connections:
			if conn.socket is sock:
				return conn 
		
		return None	
	
	def close_connection(self, conn):
		print("[DEBUG] Closing connection %s." % str(conn.client_address))
		self.close_socket(conn.socket)
		
		if conn in self.connections:
			self.connections.remove(conn)
			
		del conn
	
	def close_socket(self, sock):
		conn = self.find_connection(sock)
		if conn is not None:
			print("[DEBUG] Closing socket.")
	
			if sock in self.input_list:
				self.input_list.remove(sock)
		
			if sock in self.output_list:
				self.output_list.remove(sock)
			
			try:
				sock.shutdown(socket.SHUT_RD | socket.SHUT_WR)
				sock.close()
			except socket.error as ex:
				print("[WARN] Unable to close socket.")
			else:
				print("[DEBUG] Socket closed.")
