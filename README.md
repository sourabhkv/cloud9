# cloud9
cloud storage using django, #BYOC

# cloud9
cloud storage using django, #BYOC
<p align="center">
<img alt="Windows" src="https://img.shields.io/badge/Windows-0078D6?style=flat&logo=windows&logoColor=white" ></a>
</a>
</p>

## Highlights
- Private
- Suitable for home network
- yt-dlp, ffmpeg powered
- built in media download automator
- FTP support

### Automation
Cloud9 is capable of downloading video/audio from internet. [Read more](https://github.com/yt-dlp/yt-dlp).<br>
Apart from video/audio downloading other media format such as images/docs can be done by uploading `URL_DOWNLOAD.txt` file with media URL in each line, once uploaded , files be will downloaded in same directory as `URL_DOWNLOAD.txt` file resides. Remember `URL_DOWNLOAD.txt` wont be deleted once its purpose is over.

## Building
```shell
docker build -t <name> .

docker run -p 8000:80 -p 2121:2121 <name>
```

## Configs
### Maximum upload files
Max no. of files upload limit. Default 500
```python
#settings.py
DATA_UPLOAD_MAX_NUMBER_FILES = 500
```

### User folder naming
Folder name hashed by default using SHA-256
```python
def hashed_dir(s):
    # Create a hash object
    hash_object = hashlib.sha256(s.encode())

    # Get the hexadecimal representation of the hash
    hex_dig = hash_object.hexdigest()

    return hex_dig
```
Algo - SHA-256, SHA-384, SHA-512

foldername same as username. **NOT RECOMMENDED**
```python
def hashed_dir(s):
    return s
```

### FTP support
**Only for local network use**
default port is `2121` instead of `21` because of root permission, port clashing<br>
FTP URL - `127.0.0.1:2121` (configurable)
*NOTE access FTP in forced passive mode using FTP clients like [filezilla](https://filezilla-project.org/), [Winscp](https://winscp.net/eng/download.php), or even explorer.exe<br>
ftp.exe does not support passive ports properly even after enabling passive ports, allowing foreign IP address*<br>

![Screenshot 2024-04-30 201650](https://github.com/sourabhkv/cloud9/assets/55890376/751cfe89-7928-4d10-a3ef-ed60e285067b)


## Workarounds
`setup_ftp_server` can be modified to support [SFTP](https://pyftpdlib.readthedocs.io/en/latest/tutorial.html#ftps-ftp-over-tls-ssl-server)<br>
storage sense - capping storage limit for users<br>
Sharing at network, user level

docker build -t chatapp .<br>
docker run -p 8000:80 -p 2121:2121 chatapp<br>
docker tag chatapp sourabhkv/chatapp:1.6<br>
docker push sourabhkv/chatapp:1.6


docker build -t chatapp .<br>
docker run -p 8000:80 -p 2121:2121 chatapp<br>
docker tag chatapp sourabhkv/chatapp:1.6<br>
docker push sourabhkv/chatapp:1.6
