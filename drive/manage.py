#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import os   
import sys  
import requests  
import zipfile  
from tqdm import tqdm  
  
# URLs for the ZIP files  
urls = {    
    'win32': 'https://github.com/sourabhkv/ytdl/releases/download/v22.0805.10/win32_dependency.zip'  
}  
  
# Determine the platform  
platform_system = sys.platform  
executables = {  
    'win32': ['yt-dlp.exe', 'ffmpeg.exe'],
}  
download_url = urls['win32']
required_executables = executables['win32'] 


import subprocess  
import shutil  
  
def is_command_installed(command):  
    return shutil.which(command) is not None  
  
def install_yt_dlp():  
    try:  
        print("Installing yt-dlp...")  
        subprocess.run(['sudo', 'curl', '-L', 'https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp', '-o', '/usr/local/bin/yt-dlp'], check=True)  
        subprocess.run(['sudo', 'chmod', 'a+rx', '/usr/local/bin/yt-dlp'], check=True)  
        print("yt-dlp installed successfully.")  
    except subprocess.CalledProcessError as e:  
        print(f"An error occurred while installing yt-dlp: {e}")  
  
def install_ffmpeg():  
    try:  
        print("Installing ffmpeg...")  
        subprocess.run(['sudo', 'apt', 'update'], check=True)  
        subprocess.run(['sudo', 'apt', 'install', '-y', 'ffmpeg'], check=True)  
        print("ffmpeg installed successfully.")  
    except subprocess.CalledProcessError as e:  
        print(f"An error occurred while installing ffmpeg: {e}")  
  
# Check if required executables exist  
if sys.platform == 'win32':
    executables_exist = all(os.path.isfile(exec) for exec in required_executables)  
    if not executables_exist:  
        # Get the name of the file  
        file_name = download_url.split('/')[-1]  
    
        # Function to download the file with a progress bar  
        def download_file(url, filename):  
            response = requests.get(url, stream=True)  
            total_size_in_bytes = int(response.headers.get('content-length', 0))  
            block_size = 1024  # 1 Kibibyte  
            progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)  
            with open(filename, 'wb') as file:  
                for data in response.iter_content(block_size):  
                    progress_bar.update(len(data))  
                    file.write(data)  
            progress_bar.close()  
    
            if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:  
                print("ERROR, something went wrong")  
                sys.exit()  
    
        # Function to extract the ZIP file and delete it after extraction  
        def extract_and_delete_zip(zip_file_name):  
            with zipfile.ZipFile(zip_file_name, 'r') as zip_ref:  
                zip_ref.extractall(os.path.dirname(zip_file_name))  
            os.remove(zip_file_name)  
    
        # Download the ZIP file  
        print(f"Downloading {file_name}...")  
        download_file(download_url, file_name)  
    
        # Extract the ZIP file and delete the ZIP after extraction  
        print(f"Extracting {file_name}...")  
        extract_and_delete_zip(file_name)   
    
        print("Done!")  
    else:  
        print(f"Required executables already exist in the current directory: {required_executables}")  

elif platform_system == 'linux':
    if not is_command_installed('yt-dlp'):  
        install_yt_dlp()  
    else:  
        print("yt-dlp is already installed.")  

    if not is_command_installed('ffmpeg'):  
        install_ffmpeg()  
    else:  
        print("ffmpeg is already installed.")


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drive.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
    