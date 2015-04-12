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

from psycopg2 import *


class DBHelper(object):
	
	USERS_TABLE = "users"
	PICTURES_TABLE = "pictures"
	SPACES_TABLE = "spaces"
	
	def __init__(self, dbuser, dbpass, dbname):
	
		conn_string = "dbname=" + dbname + " dbuser=" + dbuser + " dbpass=" + dbpass 
		
		try:
			self.db_conn = psycopg2.connect(conn_string)
			self.cursor = self.db_conn.cursor()
		except psycopg2.Error as ex:
			print("[ERROR] Unable to connect to the database server: " + str(ex.args[1]))
			self.db_conn = None
			
		
	def register_user(self, user_fb_id, user_real_name):
		query = "INSERT INTO " + USERS_TABLE + " VALUES(%s, %s);"
		
		try:
			self.cursor = self.db_conn.cursor()
			self.cursor.execute(query, (user_fb_id, user_real_name))
		except psycopg2.Error as ex:
			print("[ERROR] Unable to insert data: " + str(ex.args[1]))
			return False
		else:
			self.cursor.close()
			self.cursor = None
			return True
