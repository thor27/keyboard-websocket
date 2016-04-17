#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
    Websocket server, receive websocket message from hardware and broadcast it.
    Copyright (C) 2016 Thomaz de Oliveira dos Reis <thor27@gmail.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from __future__ import print_function
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import argparse
import sys

app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('hardware_event')
def test_message(message):
    emit('key_event', message, broadcast=True)


def parse_args(args):
    parser = argparse.ArgumentParser(description='Keyboard Websocket webserver and Testground')
    parser.add_argument('-H', '--hostname', dest='hostname', type=str, default='localhost',
                        help='Specify socketIO hostname to connect. (Default: localhost)')
    parser.add_argument('-p', '--port', dest='port', type=int, default=5000,
                        help='Specify socketIO port to connect. (Default: 5000)')
    parser.add_argument('-s', '--silent', dest='silent', action='store_true', help='Don\'t print to stdout')

    return parser.parse_args(args)


def main():
    args = parse_args(sys.argv[1:])
    debug = not args.silent

    if debug:
        print('Listening on http://{0}:{1}/ '.format(args.hostname, args.port))

    socketio.run(app, host=args.hostname, port=args.port, debug=debug)

if __name__ == '__main__':
    main()
