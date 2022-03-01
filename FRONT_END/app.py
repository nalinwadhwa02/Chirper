from imp import reload
from subprocess import call
from flask import Flask, redirect, url_for
from flask import render_template, request
import psycopg2
import random
import datetime


app = Flask(__name__)


conn = psycopg2.connect(
    # host="10.17.50.36",
    # database="group_35",
    # user="group_35",
    # password="VxGj6gCyWTKyM"
    host = "localhost",
    database = "postgres",
    user = "postgres",
    password = "postgres"
)

db = conn.cursor()

current_login = {
    "username":"undef",
    "userid":"undef"
}

db.execute("select setval('users_userid_seq',(select max(userid) from users));")
db.execute("select setval('tweets_tweetid_seq',(select max(tweetid) from tweets));")
db.execute("drop table if exists like_nums")
db.execute("create table like_nums as select t.tweetid, count(l.tweetid) as like_num from likes l right join tweets t on t.tweetid = l.tweetid group by t.tweetid;")
conn.commit()

def get_curr_timestamp():
    ts = datetime.datetime.now()
    return str(ts.year)+"-"+str(ts.month)+"-"+str(ts.day)+" "+str(ts.hour)+":"+str(ts.minute)+":"+str(ts.second)


def buttonhandler(form, userid = None, tweetid=None, tweet=None, calledfrom=None):
    if 'addchirpbutton' in form:
        if(current_login["userid"] == 'undef'):
            return redirect(url_for("login"))
        else:
            db.execute("insert into tweets(userid, tweet, tweettime, response_tweets, in_response_to_tweet) values("
                +str(current_login["userid"])+", '"
                +form.get('addchirp')+"', '"
                +get_curr_timestamp()+"', array[]::integer[], array[]::integer[]) returning tweetid;")
            ntweetid = db.fetchall()[0][0]
            db.execute("insert into like_nums values("+str(ntweetid)+", 0);")
            conn.commit()
            return redirect(url_for('home'))

    elif 'searchbutton' in form and len(form['search'])>0:
        print("searching")
        return redirect(url_for('search', searchquery=form.get('search')))

    elif 'followbutton' in form:
        if current_login["userid"] != 'undef':
            db.execute("insert into followers values("+str(current_login["userid"])+","+str(userid)+");")
            conn.commit()
            return redirect(url_for('userpage', userid=userid))
        else:
            return redirect(url_for('login', wrongcreds=0))
    
    elif 'followingbutton' in form:
        if current_login["userid"] != 'undef':
            db.execute("delete from followers where fr="+str(current_login["userid"])+" and fe="+str(userid)+";")
            conn.commit()
            return redirect(url_for('userpage', userid=userid))
        else:
            return redirect(url_for('login', wrongcreds=0))


    elif 'responsebutton' in form and len(form.get('addresponse'))>0:
        if(current_login["userid"] == 'undef'):
            return redirect(url_for("login", wrongcreds=False))
        else:
            db.execute("insert into tweets(userid, tweet, tweettime, response_tweets, in_response_to_tweet) values("
                +str(current_login["userid"])+", '"
                +form.get('addresponse')+"', '"
                +get_curr_timestamp()+"', array[]::integer[], array["+str(tweet[2])+"]) returning tweetid;")
            newtweetid = db.fetchall()
            db.execute("insert into like_nums values("+str(newtweetid[0][0])+", 0);")
            conn.commit()
            db.execute("update tweets set response_tweets = response_tweets || "+str(newtweetid[0][0])+" where tweetid = "+str(tweet[2])+";")
            conn.commit()
            return redirect(url_for('tweetpage', tweetid=tweetid))
    
    elif 'login' in form:
        return redirect(url_for('login', wrongcreds=0))

    elif 'logout' in form:
        logout()
        return redirect(url_for('home'))
        
    elif 'loginbutton' in form:
        username = form['username']
        password = form['password']
        db.execute("select userid from users where username = '"+str(username)+"' and password = '"+str(password)+"';")
        res = db.fetchall()
        print(res, username, password)
        if len(res) == 1 :
            current_login['userid'] = res[0][0]
            current_login['username'] = username
            db.execute('drop view if exists followers;')
            conn.commit()
            db.execute('drop view if exists userlikes;')
            conn.commit()
            db.execute("create view followers as select fr, fe from network where fr = "+str(current_login["userid"])+";")
            conn.commit()
            db.execute("create view userlikes as select tweetid, userid from likes where userid = '"+str(current_login['userid'])+"';")
            conn.commit()
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login', wrongcreds=1))


    elif 'signupbutton' in form:
        username = form['username']
        password = form['password']
        db.execute("select userid from users where username = '"+str(username)+"';")
        res = db.fetchall()
        print(res, username, password)
        if len(res) == 0 :
            db.execute("insert into users(username, password) values('"+str(username)+"', '"+str(password)+"') returning userid;")
            res = db.fetchall()
            conn.commit()
            current_login['userid'] = res[0][0]
            current_login['username'] = username
            db.execute('drop view if exists followers;')
            conn.commit()
            db.execute('drop view if exists userlikes;')
            conn.commit()
            db.execute("create view followers as select fr, fe from network where fr = "+str(current_login["userid"])+";")
            conn.commit()
            db.execute("create view userlikes as select tweetid, userid from likes where userid = '"+str(current_login['userid'])+"';")
            conn.commit()
            return redirect(url_for('home'))
    
    elif 'profilebutton' in form:
        return redirect(url_for('userpage', userid=current_login["userid"]))
    
    elif 'likebutton' in form:
        if current_login["userid"] == 'undef':
            return redirect(url_for('login', wrongcreds=0))
        else:
            db.execute("insert into userlikes values("+str(form['likebutton'])+","+str(current_login["userid"])+");")
            conn.commit()
            db.execute("update like_nums set like_num = like_num + 1 where tweetid = "+str(form['likebutton'])+";")
            conn.commit()
            if calledfrom == 'home':
                return redirect(url_for('home'))
            elif calledfrom == 'userpage':
                return redirect(url_for('userpage', userid=userid))
            elif calledfrom == 'tweetpage':
                return redirect(url_for('tweetpage', tweetid=tweetid))
    
    elif 'likedbutton' in form:
        db.execute("delete from userlikes where tweetid = "+str(form['likedbutton'])+" and userid = "+str(current_login["userid"])+";")
        conn.commit()
        db.execute("update like_nums set like_num = like_num - 1 where tweetid = "+str(form['likedbutton'])+";")
        conn.commit()
        if calledfrom == 'home':
            return redirect(url_for('home'))
        elif calledfrom == 'userpage':
            return redirect(url_for('userpage', userid=userid))
        elif calledfrom == 'tweetpage':
            return redirect(url_for('tweetpage', tweetid=tweetid))
            



