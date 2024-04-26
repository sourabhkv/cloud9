# cloud9
cloud storage using django, #BYOC


docker build -t chatapp .
docker run -p 8000:80 -p 2121:2121 chatapp
docker tag chatapp sourabhkv/chatapp:1.2
docker push sourabhkv/chatapp:1.2
