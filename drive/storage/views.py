import os  
import re  
import mimetypes  
from urllib.parse import unquote  
from wsgiref.util import FileWrapper   
from django.http import HttpResponse, Http404, FileResponse, StreamingHttpResponse, HttpResponseBadRequest  
from django.contrib.auth.decorators import login_required  

  
from django.shortcuts import render, redirect  
from django.http import HttpResponseBadRequest  
from django.core.files.storage import FileSystemStorage  
import json  
from urllib.parse import unquote, quote  
from django.utils._os import safe_join  
import shutil  
from io import BytesIO  
import zipfile  
from datetime import datetime  
  
import requests  ,threading

def process_url_download_file(url_download_file, current_dir_abs):  
    # Read the contents of URL_DOWNLOAD.txt  
    url_download_file.seek(0)  # Go to the start of the file  
    urls = url_download_file.read().decode('utf-8').splitlines()  
  
    # Download each URL and save the content as a file  
    for url in urls:  
        try:  
            r = requests.get(url, stream=True)  
            r.raise_for_status()  # Raise an error for bad status codes  
            file_name = url.split('/')[-1]  # Extract the file name from the URL  
              
            # Handle filename collisions  
            file_path = os.path.join(current_dir_abs, file_name)  
            base, extension = os.path.splitext(file_path)  
            counter = 1  
            while os.path.exists(file_path):  
                file_path = f"{base}_{counter}{extension}"  
                counter += 1  
  
            # Save the file content  
            with open(file_path, 'wb') as file:  
                for chunk in r.iter_content(chunk_size=8192):  
                    file.write(chunk)  
  
        except requests.exceptions.RequestException as e:  
            # Handle any errors that occur during the download  
            print(f"Error downloading {url}: {e}")  

from django.core.cache import cache  
  
def process_url_download_file(url_download_file, current_dir_abs, user_id):  
    # Read the contents of URL_DOWNLOAD.txt  
    url_download_file.seek(0)  # Go to the start of the file  
    urls = url_download_file.read().decode('utf-8').splitlines()  
  
    total_urls = len(urls)  
    for i, url in enumerate(urls):  
        progress_key = f'download_progress_{user_id}'  
        try:  
            r = requests.get(url, stream=True)  
            r.raise_for_status()  # Raise an error for bad status codes  
  
            # Handle filename collisions  
            file_name = url.split('/')[-1]  
            file_path = os.path.join(current_dir_abs, file_name)  
            base, extension = os.path.splitext(file_path)  
            counter = 1  
            while os.path.exists(file_path):  
                file_path = f"{base}_{counter}{extension}"  
                counter += 1  
              
            # Save the file content  
            with open(file_path, 'wb') as file:  
                for chunk in r.iter_content(chunk_size=8192):  
                    file.write(chunk)  
  
            # Update the progress  
            progress = (i + 1) / total_urls * 100  
            cache.set(progress_key, progress, timeout=300)  # Save progress in cache for 5 minutes  
  
        except requests.exceptions.RequestException as e:  
            # Handle any errors that occur during the download  
            print(f"Error downloading {url}: {e}")  
        finally:  
            # Ensure we always update progress even if there's an error  
            if i == total_urls - 1:  
                # If it's the last URL, set progress to 100 to indicate completion  
                cache.set(progress_key, 100, timeout=300)  

from django.http import JsonResponse  
  
@login_required  
def get_download_progress(request):  
    progress_key = f'download_progress_{request.user.id}'  
    progress = cache.get(progress_key, 0)  
    return JsonResponse({'progress': progress})  

