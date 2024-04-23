from django.db import models  
from django.conf import settings  
import os  ,string
  
# Function to sanitize the email and create a user-specific folder path  
def user_directory_path(instance, filename):  
    # Clean up the email address to be used as a folder name  
    email = instance.uploader.email  
    return f'{email}/{filename}'  
  
class File(models.Model):  
    file = models.FileField(upload_to=user_directory_path)  
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  
    uploaded_at = models.DateTimeField(auto_now_add=True)  
