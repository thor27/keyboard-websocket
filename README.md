# keyboard-websocket
Read evdev device and send to websocket

hardware_app.py: Read device from evdev and send key events to websocket.
app.py: Websocket server, receive websocket message from hardware and broadcast it.
detect_keyboard.py: Detect which keyboard to use, and saves in keyboard.cfg

Run detect_keyboard.py as root (or evdev allowed user) once to configure.
Run app.py
Run hardware_app.py as root (or evdev allowed user)

open http://localhost:5000
