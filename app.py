from imp import reload
import os
from flask import Flask, redirect, url_for
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
    posts = [[]]
    users = [[]]
    extra = [[]]
    if current_login["userid"] == "undef":
        db.execute("select u.username, t.tweet, t.tweettime, u.userid, t.tweetid from tweets t, users u where u.userid = t.userid order by tweettime desc fetch first 50 rows only;")
        posts = db.fetchall()
        db.execute("select username, userid from users fetch first 50 rows only;")
        users = db.fetchall()
    else:
        db.execute("select u.username, t.tweet, t.tweettime, u.userid, t.tweetid from tweets t, users u where u.userid = t.userid and u.userid = "+str(current_login["userid"])+" union select u.username, t.tweet, t.tweettime, u.userid, t.tweetid from tweets t, users u, followers f where u.userid = t.userid and f.fe = u.userid order by tweettime desc fetch first 50 rows only;")
        posts = db.fetchall()
        db.execute("select username, u.userid from users u, followers f where f.fe = u.userid fetch first 50 rows only;")
        users = db.fetchall()
        db.execute("select username, u.userid from users u, (select userid from users where not userid = "+str(current_login["userid"])+"  except select fe as userid from followers) as diff where diff.userid = u.userid fetch first 50 rows only;")
        extra = db.fetchall()
    if request.method == "POST":
        if 'addchirpbutton' in request.form:
            if(current_login["userid"] == 'undef'):
                return redirect(url_for("login"))
            else:
                db.execute("insert into tweets(userid, tweet, tweettime, response_tweets, in_response_to_tweet) values("
                    +str(current_login["userid"])+", '"
                    +request.form.get('addchirp')+"', '"
                    +get_curr_timestamp()+"', array[]::integer[], array[]::integer[]);")
                conn.commit()
                db.execute("select u.username, t.tweet, t.tweettime, u.userid, t.tweetid from tweets t, users u where u.userid = t.userid and u.userid = "+str(current_login["userid"])+" union select u.username, t.tweet, t.tweettime, u.userid, t.tweetid from tweets t, users u, followers f where u.userid = t.userid and f.fe = u.userid order by tweettime desc fetch first 50 rows only;")
                posts = db.fetchall()
                db.execute("select username, u.userid from users u, followers f where f.fe = u.userid fetch first 50 rows only;")
                users = db.fetchall()
                db.execute("select username, u.userid from users u, (select userid from users where not userid = "+str(current_login["userid"])+"  except select fe as userid from followers) as diff where diff.userid = u.userid fetch first 50 rows only;")
                extra = db.fetchall()
                return render_template("index.html", posts=posts, users=users, loginuser=[current_login["userid"],current_login["username"]], extra=extra)
        if 'searchbutton' in request.form and len(request.form.get('search'))>0:
            return redirect(url_for('search', searchquery=request.form.get('search')))
    return render_template("index.html", posts=posts, users=users, loginuser=[current_login["userid"],current_login["username"]], extra=extra)

@app.route("/search/<string:searchquery>", methods=["POST", "GET"])
def search(searchquery):
    db.execute("select u.userid, t.tweetid, u.username, t.tweet, t.tweettime from tweets t, users u where u.userid = t.userid and tweet like '%"+searchquery+"%' order by tweettime desc fetch first 50 rows only;")
    tweetresults = db.fetchall()
    db.execute("select userid, username from users where username like '%"+searchquery+"%' fetch first 50 rows only;")
    userresults = db.fetchall()
    if request.method == "POST":
        if 'searchbutton' in request.form and len(request.form.get('search'))>0:
            return redirect(url_for('search', searchquery=request.form.get('search')))
    return render_template("search.html", results=tweetresults, userresults=userresults, searchquery=searchquery, loginuser=[current_login["userid"],current_login["username"]])

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
            db.execute("drop view if exists followers;")
            conn.commit()
            db.execute("create view followers as select * from network where fr = "+ str(current_login["userid"])+" with cascaded check option;")
            conn.commit()
    return render_template("login.html")

