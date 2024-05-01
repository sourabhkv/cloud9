# accounts/urls.py  
from .ftp_server import start_ftp_server
import threading
  
# Ensure the FTP server starts only once by checking if the thread is already running  
if not any(thread.name == 'FtpServerThread' for thread in threading.enumerate()):  
    _server_thread = threading.Thread(target=start_ftp_server, name='FtpServerThread')  
    _server_thread.start()  

from django.urls import path
from . import views  

urlpatterns = [  
    path('signup/', views.signup_view, name='signup'),  
    path('login/', views.login_view, name='login'),  
    path('logout/', views.logout_view, name='logout'),
    path('delete_account/', views.delete_account, name='delete_account'),
]  

