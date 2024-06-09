import flask
import backend
from backend.api.utils import *
import backend.database
import backend.model
from backend.model.main import run_models

@backend.app.route("/", methods=["GET"])
def endpoints():
    """Return a list of all available endpoints."""
    return flask.jsonify(
        {
            "endpoints": [
                "/api/v1/account/create/",
                "/api/v1/questions/",
                "/api/v1/answers/",
                "/api/v1/startups/",
                "/api/v1/request_startup_info/",
                "/api/v1/request_summary/",
            ]
        }
    )


@backend.app.route("/api/v1/account/create/", methods=["POST"])
def create_acc():
    """Route to create an account.

    Expects a form data from registration page.
    """
    username = flask.request.form.get("username", type=str)
    name = flask.request.form.get("name", type=str)
    password = flask.request.form.get("password", type=str)
    type = flask.request.form.get("type", type=bool)
    industry = flask.request.form.get("industry", type=str)
    summary = flask.request.form.get("summary", type=str)
    file = flask.request.files.get("file")  # optional

    if None in (username, password, name, type, summary):
        # missing required fields
        return (
            flask.jsonify(make_err_response(404, "Missing required field")),
            404,
        )

    # save file to disk and get filename
    if file is not None:
        filename = save_file_to_disk(file)
    else:
        filename = ""

    # create an entry in the db
    connection = backend.database.get_db()
    connection.execute(
        "INSERT INTO users "
        "(username, name, password, filename, is_vc, points, industry, summary) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (username, name, password, filename, type, 0, industry, summary),
    )
    # return an empty string and 201 - created
    return "", 201


# ###### TEMP FUNCTIONS since login page not implemented yet
# @backend.app.route("/set_session/", methods=["POST", "GET"])
# def set_session():
#     username = flask.request.form.get("username", type=str)
#     flask.session["username"] = username
#     return "", 200


# @backend.app.route("/login/", methods=["POST", "GET"])
# def login_page():
#     return flask.render_template("index.html")


# ######
@backend.app.route("/api/v1/user_info/<username>")
def get_user_info(username: str):
    """Return info of username."""
    connection = backend.database.get_db()
    if username is None:
        return (
            flask.jsonify(make_err_response(404, "username not found.")),
            404,
        )
    cur = connection.execute("SELECT users.name, users.filename, users.is_vc, users.points, users.industry, users.summary"
                             "FROM users WHERE username = ?", (username,))
    user_info = cur.fetchall()
    flask.jsonify({"user": user_info}), 200


@backend.app.route("/api/v1/questions/", methods=["GET"])
def get_question():
    """Returns the next <size> questions with corresponding id.

    <size> is a query param with default value 5
    next is defined as the offset by points of the user, ie if 5 points, we want the 6th question
    """
    username = flask.request.args.get("username")
    if username is None:
        return (
            flask.jsonify(make_err_response(404, "username not found.")),
            404,
        )
    connection = backend.database.get_db()
    size = flask.request.args.get("size", type=int, default=5)
    cur = connection.execute(
        "SELECT points, is_vc FROM users WHERE username = ?", (username,)
    )
    user = cur.fetchone()
    next = user["points"]
    is_vc = user["is_vc"]
    cur = connection.execute(
        "SELECT question_id, question FROM questions WHERE is_vc = ? LIMIT ? OFFSET ?",
        (is_vc, size, next),
    )
    questions = cur.fetchall()
    return flask.jsonify({"questions": questions}), 200


@backend.app.route("/api/v1/answers/", methods=["POST"])
def ans_question():
    """Updates db with answers to each question id.

    Expects a {"data": [{}, {}, ...]} JSON object where each {} contains 'question_id' & 'answer'
    """
    username = flask.request.args.get("username")
    if username is None:
        return (
            flask.jsonify(make_err_response(404, "username not found.")),
            404,
        )
    data = flask.request.json
    data = data.get("data", None)
    if data is None:
        return (
            flask.jsonify(make_err_response(404, "Missing data object")),
            404,
        )

    connection = backend.database.get_db()
    for entry in data:
        id = entry.get("question_id")
        ans = entry.get("answer")
        if None in (id, ans):
            return (
                flask.jsonify(make_err_response(404, "Invalid key in data")),
                404,
            )
        connection.execute(
            "INSERT INTO answers (question_id, answer, username)"
            "VALUES (?, ?, ?)",
            (id, ans, username),
        )
    # update points
    cur = connection.execute(
        "SELECT points FROM users WHERE username = ?", (username,)
    )
    cur = cur.fetchone()
    points = cur["points"]
    new_points = points + len(data)
    connection.execute(
        "UPDATE users SET points = ? WHERE username = ?",
        (new_points, username),
    )
    feedback = f"Created {len(data)} answers for {username}"
    return flask.jsonify({"feedback": feedback,}), 201

