import flask
import sys
import os.path
import pickle
import logging
import sqlalchemy


from sqlalchemy import Column, Integer, String, Float, DateTime, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
class Entry(Base):
    __tablename__ = 'entry'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    sugar = Column(Float)
    dosage = Column(Float)
    food = Column(Integer, nullable=True)
    brand = Column(String, nullable=True)
    water = Column(Integer, nullable=True)
    
    def __getitem__(self, key):
        if key in ("year", "month", "day", "hour", "minute"):
            return getattr(self.date, key)
        return getattr(self, key)

    def __repr__(self):
       return " ".join(map(str, (self.date,
                                 self.sugar,
                                 self.dosage,
                                 self.food,
                                 self.brand,
                                 self.water)))

engine = create_engine("postgresql://local:sql@postgres")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

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
    import sys

    df = pd.DataFrame({
        "sugar": [entry["sugar"] for entry in entries],
        "date": [entry["date"] for entry in entries],
    })

    return json.dumps(px.scatter(df, x="date", y="sugar"), cls=plotly.utils.PlotlyJSONEncoder)

@app.route("/", methods=["get"])
def index():
    return flask.render_template("base.jinja2", entries=session.query(Entry).order_by(Entry.date.desc()).all())

def get_date(form):
    from datetime import datetime
    return datetime(year=int(form.get("year")),
                    month=int(form.get("month")),
                    day=int(form.get("day")),
                    hour=int(form.get("hours")),
                    minute=int(form.get("minutes")))

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