#-*- coding: utf-8 -*-

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def test_connect():
    emit('ok')

@socketio.on('hardware_event')
def test_message(message):
    emit('key_event', message, broadcast=True)

if __name__ == '__main__':
    socketio.run(app)
