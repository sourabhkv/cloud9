from django.shortcuts import render  
from django.contrib.auth.decorators import login_required  
import os, math, hashlib

def get_folder_size(folder_path):
    total = 0
    for path, dirs, files in os.walk(folder_path):
        for f in files:
            fp = os.path.join(path, f)
            total += os.path.getsize(fp)
    return total

def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])

def hashed_dir(s):
    # Create a hash object
    hash_object = hashlib.sha256(s.encode())

    # Get the hexadecimal representation of the hash
    hex_dig = hash_object.hexdigest()

    return hex_dig

@login_required  
def home(request):  
    # Get the size of the user's folder
    user_folder = os.path.join('media', hashed_dir(str(request.user.username)))
    folder_size = get_folder_size(user_folder)
    folder_size = convert_size(folder_size)

    context = {
        'user': request.user,
        'folder_size': folder_size,
        'hashed_password': request.user.password
    }  
    return render(request, 'home.html', context)

