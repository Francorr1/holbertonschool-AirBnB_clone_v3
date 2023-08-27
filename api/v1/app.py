#!/usr/bin/python3
""" Creates flask app """
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    storage.close()


@app.errorhandler(404)
def fourofour(exception):
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', threaded=True)
