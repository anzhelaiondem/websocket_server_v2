# websocket_server_v2
## Summary
This program creates a publicly available websocket server that sends to connected clients, particularly to "WebSocket Test Client" extension, the right ascension (RA) and the declination (DEC) of the Moon every 10 seconds.

### Required packages
websockets (pip install websockets)\
asyncio\
logging\
ngrok from pyngrok (pip install pyngrok)

### Steps to follow
1. Before running websocket_server.py module, run requirements.txt by writing "pip install -r requirements.txt" to install websockets and pyngrok packages.
2. When running server.py, it returns _"Ngrok tunnel address: ws://ngrok.address"_ as an output.
3. Copy the websocket address and past it into the "WebSocket Test Client" extension:\
  . If you have already added the WebSocket Test Client extension into Chrom, then use this link:\
  chrome-extension://fgponpodhbmadfljofbimhhlengambbn/index.html \
  . If you have not added it into chrome, open this link to add:\
  https://chrome.google.com/webstore/detail/websocket-test-client/fgponpodhbmadfljofbimhhlengambbn/related?hl=en \
  then use the link mentioned above to use it.\
The picture should look like this:
<img width="600" alt="image" src="https://user-images.githubusercontent.com/82014669/119537994-b047ad00-bd9b-11eb-8307-47b98a7a7172.png">
 
4. After pressing "Open", the program will start providing the RA and DEC of the Moon every 10 seconds.\
The final picture should look like this:
<img width="600" alt="image" src="https://user-images.githubusercontent.com/82014669/119538613-572c4900-bd9c-11eb-9c00-52d0466dd726.png">
 
### Information about the program
_Client.log file:_ After running the program, it creates users.log file where the flow of the connected and/or disconnected clients is reflected.\
_Message from a client:_ The program does not react to any message sent from the client.\
_Stop the server:_ Once the websocket server has started, it can be stopped by closing/stopping the program.


### Additional information
_Average RA and DEC_ The obvious predictable behavior of RA and DEC was noticeable, so the average approach was taken as the basis for calculating the Moon coordinates. Rarely, but in some periods, the DEC may have significant deviations, but RA has constantly small deviations.





  
