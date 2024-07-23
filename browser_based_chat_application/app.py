from flask import Flask, render_template, request
from flask_socketio import SocketIO, send

app=Flask(__name__)
app.config['SECRET_KEY'] = 'hey heyy heyyyyy'
socketio=SocketIO(app)

def get_client_ip(request):
    if request.headers.getlist("X-Forwarded-For"):
        return request.headers.getlist("X-Forwarded-For")[0]
    return request.remote_addr

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(msg):
    client_ip=get_client_ip(request)
    if client_ip=="127.0.0.1":
        client_ip="localhost"
       
    print(f'Message from {client_ip}: {msg}')
    send(f'{client_ip}: {msg}', broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
