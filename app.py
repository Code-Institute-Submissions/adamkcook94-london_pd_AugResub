import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/pending_inv")
def pending_inv():
    pending = mongo.db.pending.find()
    return render_template("pending.html", pending=pending)


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    pending = mongo.db.pending.find({"$text": {"$search": query}})
    return render_template("pending.html", pending=pending)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("my_submissions", username=session["user"]))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(request.form.get("username")))
                return redirect(url_for(
                    "my_submissions", username=session["user"]))

            else:
                flash("Incorrect username or password")
                return redirect(url_for("login"))

        else:
            flash("Incorrect username or password")
            return redirect(url_for("login"))
    return render_template("login.html")


@app.route("/my_submissions/<username>", methods=["GET", "POST"])
def my_submissions(username):
    # grab user from mongoDB. follow this pathway for specific user data.
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        return render_template("my_submissions.html", username=username)

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/submit_investigation", methods=["GET", "POST"])
def submit_investigation():
    if request.method == "POST":
        investigation = {
            "crime_name": request.form.get("crime_name"),
            "family_name": request.form.get("family_name").upper(),
            "forename": request.form.get("forename"),
            "gender": request.form.get("gender"),
            "last_seen": request.form.get("last_seen"),
            "date_of_birth": request.form.get("date_of_birth"),
            "nationality": request.form.get("nationality"),
            "ethnicity": request.form.get("ethnicity"),
            "phone_number": request.form.get("phone_number"),
            "email": request.form.get("email"),
            "additional_info": request.form.get("additional_info"),
            "submitted_by": session["user"]
        }
        mongo.db.pending.insert_one(investigation)
        flash("Investigation submitted.")
        return redirect(url_for('home'))
    crime = mongo.db.crime.find().sort("crime_name", 1)
    return render_template("submit_investigation.html", crime=crime)


@app.route("/edit_inv/<pendings_id>", methods=["GET", "POST"])
def edit_inv(pendings_id):
    if request.method == "POST":
        investigation = {
            "crime_name": request.form.get("crime_name"),
            "family_name": request.form.get("family_name").upper(),
            "forename": request.form.get("forename"),
            "gender": request.form.get("gender"),
            "last_seen": request.form.get("last_seen"),
            "date_of_birth": request.form.get("date_of_birth"),
            "nationality": request.form.get("nationality"),
            "ethnicity": request.form.get("ethnicity"),
            "phone_number": request.form.get("phone_number"),
            "email": request.form.get("email"),
            "additional_info": request.form.get("additional_info"),
            "submitted_by": session["user"]
        }
        mongo.db.pending.update({"_id": ObjectId(pendings_id)}, investigation)
        flash("Investigation edited.")
        return redirect(url_for('pending_inv'))
    pendings = mongo.db.pending.find_one({"_id": ObjectId(pendings_id)})
    crime = mongo.db.crime.find().sort("crime_name", 1)
    return render_template("edit_inv.html", pendings=pendings, crime=crime)


@app.route("/delete_task/<pendings_id>")
def delete_inv(pendings_id):
    mongo.db.pending.remove({"_id": ObjectId(pendings_id)})
    flash("Investigation deleted")
    return redirect(url_for("pending_inv"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
