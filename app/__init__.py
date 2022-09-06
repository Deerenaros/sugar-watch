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
    food = Column(Integer)
    brand = Column(String)
    water = Column(Integer)
    
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

@app.add_template_filter
def plot_entries(entries):
    import matplotlib.dates as dt
    import matplotlib.figure as fg
    import io, base64

    X = [entry.date for entry in entries]
    Y = [entry.sugar for entry in entries]

    figure = fg.Figure()
    plot = figure.subplots()
    plot.plot_date(dt.date2num(X), Y, "ro")
    buff = io.BytesIO()
    figure.savefig(buff, format="png")
    return base64.b64encode(buff.getbuffer()).decode("ascii")


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
    session.add(Entry(date=get_date(flask.request.form),
                      sugar=flask.request.form.get("sugar"),
                      dosage=flask.request.form.get("dosage"),
                      food=flask.request.form.get("foodamount"),
                      brand=flask.request.form.get("foodbrand"),
                      water=flask.request.form.get("water")))
    session.commit()

    return flask.redirect("/")