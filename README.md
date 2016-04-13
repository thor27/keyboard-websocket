# keyboard-websocket
Read evdev device and send to websocket

hardware_app.py: Read device from evdev and send key events to websocket.
app.py: Websocket server, receive websocket message from hardware and broadcast it.

Run hardware_app.py as root (or evdev allowed user)
Run app.py 


