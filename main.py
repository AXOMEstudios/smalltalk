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
		return render_template("st.html",
		                       mails=db[session["username"]]["msg"],
		                       count=len(db[session["username"]]["msg"]),
		                       storage=round(len(str(db[session["username"]]))/1024,2))
	except KeyError:
		return render_template("index.html", users=len(db.keys()))


@app.route("/login", methods=["GET", "POST"])
def login():
	username = auth.login(request.args.get("usr"))
	session["username"] = username
	if not username in list(db.keys()):
		db[username] = {
		    "msg": []
		}
	return redirect("/")


@app.route("/st/")
def smalltalk():
	return render_template("st.html",
	                       mails=db[session["username"]]["msg"],
	                       count=len(db[session["username"]]["msg"]),
	                       storage=round(len(str(db[session["username"]]))/1024,2))


@app.route("/st/new/")
def write():
	return render_template("new.html", sub="", text="", rec="")


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
	    "id": randint(1000000000000000, 9999999999999999)
	}

	x = db[to]
	x["msg"].append(pre)
	db[to] = x

	return render_template("success.html")


def deleteMail(i, u):
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


def getMail(i, u):
	for x in db[u]["msg"]:
		if str(x["id"]) == str(i):
			return x
	else:
		deleteMail(i, u)
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
	i["text"] = i["text"].replace("\\n", "\\\\n")
	return render_template("reader.html", i=i)


@app.route("/del/<i>")
def delMail(i):
	deleteMail(i, session["username"])
	return redirect("/st/")


@app.route("/rep/<i>")
def replyMail(i):
	m = getMail(i, session["username"])
	s = "Reply: " + str(m["sub"])
	t = ""
	r = m["from"]
	return render_template("new.html", sub=s, text=t, rec=r)


@app.route("/fc/")
def flowcloud():
	if "username" in session.keys():
		return render_template("st.html")
	else:
		return render_template("setupfc.html")


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


app.run(host="0.0.0.0", port=8080)
