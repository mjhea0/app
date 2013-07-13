var worker_code = "\
function initialize_websocket(host,port,uri)\
{\
  var ws = new WebSocket('ws://' + host + ':' + port + uri);\
  ws.onmessage = function(evt) { postMessage(evt.data) };\
  ws.onclose = function(evt) { postMessage('Connection closed'); };\
  ws.onopen = function(evt) { postMessage('Connection opened'); };\
}\
\
onmessage = function (event)\
{\
  if(event.data=='init')\
    initialize_websocket('54.214.125.115',8888,'/web');\
  postMessage('Hi ' + event.data);\
}";
  //ws.send('something');
  //ws.close();