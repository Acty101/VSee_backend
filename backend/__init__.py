"""Create a backend server."""

from flask import Flask
from pathlib import Path

# create flask instance
app = Flask(__name__)
ROOT = Path(__file__).resolve().parent.parent

# configurations
app.config["UPLOAD_FOLDER"] = ROOT / Path("var/uploads")

import backend.api