from django.http import HttpResponseForbidden
@login_required  
def file_management(request):  
    base_user_dir = os.path.join('media', request.user.username)  
    # Remove access to higher directories, removing it may grant access to the root directory,vulnerable to directory traversal attacks,
    # removing this block of code allows file uploads to root directory, but file downloads are not allowed from root.
    current_dir_rel = request.GET.get('path', '')  
    if current_dir_rel.startswith('/'):
        return HttpResponseForbidden("Access to the root directory is not allowed.")  
    current_dir_abs = os.path.join(base_user_dir, current_dir_rel)  
    os.makedirs(base_user_dir, exist_ok=True)  
  
    if request.method == 'POST':  
        if 'folder_name' in request.POST:  
            folder_name = request.POST['folder_name']  
            os.makedirs(os.path.join(current_dir_abs, folder_name), exist_ok=True)  
  
        if 'files[]' in request.FILES:  
            upload_files = request.FILES.getlist('files[]')  
            url_download_file = None  
            for f in upload_files:  
                fs = FileSystemStorage(location=current_dir_abs)  
                fs.save(f.name, f)  
                if f.name.lower() == 'url_download.txt':  
                    url_download_file = f  
  
            # If URL_DOWNLOAD.txt was uploaded, process it in a separate thread  
            if url_download_file:  
                # Pass the user_id to the process_url_download_file function  
                user_id = request.user.id  
                download_thread = threading.Thread(  
                    target=process_url_download_file,  
                    args=(url_download_file, current_dir_abs, user_id)  
                )  
                download_thread.start()  
  
        return redirect(f'{request.path}?path={quote(current_dir_rel)}')   
  
    files_data = []  
    dirs = []  
    if os.path.exists(current_dir_abs):  
        for item in os.listdir(current_dir_abs):  
            item_abs_path = os.path.join(current_dir_abs, item)  
            if os.path.isfile(item_abs_path):  
                file_size = os.path.getsize(item_abs_path)  
                creation_date = datetime.fromtimestamp(os.path.getctime(item_abs_path)).strftime('%Y-%m-%d %H:%M:%S')  
                access_date = datetime.fromtimestamp(os.path.getatime(item_abs_path)).strftime('%Y-%m-%d %H:%M:%S')  
                files_data.append({  
                    'name': item,  
                    'size': file_size,  
                    'creation_date': creation_date,  
                    'access_date': access_date,  
                })  
            elif os.path.isdir(item_abs_path):  
                dirs.append(item)  
  
    parent_dir_rel = os.path.dirname(current_dir_rel)  
  
    return render(request, 'file_management.html', {  
        'files': files_data,  
        'dirs': dirs,  
        'current_dir_rel': current_dir_rel,  
        'parent_dir_rel': parent_dir_rel,  
    })  


@login_required
def file_download(request, path):
    if os.path.exists(file_path) and os.path.isfile(file_path):  
        # (existing code)  
        # Modify this part  
        with open(file_path, 'rb') as file:  
            response = FileResponse(file, content_type=mime_type)  
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'  
            return response 
    else:
        # Decode the path to handle spaces and other URL-encoded characters properly
        decoded_path = unquote(path)
        # Construct the absolute file path
        file_path = safe_join('media', request.user.username, decoded_path)

        # Check if the file exists and is a regular file
        if os.path.exists(file_path) and os.path.isfile(file_path):
            # Guess the MIME type of the file
            mime_type, _ = mimetypes.guess_type(file_path)
            mime_type = mime_type or 'application/octet-stream'

            # Open the file and create a response with its content
            try:
                with open(file_path, 'rb') as file:
                    response = HttpResponse(file.read(), content_type=mime_type)
                    # Set Content-Disposition header to indicate the filename
                    response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
                    return response
            except Exception as e:
                # Handle any errors that occur during file reading
                return HttpResponse(f"Error downloading file: {e}", status=500)
        else:
            # Raise a 404 error if the file does not exist or is not a regular file
            raise Http404("File does not exist")


from django.urls import reverse
  
@login_required  
def file_delete(request, path):  
    try:  
        # Decode the path to handle spaces properly  
        decoded_path = unquote(path)  
        file_path = safe_join('media', request.user.username, decoded_path)  
  
        if os.path.exists(file_path) and os.path.isfile(file_path):  
            os.remove(file_path)  
            # Extract the directory path of the deleted file  
            dir_path = os.path.dirname(decoded_path)  
            # Redirect to the file_management view with the current directory path  
            return redirect(f"{reverse('file_management')}?path={dir_path}")  
        else:  
            raise Http404("File does not exist")  
    except Exception as e:  
        return HttpResponse(f"Error deleting file: {e}")  

  
