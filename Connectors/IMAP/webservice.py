#webservice for IMAP
from flask import Flask, render_template, url_for, request, redirect, send_file
import lockerfs
import time
import datetime
import urllib2
import thread
from limap import MailboxProcessor

app = Flask(__name__)

@app.route("/setupAuth")
def setupAuth():
    return render_template("setupAuth.html")

@app.route("/update")
def update():
    if app.consumerValidated:
        secrets = lockerfs.loadJsonFile("secrets.json");
        proc = MailboxProcessor(secrets["server"], secrets["username"], secrets["password"])
        thread.start_new_thread(proc.process,())
        return "Yep!"
    else:
        return redirect(url_for("setupAuth"))

@app.route("/save")
def saveAuth():
    secrets = lockerfs.loadJsonFile("secrets.json");
    secrets["username"] = request.args["username"]
    secrets["password"] = request.args["password"]
    secrets["server"] = request.args["server"]
    app.consumerValidated = True
    lockerfs.saveJsonFile("secrets.json", secrets)
    return redirect(url_for("mainIndex"))

@app.route("/")
def mainIndex():
    if app.consumerValidated:
        return "hello!!"
        #return render_template("index.html", updateTime=app.updateAt, updatesStarted=app.updatesStarted)
    else:
        return "redirect!"
#        return redirect(url_for("setupAuth"))

def runService(info):
    secrets = lockerfs.loadJsonFile("secrets.json");
    app.lockerInfo = info
    app.consumerValidated = "username" in secrets and "password" in secrets and "server" in secrets 
    app.debug = True
    app.run(port=app.lockerInfo["port"], use_reloader=False)

