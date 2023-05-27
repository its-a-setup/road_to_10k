from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

app = Flask(__name__)
app.app_context().push()
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"mysql+mysqlconnector://{USERNAME}:{PASSWORD}@localhost:3306/road_10k_v2"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True

db = SQLAlchemy(app)


class SESSIONS(db.Model):
    session_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    created_at = db.Column(db.DATETIME, default=datetime.utcnow())
    tag = db.Column(db.String(100))
    time_passed = db.Column(db.Time, default="00:00:00")


db.create_all()


@app.get("/")
def home():
    session_history = db.session.query(SESSIONS).all()
    return render_template("base.html", session_history=session_history)


@app.post("/add")
def add():
    tag = request.form.get("tag")
    new_session = SESSIONS(tag=tag, complete=False)
    db.session.add(new_session)
    db.session.commit()
    return redirect(url_for("home"))


@app.get("/delete/<int:session_id>")
def delete(session_id):
    session = db.session.query(SESSIONS).filter(SESSIONS.session_id == session_id).first()
    db.session.delete(session)
    db.session.commit()
    return redirect(url_for("home"))
