
# Nears Server
Doctorize version of nears server for production




##  Run on a VM  
Clone the project  

~~~bash  
 git clone https://github.com/StanleyAbotsikuma/dockerize_near_server.git
~~~

Go to the project directory  

~~~bash  
cd dockerize_near_server
~~~

Build the Dockerfile  

~~~bash  
docker build -t near_server .
~~~

Run the dockerfile 

~~~bash  
docker run -d -p 8080:8000 near_server
~~~  

## Other Commands


~~~bash  
  // delete dir
  rm -rf  dockerize_near_server
  //test 
  curl http://173.230.136.205:8080
~~~

 
