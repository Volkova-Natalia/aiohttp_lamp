# aiohttp_lamp

Packaged WebSockets client to manage a lamp (using aiohttp).  

---
## Using

See example of using [project_sample](https://github.com/Volkova-Natalia/aiohttp_lamp/blob/main/project_sample).  

---
#### Install the application
The application is **not published**, so you should use link to the github repository:  
```
https://github.com/Volkova-Natalia/aiohttp_lamp/raw/master/dist/aiohttp_lamp-0.1.tar.gz
```

---
#### Create .env
If you want, you can define environment variables (see file [project_sample/.env.sample](https://github.com/Volkova-Natalia/aiohttp_lamp/blob/main/project_sample/.env.sample)):  
* DEBUG (default "True")  
* SERVER_HOST (default "127.0.0.1")  
* SERVER_PORT (default "9999")  

Or you can use any other way to define the variables.  
And you may not define them at all and use them by default.  

---
<br>

The client use WebSockets.  

You have to run server (WebSockets) on http://127.0.0.1:9999   
You can choose another host and port and define they as environment variables, but the client does not use https.  
Next, you can run the client.  
See example of the server [project_sample/src/server_example.py](https://github.com/Volkova-Natalia/aiohttp_lamp/blob/main/project_sample/src/server_example.py).  
Sample of using the client ([project_sample/src/main.py](https://github.com/Volkova-Natalia/aiohttp_lamp/blob/main/project_sample/src/main.py)):  
```python
my_lamp = Lamp(debug=DEBUG)
ws_client = WSClient(server_host=SERVER_HOST, server_port=SERVER_PORT, lamp=my_lamp)
ws_client.run()
```

<br>

---
## Lamp logic
Commands:  
1) ON - turn on the lamp  
1) OFF - turn off the lamp  
1) COLOR - change color of the lamp  

* You can send the command ON even if the lamp is turned on.  
* You can send the command OFF even if the lamp is turned off.  
* You can send the command ON after the command OFF - the command OFF does not shutdown the client.  
* You can change color of the lamp even if the lamp is turned off. When you turn on the lamp, its color will be new.  
* You can set black color even if the lamp is turned on.  
* The lamp color when the lamp is turned off can be anything - this is the future color of the lamp.  
* You can get the state of the lamp from its properties: **lamp.state** and **lamp.color**.  

See details [Lamp.pdf](https://github.com/Volkova-Natalia/aiohttp_lamp/blob/main/Lamp.pdf).  
