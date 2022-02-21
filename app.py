import os
from flask import Flask
from flask import render_template, request
import psycopg2
import random


app = Flask(__name__)

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="postgres"
)

db = conn.cursor()

current_login = {
    "username":"undef",
    "userid":"undef"
}

@app.route('/', methods=["POST", "GET"])
def home():
    db.execute("select u.username, t.tweet from tweets t, users u where u.userid = t.userid;")
    posts = db.fetchall()
    db.execute("select username from users;")
    users = db.fetchall()
    return render_template("index.html", posts=posts, users=users, loginuser=current_login["username"])

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        newusername = request.form["username"]
        db.execute("insert into users(username) values('"+newusername+"');")
        current_login["username"] = newusername
        db.execute("select userid from users where username = '"+newusername+"' fetch first 1 row only;")
        current_login["userid"] = db.fetchall()[0][0];
    return render_template("login.html")

@app.route('/add', methods=["POST", "GET"])
def add():
    if request.method == "POST" and current_login["username"]!= "undef":
        stweet = request.form["tweet"]
        db.execute("insert into tweets(userid, tweet) values("+str(current_login["userid"])+", '"+stweet+"');")
    return render_template("add.html")