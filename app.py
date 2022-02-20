from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import render_template, request
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
import random

import sqlalchemy
conn_text = 'postgresql+psycopg2://postgres:postgres@localhost/postgres'
engine = create_engine (conn_text)

db = scoped_session(sessionmaker(bind=engine))
app = Flask(__name__)
app.secret_key = 'supersecretkey'


loginusername = "undef"
loginuserid = "undef"

@app.route('/', methods=["POST", "GET"])
def home():
    posts = db.execute("select u.username, t.tweet from tweets t, users u where u.userid = t.userid").fetchall()
    users = db.execute("select username from users")
    return render_template("index.html", posts=posts, users=users, loginuser=loginusername)

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        global loginuserid
        global loginuserid
        newusername = request.form["username"]
        adduser = db.execute("insert into users(username) values(:username)",
        {"username":newusername})
        db.commit()
        loginusername = newusername
        loginuserid = db.execute("select userid from users where username = :username",{"username":loginusername}).fetchall()[0].userid
    return render_template("login.html")

@app.route('/add', methods=["POST", "GET"])
def add():
    if request.method == "POST" and loginuserid != "undef":
        stweet = request.form["tweet"]
        db.execute("insert into tweets(userid, tweet) values(:userid, :tweet)",
        {"userid":loginuserid,
        "tweet":stweet})
        db.commit()
    return render_template("add.html")