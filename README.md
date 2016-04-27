# Keyboard Websocket
Read evdev device and send to websocket. Works only on Linux with X11.

* **hardware_app.py**: Read device from evdev and send key events to websocket.
* **app.py**: Websocket server, receive websocket message from hardware and broadcast it.
* **detect_keyboard.py**: Detect which keyboard to use, and saves in keyboard.cfg

## Install

To run this project you need [Xinput](http://www.x.org/archive/X11R7.5/doc/man/man1/xinput.1.html), [Python](https://www.python.org/), [Python Evdev](http://python-evdev.readthedocs.org/en/latest/), [flask-SocketIO](https://flask-socketio.readthedocs.org/en/latest/) and my own fork of [Python socketIO-client](https://github.com/thor27/socketIO-client). You need this to be running in a Linux environment with X11.

To install this project, first you need to clone it:

```bash
git clone https://github.com/thor27/multimonitor-browser.git
```

Then, just install **requirements.txt** with pip:

```bash
pip install -r requirements.txt
```

**Python Evdev** needs special dependencies installed on your system to build and work. Refer to their [documentation](http://python-evdev.readthedocs.org/en/latest/) for more information

On Debian, you can install **xinput** with:

```bash
apt install xinput
```

## Usage

Run **detect_keyboard.py** as root (or evdev allowed user) once to configure.

```bash
sudo ./detect_keyboard.py
```

Remember, if you use **virtualenv**, to run **sudo** you will need to specify python to run the file, for example:

```bash
sudo /path/to/virtual_env/bin/python ./detect_keyboard.py
```


Run **app.py** to start the SocketIO server

```bash
./app.py
```

You can also run **app.py** as daemon with **gunicorn**. To do that, use the **start_gunicorn.sh** and **stop_gunicorn.sh** scripts to start and stop the SocketIO server respectively.

Run **hardware_app.py** as root (or evdev allowed user)

```bash
sudo ./hardware_app.py
```

**IMPORTANT**: While running **hardware_app.py** the controlled keyboard is disabled on X11. Make sure you don't disable the only keyboard you have. You can disable this behavior using **--keep-keyboard-enabled**

```bash
sudo ./hardware_app.py --keep-keyboard-enabled
```

Remember, if you use **virtualenv**, to run **sudo** you will need to specify python to run the file, for example:

```bash
sudo /path/to/virtual_env/bin/python ./hardware_app.py
```

You can test if everything is working at <http://localhost:5000/>

## Command line Argument

All scripts used above has special command line arguments to change it's behavior. Use **--help** to get more information about them.
```bash
./detect_keyboard.py --help
./app.py --help
./hardware_app.py --help
```

## Give /dev/input* keyboard permission to an user

To do that, you need to create a new rule on **/etc/udev/rules.d/**:

```bash
vim /etc/udev/rules.d/99-user-input-reader.rules
```
Put this content on the file, where **username** is the name of the user you want to give this permission:

```
KERNEL=="event*", SUBSYSTEM=="input", RUN+="/usr/bin/setfacl -m u:username:r $env{DEVNAME}"
```

After that you can run:

```bash
sudo setfacl -m u:username:r /dev/input/eventx
```
To make the changes now. Remember to replace **username** with the correct name.

**IMPORTANT** Before doing that, remember that given this power to any user, you will give the user and any software executed by them, the power to sniff any input device, **including reading passwords**. If it's possible, create a specific user with this permission that only runs this software.


## Contributors

* Thomaz de Oliveira dos Reis <thor27@gmail.com>

## License

* GPLv3