@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        newusername = request.form["username"]
        newpassword = request.form["password"]
        db.execute("insert into users(username, password) values('"+newusername+"','"+newpassword+"');")
        conn.commit()
    return render_template("signup.html")

@app.route('/user/<int:userid>', methods=["POST", "GET"])
def userpage(userid):
    db.execute("select username from users where userid = "+str(userid)+";")
    username=db.fetchall()[0][0]
    db.execute("select u.username, t.tweet, t.tweettime, t.tweetid from tweets t, users u where u.userid = t.userid and u.userid = "+str(userid)+" order by tweettime desc;")
    tweets=db.fetchall()
    isfollowing = False
    if(current_login["userid"] != 'undef'):
        db.execute("select fe from followers where fe = "+str(userid)+";")
        nid = db.fetchall()
        print(nid)
        if(len(nid)>0):
            isfollowing = True
    if request.method == "POST":
        if 'searchbutton' in request.form and len(request.form.get('search'))>0:
            return redirect(url_for('search', searchquery=request.form.get('search')))
        if 'followbutton' in request.form:
            db.execute("insert into followers values("+str(current_login["userid"])+","+str(userid)+");")
            conn.commit()
            return redirect(url_for('userpage', userid=userid))
    return render_template("user.html", loginuser=[current_login['userid'],current_login["username"]], user=[userid, username], tweets=tweets, isfollowing=isfollowing)

@app.route('/tweet/<int:tweetid>', methods=["POST", "GET"])
def tweetpage(tweetid):
    db.execute("select u.userid, u.username, t.tweetid, t.tweet, t.tweettime, t.in_response_to_tweet, t.response_tweets from tweets t, users u where u.userid = t.userid and t.tweetid = "+str(tweetid)+";")
    tweet = db.fetchall()[0]
    posts=[]
    if((tweet[6]) != None and len(tweet[6])>0):
        db.execute("select u.username, t.tweet, t.tweettime, u.userid, t.tweetid from tweets t, users u where u.userid = t.userid and t.tweetid = any(array"+str(tweet[6])+") order by tweettime desc fetch first 50 rows only;")
        posts=db.fetchall()
    if request.method == "POST":
        if 'searchbutton' in request.form and len(request.form.get('search'))>0:
            return redirect(url_for('search', searchquery=request.form.get('search')))
        elif 'responsebutton' in request.form and len(request.form.get('addresponse'))>0:
            if(current_login["userid"] == 'undef'):
                return redirect(url_for("login"))
            else:
                print("adding "+request.form.get('addresponse'))
                db.execute("insert into tweets(userid, tweet, tweettime, response_tweets, in_response_to_tweet) values("
                    +str(current_login["userid"])+", '"
                    +request.form.get('addresponse')+"', '"
                    +get_curr_timestamp()+"', array[]::integer[], array["+str(tweet[2])+"]) returning tweetid;")
                newtweetid = db.fetchall()[0][0]
                print(newtweetid)
                db.execute("update tweets set response_tweets = response_tweets || "+str(newtweetid)+" where tweetid = "+str(tweet[2])+"")
                conn.commit()
                db.execute("select u.userid, u.username, t.tweetid, t.tweet, t.tweettime, t.in_response_to_tweet, t.response_tweets from tweets t, users u where u.userid = t.userid and t.tweetid = "+str(tweetid)+";")
                tweet = db.fetchall()[0]
                db.execute("select u.username, t.tweet, t.tweettime, u.userid, t.tweetid from tweets t, users u where u.userid = t.userid and t.tweetid = any(array"+str(tweet[6])+") order by tweettime desc fetch first 50 rows only;")
                posts=db.fetchall()
                return render_template("tweet.html", tweet=tweet, loginuser=[current_login["userid"],current_login["username"]], posts=posts)
    return render_template("tweet.html", tweet=tweet, loginuser=[current_login["userid"],current_login["username"]], posts=posts)