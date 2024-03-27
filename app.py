import os
import json
from flask import Flask, request, render_template, Response, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

# Creating the flask app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{os.environ['DB_UN']}:{os.environ['DB_PW']}@localhost:5432/{os.environ['DB']}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Creating the database
db = SQLAlchemy(app)

# Defining the table
class Cat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)

# Creating the context
with app.app_context() as context:
    context.push()

# Creating the table
db.create_all()

# Creating the routes for the app

# This route allows the user to view the existing cats
@app.route("/", methods=["GET"])
def home():
    cats = Cat.query.all()
    return render_template("index.html", cats=cats)

# This route allows the user to make a new cat
@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "GET":
        return render_template("create.html")

    if request.method == "POST":
        # Creating the new cat object based off of json data
        new_cat = Cat(name=request.json["name"], color=request.json["color"], age=request.json["age"])

        # Adding the object to the database
        db.session.add(new_cat)
        db.session.commit()

        # Returning a response
        return redirect(url_for("home"))

# This route allows the user to edit an existing cat
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    # Getting the cat
    cat = Cat.query.get_or_404(id)

    # If the method is get, then the program loads the edit page
    if request.method == "GET":
        return render_template("edit.html", cat=cat)

    # If the method is post, then the program edits the cat object
    if request.method == "POST":
        # Getting the json data
        data = request.json

        # Getting the values from the json
        cat.name = data["name"]
        cat.color = data["color"]
        cat.age = data["age"]

        # Updating the cat and saving the changes
        db.session.add(cat)
        db.session.commit()

        # Returns a response
        return redirect(url_for("home"))

# This route allows the user to delete an existing cat
@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    cat = Cat.query.get_or_404(id)
    db.session.delete(cat)
    db.session.commit()

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(port="80")
