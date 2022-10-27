import flask

from .model import session, Entry
from .utils import get_date


app = flask.Flask(__name__)
err = []


@app.add_template_global
def last_err():
    if not err:
        return None

    last = err[-1]
    err.clear()
    return last


@app.add_template_filter
def plot_entries(entries):
    import plotly
    import json
    import pandas as pd
    import plotly.express as px

    df = pd.DataFrame({
        "sugar": [entry["sugar"] for entry in entries],
        "date": [entry["date"] for entry in entries],
    })

    return json.dumps(px.scatter(df, x="date", y="sugar"), cls=plotly.utils.PlotlyJSONEncoder)


@app.route("/", methods=["get"])
def index():
    return flask.render_template("base.jinja2", entries=session.query(Entry).order_by(Entry.date.desc()).all())


@app.route("/", methods=["post"])
def push():
    try:
        session.add(Entry(date=get_date(flask.request.form),
                        sugar=flask.request.form.get("sugar"),
                        dosage=flask.request.form.get("dosage"),
                        food=flask.request.form.get("foodamount") or None,
                        brand=flask.request.form.get("foodbrand") or None,
                        water=flask.request.form.get("water") or None))
        session.commit()
    except Exception as e:
        err.append(str(e))

    return flask.redirect("/")