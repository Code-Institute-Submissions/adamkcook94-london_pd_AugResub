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


@app.route("/stay_safe")
def stay_safe():
    return render_template("stay_safe.html")


@app.route("/wanted")
def wanted():
    wanted_persons = mongo.db.wanted_persons.find()
    users = mongo.db.users.find()
    return render_template("wanted_persons.html",
                           wanted_persons=wanted_persons, users=users)


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    wanted_persons = mongo.db.wanted_persons.find(
        {"$text": {"$search": query}})
    return render_template("wanted_persons.html",
                           wanted_persons=wanted_persons)


def creating_new_user(request):
    register = {
        "username": request.form.get("username").lower(),
        "password": generate_password_hash(request.form.get("password"))
    }
    mongo.db.users.insert_one(register)

    session["user"] = request.form.get("username").lower()
    flash("Registration Successful!")
    return True


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        if creating_new_user(request):
            return redirect(url_for("submit_investigation",
                                    username=session["user"]))
    return render_template("register.html")


def is_user_authenticated(request):
    existing_user = mongo.db.users.find_one(
        {"username": request.form.get("username".lower())}
    )
    if check_password_hash(
            existing_user["password"], request.form.get("password")):
        session["user"] = request.form.get("username").lower()
        flash("Welcome, {}".format(request.form.get("username")))
        return True
    else:
        return False


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            if is_user_authenticated(request):
                return redirect(url_for(
                    "submit_investigation", username=session["user"]))
            else:
                flash("Incorrect username or password")
                return redirect(url_for("login"))

        else:
            flash("Incorrect username or password")
            return redirect(url_for("login"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


def form_submission():
    investigation = {
        "crime_name": request.form.get("crime_name"),
        "family_name": request.form.get("family_name").upper(),
        "forename": request.form.get("forename"),
        "gender": request.form.get("gender"),
        "last_seen": request.form.get("last_seen"),
        "date_of_birth": request.form.get("date_of_birth"),
        "suspect_photo": request.form.get("suspect_photo"),
        "ethnicity": request.form.get("ethnicity"),
        "phone_number": request.form.get("phone_number"),
        "email": request.form.get("email"),
        "additional_info": request.form.get("additional_info"),
        "submitted_by": session["user"]
    }
    mongo.db.wanted_persons.insert_one(investigation)


@app.route("/submit_investigation", methods=["GET", "POST"])
def submit_investigation():
    if request.method == "POST":
        if form_submission():
            mongo.db.wanted_persons.insert_one()
        return redirect(url_for('wanted'),
                        flash("Investigation received."))
    gender = mongo.db.gender.find().sort("gender", 1)
    crime = mongo.db.crime.find().sort("crime_name", 1)
    return render_template("submit_investigation.html",
                           crime=crime, gender=gender)


def edit_submission_form(wanted_id):
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
    mongo.db.wanted_persons.update(
        {"_id": ObjectId(wanted_id)}, investigation)


@app.route("/edit/<wanted_id>", methods=["GET", "POST"])
def edit(wanted_id):
    if request.method == "POST":
        if edit_submission_form(wanted_id):
            mongo.db.wanted_persons.update(
                {"_id": ObjectId(wanted_id)})
        return redirect(url_for('wanted')), flash("Investigation edited.")
    wanted = mongo.db.wanted_persons.find_one({"_id": ObjectId(wanted_id)})
    gender = mongo.db.gender.find().sort("gender", 1)
    crime = mongo.db.crime.find().sort("crime_name", 1)
    return render_template("edit.html", wanted=wanted,
                           crime=crime, gender=gender)


@app.route("/delete_task/<wanted_id>")
def delete_inv(wanted_id):
    mongo.db.wanted_persons.remove({"_id": ObjectId(wanted_id)})
    flash("Investigation deleted")
    return redirect(url_for("wanted"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
