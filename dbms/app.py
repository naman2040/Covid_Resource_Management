import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db1 = SQL("sqlite:///resources.db")
db2 = SQL("sqlite:///hospitals.db")


@app.route("/")
def index():
    session["hospital_name"] = "error"
    resources = db1.execute("SELECT * FROM resources")
    return render_template("index.html", resources=resources)

@app.route("/fetch", methods=["GET", "POST"])
def fetch():
    if request.method == "POST":
        hospital = request.form["hospital"]
        session["hospital_name"] = hospital
        return redirect("/update")

    
    else:
        hospitals = db2.execute("SELECT * FROM hospitals ORDER BY REG_ID")
        return render_template("fetch.html", hospitals=hospitals)

@app.route("/update", methods=["GET", "POST"])
def update():
    hospital_name = session["hospital_name"]
    reg_id = db2.execute("SELECT REG_ID FROM hospitals where NAME = ?", hospital_name)
        
    REG_ID = reg_id[0]['REG_ID']

    if request.method == "POST":
        OXYGEN = request.form["OXYGEN"]
        REMDESIVIR = request.form["REMDESIVIR"]
        VENTILATOR = request.form["VENTILATOR"]
        BEDS = request.form["BEDS"]

        db1.execute("update resources set OXYGEN = :oxygen, REMDESIVIR = :remdesivir, VENTILATOR = :ventilators, BEDS = :beds WHERE REG_ID = :reg_id", 
            reg_id = REG_ID, 
            oxygen = OXYGEN, 
            remdesivir = REMDESIVIR, 
            ventilators = VENTILATOR, 
            beds = BEDS
        )
        
        return redirect("/update")
        
    else: 
        
        Resources  =  db1.execute("SELECT * FROM resources where REG_ID = ?", REG_ID)
        resources=Resources[0]
        return render_template("update.html", hospital=hospital_name, resources=resources)
    