@app.route('/', methods=["POST", "GET"])
def home():
    posts = [[]]
    users = [[]]
    extra = [[]]
    recm = [[]]
    if current_login["userid"] == "undef":
        db.execute("select u.username, t.tweet, t.tweettime, u.userid, t.tweetid, l.like_num from tweets t, users u, like_nums l where u.userid = t.userid and t.tweetid = l.tweetid order by tweettime desc fetch first 200 rows only;")
        posts = db.fetchall()
        db.execute("select username, userid from users order by random() fetch first 200 rows only;")
        users = db.fetchall()
    else:
        db.execute("select u.username, t.tweet, t.tweettime, u.userid, t.tweetid, l.like_num, case when t.tweetid = any(select tweetid from userlikes) then 'TRUE' else 'FALSE' end as userliked from tweets t, users u, like_nums l where u.userid = t.userid and t.tweetid = l.tweetid and u.userid = "+str(current_login["userid"])+" union select u.username, t.tweet, t.tweettime, u.userid, t.tweetid, l.like_num, case when t.tweetid = any(select tweetid from userlikes) then 'TRUE' else 'FALSE' end as userliked from tweets t, users u, followers f, like_nums l where u.userid = t.userid and f.fe = u.userid and t.tweetid = l.tweetid order by tweettime desc fetch first 200 rows only;")
        posts = db.fetchall()
        db.execute("select username, u.userid from users u, followers f where f.fe = u.userid fetch first 200 rows only;")
        users = db.fetchall()
        db.execute("select u.userid, username from users u, (select userid from users where not userid = "+str(current_login["userid"])+"  except select fe as userid from followers) as diff where diff.userid = u.userid order by random() fetch first 200 rows only;")
        extra = db.fetchall()
        db.execute("with recm as ((select fe from network where fr = any (select fe from followers) union select fr from network where fe = any (select fe from followers)) except select fe from followers) select userid, username from recm, users where fe = userid and not userid = "+str(current_login["userid"])+";")
        recm = db.fetchall()
        if len(recm) == 0:
            recm = extra
    if request.method == "POST":
        rval = buttonhandler(request.form, calledfrom='home')
        if rval!=None:
            return rval
    return render_template("index.html", posts=posts, users=users, loginuser=[current_login["userid"],current_login["username"]], extra=extra, recm=recm)