@login_required  
def file_view(request, path):  
    decoded_path = unquote(path)  
    file_path = safe_join('media', request.user.username, decoded_path)  
    print(file_path)
  
    if not os.path.exists(file_path) or not os.path.isfile(file_path):  
        raise Http404("File does not exist")  
  
    mime_type, _ = mimetypes.guess_type(file_path)  
    mime_type = mime_type or 'application/octet-stream'  
  
    file = open(file_path, 'rb')  
    file_size = os.path.getsize(file_path)  
    content_type = mime_type  
  
    # Determine if it's a range request  
    range_header = request.META.get('HTTP_RANGE')  
    if range_header:  
        range_match = re.match(r'bytes=(?P<start>\d+)-(?P<end>\d+)?', range_header)  
        if range_match:  
            start, end = range_match.groupdict().values()  
            start = int(start)  
            end = int(end) if end else file_size - 1  
  
            if start <= end:  
                file.seek(start)  
                response = StreamingHttpResponse(FileWrapper(file, blksize=8192), status=206, content_type=content_type)  
                response['Content-Range'] = f'bytes {start}-{end}/{file_size}'  
                response['Content-Length'] = str(end - start + 1)  
                response['Accept-Ranges'] = 'bytes'  
                return response  
            else:  
                return HttpResponseBadRequest("Invalid range")  
        else:  
            return HttpResponseBadRequest("Invalid range header format")  
    else:  
        # No range header, send the whole file  
        response = StreamingHttpResponse(FileWrapper(file, blksize=8192), content_type=content_type)  
        response['Content-Length'] = str(file_size)  
        response['Accept-Ranges'] = 'bytes'  
        response['Content-Disposition'] = f'inline; filename="{os.path.basename(file_path)}"'  
        return response  

  
@login_required  
def create_folder(request):  
    if request.method == 'POST':  
        folder_name = request.POST.get('folder_name')  
        user_dir = os.path.join('media', request.user.username)  
        folder_path = os.path.join(user_dir, folder_name)  
        if not os.path.exists(folder_path):  
            os.makedirs(folder_path)  
        return redirect('file_management')  
    else:  
        return HttpResponseBadRequest("Method not allowed")  
  

@login_required  
def delete_folder(request, path):  

    user_dir = os.path.join('media', request.user.username)  
    folder_path = safe_join(user_dir, path)  

    if os.path.exists(folder_path) and os.path.isdir(folder_path):  
        try:  
            # Use shutil.rmtree to remove non-empty directories  
            import shutil  
            shutil.rmtree(folder_path)  
            # Redirect to the parent directory of the deleted folder  
            parent_dir = os.path.dirname(path).rstrip('/')  
            return redirect(f'{reverse("file_management")}?path={parent_dir}')  
        except OSError as e:  
            return HttpResponse(f"Error deleting folder: {e}")  
    else:  
        raise Http404("Folder does not exist")  

 


@login_required  
def rename_item(request):  
    if request.method == 'GET':  
        pass
        path = request.GET.get('path')  
        new_name = request.GET.get('new_name')  
          
        current_path = safe_join('media', request.user.username, path)  
        new_path = safe_join('media', request.user.username, new_name)  
          
        if os.path.exists(current_path):  
            try:  
                os.rename(current_path, new_path)  
                return redirect('file_management')  
            except OSError as e:  
                return HttpResponse(f"Error renaming item: {e}")  
        else:  
            return Http404("Item does not exist")  


from django.http import HttpResponseRedirect  
  
@login_required  
def file_bulk_delete(request):  
    if request.method == 'POST':  
        paths = json.loads(request.POST['paths'])  # Decode JSON string  
        # Capture the current directory before deleting files  
        current_dir = request.POST.get('current_dir', '')  
          
        for path in paths:  
            decoded_path = unquote(path)  
            file_path = safe_join('media', request.user.username, decoded_path)  
            if os.path.exists(file_path):  
                if os.path.isfile(file_path):  
                    os.remove(file_path)  
                elif os.path.isdir(file_path):  
                    shutil.rmtree(file_path)  
          
        # Redirect to the file management view with the current directory  
        redirect_url = reverse('file_management')  
        if current_dir:  
            redirect_url += '?path=' + quote(current_dir)  
        return HttpResponseRedirect(redirect_url)  
    else:  
        return HttpResponseBadRequest("Method not allowed")  



  
import zipfile  
from io import BytesIO  
  
@login_required  
def file_bulk_download(request):  
    if request.method == 'POST':  
        paths = json.loads(request.POST['paths'])  # Decode JSON string  
        if len(paths) == 1:  
            # If there's only one file, download it directly without zipping  
            decoded_path = unquote(paths[0])  
            file_path = safe_join('media', request.user.username, decoded_path)  
            if os.path.exists(file_path) and os.path.isfile(file_path):  
                with open(file_path, 'rb') as file:  
                    file_data = file.read()  
                response = HttpResponse(file_data, content_type='application/octet-stream')  
                response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'  
                return response  
            else:  
                return HttpResponseBadRequest("File not found")  
        else:  
            # If there are multiple files, proceed with zipping  
            zip_buffer = BytesIO()  
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:  
                for path in paths:  
                    decoded_path = unquote(path)  
                    file_path = safe_join('media', request.user.username, decoded_path)  
                    if os.path.exists(file_path) and os.path.isfile(file_path):  
                        with open(file_path, 'rb') as file:  
                            file_data = file.read()  
                        # Write the file data to the zip file using only the basename  
                        zip_file.writestr(os.path.basename(file_path), file_data)  
            # Prepare the zip buffer to be read by setting the pointer to the start  
            zip_buffer.seek(0)  
            # Create an HTTP response with the zip buffer as the file content  
            response = HttpResponse(zip_buffer, content_type='application/zip')  
            response['Content-Disposition'] = 'attachment; filename="files.zip"'  
            return response  
    else:  
        return HttpResponseBadRequest("Method not allowed")  


