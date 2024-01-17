from flask import Flask
from flask_socketio import SocketIO


app = Flask(__name__)
app.config["SECRET_KEY"] = 'asdasdasffasdfdsgadsfas'
socketio = SocketIO(app)

from chat import views