@app.route("/search/<string:searchquery>", methods=["POST", "GET"])
def search(searchquery):
    db.execute("select u.userid, t.tweetid, u.username, t.tweet, t.tweettime from tweets t, users u where u.userid = t.userid and lower(tweet) like lower('%"+searchquery+"%') order by tweettime desc fetch first 200 rows only;")
    tweetresults = db.fetchall()
    db.execute("select userid, username from users where lower(username) like lower('%"+searchquery+"%') fetch first 200 rows only;")
    userresults = db.fetchall()
    if request.method == "POST":
        rval = buttonhandler(request.form)
        if rval!=None:
            return rval
    return render_template("search.html", results=tweetresults, userresults=userresults, searchquery=searchquery, loginuser=[current_login["userid"],current_login["username"]])


@app.route("/login/<int:wrongcreds>", methods=["POST", "GET"])
def login(wrongcreds):
    wds = "true" if wrongcreds == 1 else "false"
    if request.method == "POST":
        rval = buttonhandler(request.form)
        if rval != None:
            return rval
    return render_template("login.html", wrongcreds=wds)


@app.route('/user/<int:userid>', methods=["POST", "GET"])
def userpage(userid):
    db.execute("select username from users where userid = "+str(userid)+";")
    username=db.fetchall()[0][0]
    db.execute("select u.username, t.tweet, t.tweettime, t.tweetid from tweets t, users u where u.userid = t.userid and u.userid = "+str(userid)+" order by tweettime desc;")
    tweets=db.fetchall()
    isfollowing = False
    if(current_login["userid"] != 'undef'):
        db.execute("select fr,fe from followers where fe = "+str(userid)+";")
        nid = db.fetchall()
        print(nid)
        if(len(nid)>0):
            isfollowing = True
    if request.method == "POST":
        rval = buttonhandler(request.form, userid=userid)
        if rval != None:
            return rval
    return render_template("user.html", loginuser=[current_login['userid'],current_login["username"]], user=[userid, username], tweets=tweets, isfollowing=isfollowing)


def logout():
    current_login["userid"] = "undef"
    current_login["username"] = "undef"
    db.execute("drop view if exists followers;")
    conn.commit()
    return

@app.route('/tweet/<int:tweetid>', methods=["POST", "GET"])
def tweetpage(tweetid):
    if current_login["userid"] == 'undef':
        db.execute("select u.userid, u.username, t.tweetid, t.tweet, t.tweettime, t.in_response_to_tweet, t.response_tweets, l.like_num from tweets t, users u, like_nums l where u.userid = t.userid and t.tweetid = "+str(tweetid)+" and t.tweetid = l.tweetid;")
    else:
        db.execute("select u.userid, u.username, t.tweetid, t.tweet, t.tweettime, t.in_response_to_tweet, t.response_tweets, l.like_num, case when t.tweetid = any(select tweetid from userlikes) then 'TRUE' else 'FALSE' end as userliked from tweets t, users u, like_nums l where u.userid = t.userid and t.tweetid = l.tweetid and t.tweetid = "+str(tweetid)+"; ")
    tweet = db.fetchall()[0]
    posts=[]
    if((tweet[6]) != None and len(tweet[6])>0):
        db.execute("select u.username, t.tweet, t.tweettime, u.userid, t.tweetid from tweets t, users u where u.userid = t.userid and t.tweetid = any(array"+str(tweet[6])+") order by tweettime desc fetch first 200 rows only;")
        posts=db.fetchall()
    if request.method == "POST":
        rval = buttonhandler(request.form, tweetid=tweetid, tweet=tweet, calledfrom='tweetpage')
        if rval != None:
            return rval
    inrespto = []
    if(tweet[5] != None and len(tweet[5])==1):
        db.execute("select u.username, t.tweet, t.tweettime, u.userid, t.tweetid from tweets t, users u where u.userid = t.userid and t.tweetid = "+str(tweet[5][0])+";")
        inrespto = db.fetchall()[0]
    return render_template("tweet.html", tweet=tweet, loginuser=[current_login["userid"],current_login["username"]], posts=posts, inrespto=inrespto)