import time
import threading, hashlib
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from django.contrib.auth.models import User
def hashed_dir(s):
    # Create a hash object
    hash_object = hashlib.sha256(s.encode())

    # Get the hexadecimal representation of the hash
    hex_dig = hash_object.hexdigest()

    return hex_dig

import threading  
from pyftpdlib.authorizers import DummyAuthorizer  
from pyftpdlib.handlers import FTPHandler  
from pyftpdlib.servers import FTPServer  
  
# Instantiate a dummy authorizer to manage 'virtual' users  
authorizer = DummyAuthorizer()  
  
# Define the FTP handler class  
handler = FTPHandler  
handler.passive_ports = range(50000, 50011)  
  
# Instantiate FTP server  
def setup_ftp_server():  
    # Define the server address and the server port  
    server = FTPServer(('0.0.0.0', 2121), handler)  
      
    # Set the authorizer for the handler  
    handler.authorizer = authorizer  
      
    # Start the FTP server in a separate thread  
    server_thread = threading.Thread(target=server.serve_forever)  
    server_thread.daemon = True  # Allow server thread to exit when main thread does  
    server_thread.start()  
  
# This function could be called to initialize the FTP server,   
# for example, from Django's AppConfig.ready() method.  
def start_ftp_server():  
    setup_ftp_server()  
  
# Example usage in Django's AppConfig:  
# from django.apps import AppConfig  
#  
# class MyFtpAppConfig(AppConfig):  
#     name = 'my_ftp_app'  
#  
#     def ready(self):  
#         # Start the FTP server when Django starts  
#         start_ftp_server()  