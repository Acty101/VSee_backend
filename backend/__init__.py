"""Create a backend server."""

from flask import Flask
from pathlib import Path
from flask_cors import CORS

# create flask instance
app = Flask(__name__)
CORS(app)
ROOT = Path(__file__).resolve().parent.parent

# configurations
app.config["UPLOAD_FOLDER"] = ROOT / Path("var/uploads")

# temp secret key to set session object
app.config["SECRET_KEY"] = (
    b'?#\xfc=\x00@\xa1"D\x01\x02g\xab\xc5\x11\xeb\xd4\xb2-5?\x93Y '
)
app.config["DATABASE_FILENAME"] = ROOT / "var" / "backend.sqlite3"

import backend.api
