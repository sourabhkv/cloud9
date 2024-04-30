# cloud9
cloud storage using django, #BYOC


docker build -t chatapp .<br>
docker run -p 8000:80 -p 2121:2121 chatapp<br>
docker tag chatapp sourabhkv/chatapp:1.6<br>
docker push sourabhkv/chatapp:1.6
