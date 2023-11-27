from . import app
from flask import jsonify


@app.route("/")
def hello_world():
    return jsonify(hello="world")