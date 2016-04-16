# keyboard-websocket
Read evdev device and send to websocket

* **hardware_app.py**: Read device from evdev and send key events to websocket.
* **app.py**: Websocket server, receive websocket message from hardware and broadcast it.
* **detect_keyboard.py**: Detect which keyboard to use, and saves in keyboard.cfg

1. Run **detect_keyboard.py** as root (or evdev allowed user) once to configure.
2. Run **app.py**
3. Run **hardware_app.py** as root (or evdev allowed user)
4. open <http://localhost:5000/>
