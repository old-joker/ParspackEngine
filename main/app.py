from routes import create_app
from utils.constants import APP_DEBUG, APP_HOST, APP_PORT
from utils.helpers import _loadconfig
import os
from utils.constants import APP_BASE_DIR
from os.path import exists
from flask import request
from dotenv import load_dotenv


load_dotenv()

# Create the Flask app using the factory method from routes/__init__.py
app, celery = create_app()


@app.before_request
def main():
    if not exists(APP_BASE_DIR + "/results"):
        os.makedirs(APP_BASE_DIR + "/results")
    _loadconfig()



if __name__ == "__main__":
    app.run(debug=APP_DEBUG, host=APP_HOST, port=APP_PORT)
