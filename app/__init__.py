import flask
import os.path
import pickle
import logging


app = flask.Flask(__name__)
entries = []
entries_pickle = "./entries.pickle"


if os.path.exists(entries_pickle):
    try:
        with open(entries_pickle, "rb") as entries_file:
            entries = pickle.load(entries_file)
    except Exception:
        logging.exception("Can't import last data")


@app.route("/", methods=["get"])
def index():
    return flask.render_template("base.jinja2", entries=entries)

@app.route("/", methods=["post"])
def push():
    global entries
    entries.append(dict(**flask.request.form))

    try:
        with open(entries_pickle, "wb") as entries_file:
            entries = pickle.dump(entries_file)
    except Exception:
        logging.exception("Can't write current data")

    return flask.redirect("/")