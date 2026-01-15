from flask import Flask, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from random import randint as rd
from dotenv import load_dotenv
import os, datetime

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db = SQLAlchemy(app)

# ---------------- MODEL ----------------

class User(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    NAME = db.Column(db.String(50))
    MOVES = db.Column(db.Integer)
    SCORE = db.Column(db.Integer)
    TIME = db.Column(db.DateTime, default=datetime.datetime.utcnow)

# ---------------- GAME LOGIC ----------------



def avg(l:list)->float:
    return sum(l)/len(l)


def cvu(uch,USERCHOICES,moves):
    
    USERCHOICES.append(uch)
    print(f"USCHL : {USERCHOICES}")
    avguch = int(avg(USERCHOICES))
    print(f"AVG UCH : {avguch}")
    posCch = {1:2,2:3,3:1}
    negCch = {1:1,2:2,3:3}
    cch = posCch[avguch]
    var = rd(1,100)
    
    if cch == uch:
        cch = posCch[cch]
    print(f"CCH : {cch}")
    if var%moves+1 == 0 :
        return 1, negCch[cch], USERCHOICES
    if uch == cch:
        return -1, cch,  USERCHOICES   # draw
    elif (uch == 1 and cch == 2) or (uch == 2 and cch == 3) or (uch == 3 and cch == 1):
        return 0, cch,  USERCHOICES   # user loses
    else:
        return 1, cch,  USERCHOICES    # user wins

# ---------------- ROUTES ----------------

@app.route("/")
def root():
    session.clear()
    return redirect(url_for("scp"))

@app.route("/scp", methods=["GET", "POST"])
def scp():

    # initialize session values once
    if "hist" not in session:
        session['hist']=[]
    if "userscore" not in session:
        session["userscore"] = 0
    if "moves" not in session:
        session["moves"] = 0

    if request.method == "POST":

        # win condition
        if session["userscore"] >= 100:
            session["won"] = True
            return render_template("askname.html")

        session["moves"] += 1

        uchval = request.form.get("radioDefault")
        if not uchval:
            return render_template("SPC.html", ans=4)

        ch = {"stone": 1, "paper": 2, "scissor": 3}
        chl = ["stone", "paper", "scissor"]

        ans = cvu(ch[uchval],session.get('hist'),session.get('moves'))
        session['hist']=ans[2]
        # scoring
        if ans[0] == 1:          # win
            session["userscore"] += 10
        elif ans[0] == -1:      # draw
            session["userscore"] += 5
        else:                   # lose
            session["userscore"] -= 5

        return render_template(
            "SPC.html",
            ans=ans[0],
            cch=chl[ans[1]-1],
            uch=uchval,
            score=session["userscore"]
        )

    return render_template("SPC.html", ans=4)

# ---------------- SAVE USER ----------------

@app.route("/askname", methods=["POST"])
def askname():
    if session.get("userscore", 0) >= 100:
        name = request.form.get("name")

        user = User(
            NAME=name,
            SCORE=session["userscore"],
            MOVES=session["moves"]
        )

        try:
            db.session.add(user)
            db.session.commit()
        except:
            print("FAILED TO ADD USER")

    return redirect(url_for("leaderboards"))

# ---------------- LEADERBOARD ----------------

@app.route("/leaderboards")
def leaderboards():
    lead = User.query.order_by(User.MOVES.asc()).all()
    return render_template("lead.html", lead=lead)

# ---------------- RESET ----------------

@app.route("/rw")
def rw():
    session.pop("won", None)
    return redirect(url_for("root"))

# ---------------- MAIN ----------------

if __name__ == "__main__":
    
    app.run(host="0.0.0.0", port=5000, threaded =True)
