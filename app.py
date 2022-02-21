import os
from flask import Flask
from flask import render_template, request
import psycopg2
import random
import datetime


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

def get_curr_timestamp():
    ts = datetime.datetime.now()
    return str(ts.year)+"-"+str(ts.month)+"-"+str(ts.day)+" "+str(ts.hour)+":"+str(ts.minute)+":"+str(ts.second)

@app.route('/', methods=["POST", "GET"])
def home():
    db.execute("select u.username, t.tweet, t.tweettime from tweets t, users u where u.userid = t.userid;")
    posts = db.fetchall()
    db.execute("select username from users;")
    users = db.fetchall()
    return render_template("index.html", posts=posts, users=users, loginuser=current_login["username"])

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db.execute("select username, userid from users where username = '"+username+"' and password = '"+password+"';")
        users = db.fetchall()
        if(len(users) == 1):
            current_login["username"] = users[0][0]
            current_login["userid"] = users[0][1]
    return render_template("login.html")

@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        newusername = request.form["username"]
        newpassword = request.form["password"]
        db.execute("insert into users(username, password) values('"+newusername+"','"+newpassword+"');")
        conn.commit()
    return render_template("signup.html")

@app.route('/add', methods=["POST", "GET"])
def add():
    if request.method == "POST" and current_login["username"]!= "undef":
        stweet = request.form["tweet"]
        db.execute("insert into tweets(userid, tweet, tweettime) values("
            +str(current_login["userid"])+", '"
            +stweet+"', '"
            +get_curr_timestamp()+"');")
        conn.commit()
    return render_template("add.html")