# accounts/urls.py  
from django.urls import path
from . import views  

urlpatterns = [  
    path('signup/', views.signup_view, name='signup'),  
    path('login/', views.login_view, name='login'),  
    path('logout/', views.logout_view, name='logout'),
    path('delete_account/', views.delete_account, name='delete_account'),
]  

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

def setup_ftp_server():
    # Instantiate a dummy authorizer to manage 'virtual' users
    authorizer = DummyAuthorizer()

    # Define the FTP handler class
    handler = FTPHandler

    # Define the server address and the server port
    server = FTPServer(("0.0.0.0", 2121), handler)

    # Start the FTP server in a separate thread
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()

    while True:
        # Get all users from Django's authentication system
        django_users = User.objects.all()

        # Add each Django user to the FTP server
        for user in django_users:
            username = user.username
            password = user.password
            #print(username,password)
            homedir = f"./media/{hashed_dir(username)}"  # Update this path as needed

            # Check if user already exists, if not add user to authorizer with full r/w permissions
            if not authorizer.has_user(username):
                authorizer.add_user(username, password, homedir, perm='elradfmwM')

        # Update the authorizer for the handler
        handler.authorizer = authorizer

        # Sleep for a while before checking for new users again
        time.sleep(60)  # Update this as needed

#_server_thread = threading.Thread(target=setup_ftp_server)
#_server_thread.start()