@backend.app.route("/api/v1/uploads/<filename>/", methods=['GET'])
def uploads_get(filename: str):
    """Serve image files."""
    path = backend.app.config['UPLOAD_FOLDER'] / Path(filename)
    if not path.is_file():
        flask.abort(404)
    return flask.send_from_directory(backend.app.config['UPLOAD_FOLDER'],
                                     filename)

@backend.app.route("/api/v1/logs/<filename>/", methods=['GET'])
def logs_get(filename: str):
    """Serve log (text) files."""
    path = backend.app.config['LOG_FOLDER'] / Path(filename)
    if not path.is_file():
        flask.abort(404)
    return flask.send_from_directory(backend.app.config['LOG_FOLDER'],
                                     filename)

@backend.app.route("/api/v1/startups/", methods=["GET"])
def get_startups():
    """Returns information about <size> startups in the <page>th page, and their username, and next url.

    <next> is the url to query to get the next page of data
    For example, size = 5 and page = 1 (0th index) returns the 6-10th row of startups.
    <size> is a query param with default value 5
    <page> is a query param with default value 0
    """
    username = flask.request.args.get("username")
    if username is None:
        return (
            flask.jsonify(make_err_response(404, "username not found.")),
            404,
        )
    connection = backend.database.get_db()
    page = flask.request.args.get("page", type=int, default=0)
    size = flask.request.args.get("size", type=int, default=5)
    offset = page * size
    cur = connection.execute("SELECT COUNT (*) FROM users WHERE is_vc = 0")
    startups_count = cur.fetchone()["COUNT (*)"]

    cur = connection.execute(
        "SELECT username, name, filename, is_vc, points, industry, summary FROM users WHERE is_vc = 0 ORDER BY points DESC LIMIT ? OFFSET ?",
        (size, offset),
    )
    startups = cur.fetchall()
    if (page + 1) * size  < startups_count:
        return (
            flask.jsonify(
                {
                    "startups": startups,
                    "next": f"{flask.url_for("get_startups")}?username={username}&size={size}&page={page+1}",
                }
            ),
            200,
        )
    return(
        flask.jsonify(
            {
                "startups": startups,
                "next": "",
            }
        ),
        200,
    )


@backend.app.route("/api/v1/request_startup_info/", methods=["POST"])
def request_startup_info():
    """Updates the bot_summary table with information obtained from AI models.

    <company> corresponds to company username
    Returns company name and bot_summary id
    """
    vc = flask.request.args.get("username")
    if vc is None:
        return (
            flask.jsonify(make_err_response(404, "username not found.")),
            404,
        )
    startup = flask.request.args.get("company", type=str)
    connection = backend.database.get_db()

    # get VC qa
    cur = connection.execute(
        "SELECT question, answer FROM answers "
        "INNER JOIN questions ON answers.question_id = questions.question_id "
        "WHERE username = ?",(vc,)
    )
    vc_qa = cur.fetchall()
    vc_list = []
    for qa in vc_qa:
        vc_list.append(qa["question"])
        vc_list.append(qa["answer"])

    # get startup qa
    cur = connection.execute(
        "SELECT question, answer FROM answers "
        "INNER JOIN questions ON answers.question_id = questions.question_id "
        "WHERE username = ?",(startup,)
    )
    startup_qa = cur.fetchall()
    startup_str = ""
    for qa in startup_qa:
        startup_str += f"{qa["question"]};{qa["answer"]};"
    

    text, filename = run_models(vc_name=vc, startup_name=startup, startup_qa=startup_str, vc_qa=vc_list, logfolder=backend.app.config["LOG_FOLDER"])
    # insert values into bot summary table
    cur.execute(
        "INSERT INTO bot_summary(startup_username, vc_username, summary, filename)"
        "VALUES (?,?,?,?)",
        (startup, vc, text, str(filename)),
    )
    summary_id = cur.lastrowid

    return flask.jsonify({"username": startup, "summary_id": summary_id, "url": f":/api/v1/request_summary/{summary_id}"}), 200


@backend.app.route("/api/v1/request_summary/<int:id>/", methods=["GET"])
def request_summary(id):
    """Returns the summary of <id>."""
    username = flask.request.args.get("username")
    if username is None:
        return (
            flask.jsonify(make_err_response(404, "username not found.")),
            404,
        )
    connection = backend.database.get_db()
    cur = connection.execute("SELECT * FROM bot_summary WHERE summary_id = ?", (id,))
    cur = cur.fetchone()
    if cur is None:
        return flask.jsonify(make_err_response(404, "No summary found")), 404
    with open(cur["filename"], 'r') as file:
        log = file.read()
    return flask.jsonify({"summary": cur["summary"], "log": log}), 200