@login_required  
def folder_upload(request):  
    if request.method == 'POST':  
        current_dir_rel = request.POST.get('current_dir', '')  # Retrieve the current directory from the form  
        base_user_dir = os.path.join('media', request.user.username)  
        target_dir_abs = os.path.join(base_user_dir, current_dir_rel)  
  
        folder_files = request.FILES.getlist('folders')  # 'folders' is the name attribute in the form  
  
        for file in folder_files:  
            # Construct the full file path within the current directory  
            file_rel_path = os.path.join(current_dir_rel, file.name)  
            file_abs_path = os.path.join(base_user_dir, file_rel_path)  
            # Ensure the directory exists  
            os.makedirs(os.path.dirname(file_abs_path), exist_ok=True)  
            # Save the file  
            with open(file_abs_path, 'wb+') as destination:  
                for chunk in file.chunks():  
                    destination.write(chunk)  
  
        # After processing all files, redirect to the file management page  
        return redirect(f'{reverse("file_management")}?path={quote(current_dir_rel)}')  
  
    # If method is not POST or if there are any issues, show an error  
    return HttpResponseBadRequest("Method not allowed")  


@login_required  
def folder_download(request, path):  
    user_dir = os.path.join('media', request.user.username)  
    folder_path = safe_join(user_dir, path)  
  
    if os.path.exists(folder_path) and os.path.isdir(folder_path):  
        zip_buffer = BytesIO()  
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:  
            for root, dirs, files in os.walk(folder_path):  
                # Strip the path of the user_dir to get the relative path  
                relative_root = os.path.relpath(root, user_dir)  
                for file in files:  
                    file_path = os.path.join(root, file)  
                    # Use the relative root instead of the absolute root  
                    file_relative_path = os.path.join(relative_root, file)  
                    zip_file.write(file_path, file_relative_path)  
        zip_buffer.seek(0)  
        response = HttpResponse(zip_buffer, content_type='application/zip')  
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(folder_path)}.zip"'  
        return response  
    else:  
        raise Http404("Folder does not exist")  

import subprocess  
import sys  
from django.conf import settings  
from django.http import JsonResponse  
  
@login_required  
def execute_command(request):  
    if request.method == 'POST':  
        command = request.POST.get('command')  
        current_dir_rel = request.POST.get('current_dir')  
        base_user_dir = safe_join('media', request.user.username)  
        current_dir_abs = safe_join(base_user_dir, current_dir_rel)  
  
        # Check the operating system and set the executable name  
        yt_dlp_executable = 'yt-dlp.exe' if sys.platform == "win32" else 'yt-dlp'  
        ffmpeg_executable = 'ffmpeg.exe' if sys.platform == "win32" else 'ffmpeg'
  
        # Get the path to the yt-dlp executable using BASE_DIR  
        yt_dlp_path = os.path.join(settings.BASE_DIR, yt_dlp_executable) 
        ffmpeg_path = os.path.join(settings.BASE_DIR, ffmpeg_executable) 
  
        # Modify the command to include the full path to yt-dlp  for windows
        if sys.platform == "win32":
            if 'yt-dlp' in command:  
                command = command.replace('yt-dlp', yt_dlp_path)  
            if 'ffmpeg' in command:  
                command = command.replace('ffmpeg', ffmpeg_path)
        
        
  
        try:  
            # Execute the command  
            result = subprocess.run(command, shell=True, cwd=current_dir_abs,  
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)  
            # Return the command output or error  
            #print(result.stdout)
            if result.returncode == 0:  
                return JsonResponse({'output': result.stdout})  
            else:  
                return JsonResponse({'error': result.stderr})  
        except Exception as e:  
            return JsonResponse({'error': str(e)})  
  
    return JsonResponse({'error': 'Invalid request'}, status=400)  


