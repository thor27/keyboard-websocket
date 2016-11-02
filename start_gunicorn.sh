#!/bin/bash
cd "`dirname $0`"
 KEYBOARDCFG=/etc/keyboard.conf gunicorn -D --pid logs/gunicorn.pid --access-logfile logs/access.log --error-logfile logs/error.log --bind localhost:5000 --worker-class eventlet -w 1 app:app
