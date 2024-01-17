from flask import Flask


app = Flask(__name__)

from chat import views
