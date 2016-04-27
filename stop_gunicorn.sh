#!/bin/bash
cd "`dirname $0`"
if [ -f logs/gunicorn.pid ]
then
  PID=`cat logs/gunicorn.pid`
  ps $PID >/dev/null && kill $PID >/dev/null
  sleep 1
  if ps $PID >/dev/null
  then
    kill $PID >/dev/null
    sleep 1
    if ps $PID >/dev/null
    then
      ps $PID >/dev/null && kill -9 $PID >/dev/null
    fi
  fi
fi
