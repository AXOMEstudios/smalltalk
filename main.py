from flask import Flask, request, redirect, render_template, session
from replit import db
from hashlib import sha512
from os import getenv
import datetime
from random import randint
import axomeapis.auth as auth

app = Flask(__name__)
app.config["SECRET_KEY"] = getenv("TOKEN")

@app.route("/")
def index():
  try:
    session["username"]
    return render_template("st.html",mails=db[session["username"]]["msg"],count=len(db[session["username"]]["msg"]))
  except KeyError:
    return render_template("index.html")
    
@app.route("/login/",methods=["GET","POST"])
def login():
  username = auth.login(request.args.get("usr"))
  session["username"] = username
  if not username in list(db.keys()):
    return "<script>alert('This user does not exist. Create it!');document.location.href = '/signup/';</script>"
  if sha512(password.encode()).hexdigest() == db[username]["pw"]:
    session["username"] = username
    return redirect("/")
  else:
    return "<script>alert('The given password is wrong.');document.location.href='/';</script>"
    
@app.route("/st/")
def smalltalk():
  return render_template("st.html",mails=db[session["username"]]["msg"],count=len(db[session["username"]]["msg"]))
  
@app.route("/st/new/")
def write():
  return render_template("new.html",sub="",text="",rec="")
  
@app.route("/st/post/", methods=["POST"])
def postTalk():
  talk = request.form["txt"]
  to = request.form["to"]
  fr = session["username"]
  sub = request.form["subject"]
   
  if talk == "" or not talk:
    return render_template("failed.html")
  
  n = datetime.datetime.now()
  t = f"{n.day}.{n.month}.{n.year} {n.hour}:{n.minute}:{n.second}"
    
  pre = {
    "sub": sub,
    "meta": t,
    "from": fr,
    "text": str(talk),
    "id": randint(1000000000000000,9999999999999999)
  }
  
  x = db[to]
  x["msg"].append(pre)
  db[to] = x
  
  return render_template("success.html")

def getMail(i,u):
  for x in db[u]["msg"]:
    if str(x["id"]) == str(i):
      return x
  else:
    return {
    "sub": "Mail not found",
    "meta": "",
    "from": "Mailing system",
    "text": "This mail couldn't be found.",
    "id": 0
  }
  
def deleteMail(i,u):
  for x in db[u]["msg"]:
    if str(x["id"]) == str(i):
      y = db[u]
      z = y["msg"]
      z.remove(x)
      y["msg"] = z
      db[u] = y
  else:
    return {
    "sub": "Mail not found",
    "meta": "",
    "from": "Mailing system",
    "text": "This mail couldn't be found.",
    "id": 0
  }
  
@app.route("/r/<mid>")
def readMail(mid):
  i = getMail(mid, session["username"])
  return '''<!DOCTYPE html>
<html>
  <head>
    <title>Mail reader</title>
    <link rel="icon" href="/static/icon.png">
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Overpass&display=swap');
      * {
        font-family: "Overpass", Sans-Serif;
      }
      body {
        padding: 0;
        margin: 0;
        background-size: 100%;
        background-repeat: no-repeat;
      }
      main {
        background-color: white;
        text-align: start;
        color: black;
        padding: 15px;
      }
      .button {
        all: unset;
        width: 90%;
        padding: 10px;
        font-size: 20px;
        border-radius: 15px;
        border: 2px solid dodgerBlue;
        box-shadow: 0 0 15px dodgerBlue;
        margin: 10px;
      }
    </style>
  </head>
  <body>
    <main>
      <h2>'''+i["sub"]+'''</h2>
      <h3>From: '''+i["from"]+''', sent at: '''+i["meta"]+'''</h3>
      <hr>
      <p>'''+i["text"].replace("\n","<br>")+'''</p>
      </main>
  </body>
</html>'''
  
@app.route("/del/<i>")
def delMail(i):
  deleteMail(i,session["username"])
  return redirect("/st/")
  
@app.route("/rep/<i>")
def replyMail(i):
  m = getMail(i,session["username"])
  s = "Reply: " + str(m["sub"])
  t = f'''
  
  ———————————————
  Original talk:
    {m["text"]}'''
  r = m["from"]
  return render_template("new.html",sub=s,text=t,rec=r)
  
@app.route("/logout/")
def logout():
  del session["username"]
  return redirect("/")
  
@app.errorhandler(500)
def error500(e):
  e = ""
  return render_template("fail.html")
  
@app.errorhandler(400)
def error400(e):
  e = ""
  return render_template("fail.html")
  
@app.errorhandler(404)
def error404(e):
  e = ""
  return render_template("fail.html")

app.run(host="0.0.0.0",port=8080)