import flask
import backend
from backend.database import get_db


@backend.app.route("/", methods=["GET"])
def endpoints():
    """Return a list of all available endpoints."""
    return flask.jsonify(
        {
            "endpoints": [
                "/api/v1/account/create",
                "/api/v1/questions/",
                "/api/v1/answers/",
                "/api/v1/startups/",
                "/api/v1/request_startup_info/",
                "/api/v1/request_summary/",
            ]
        }
    )


@backend.app.route("/api/v1/account/create", methods=["POST"])
def create_acc():
    """Route to create an account.

    Expects a form data from registration page.
    """
    username = flask.request.form.get("username", type=str)
    password = flask.request.form.get("password", type=str)
    name = flask.request.form.get("name", type=str)
    type = flask.request.form.get("type", type=bool)
    summary = flask.request.form.get("summary", type=str)
    file = flask.request.files.get("file")
    points = 0


@backend.app.route("/api/v1/questions/", methods=["GET"])
def get_question():
    """Returns the next <size> questions with corresponding id.

    <size> is a query param with default value 5
    next is defined as the offset by points of the user, ie if 5 points, we want the 6th question
    """
    size = flask.request.args.get("size", type=int, default=5)


@backend.app.route("/api/v1/answers/", methods=["POST"])
def ans_question():
    """Updates db with answers to each question id.

    Expects a [{}, {}, ...] object where each {} contains 'question_id' & 'answer'
    """


@backend.app.route("/api/v1/startups/", methods=["GET"])
def get_startups():
    """Returns information about <size> startups in the <page>th page, and their username.

    For example, size = 5 and page = 1 (0th index) returns the 6-10th row of startups.
    <size> is a query param with default value 5
    <page> is a query param with default value 0
    """


@backend.app.route("/api/v1/request_startup_info/", methods=["POST"])
def request_startup_info():
    """Updates the bot_summary table with information obtained from AI models.

    <user> is a required form data field corresponding to company username
    Returns company name and bot_summary id
    """


@backend.app.route("/api/v1/request_summary/", methods=["GET"])
def request_summary():
    """Returns the summary of <id>.

    <id> is a required form data field representing bot_summary table's primary key
    """
