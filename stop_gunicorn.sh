#!/bin/bash
cd "`dirname $0`"
if [ -f logs/gunicorn.pid ]
then
  PID=`cat logs/gunicorn.pid`
  if ps $PID >/dev/null
  then
    kill $PID >/dev/null
    sleep 0.5
    if ps $PID >/dev/null
    then
      kill $PID >/dev/null
      sleep 1
      ps $PID >/dev/null && kill -9 $PID >/dev/null
    fi
  fi
fi
