from app import app
from flask import render_template, request, session, redirect, abort
import psycopg2
from sqlalchemy.sql import text
import secrets
from werkzeug.security import check_password_hash, generate_password_hash

import classes
import restaurant_classes
import restaurants
import reviews
import users

# gathers data for main page view
@app.route("/")
def index():
    restaurants_ = restaurants.restaurants_for_index()
    classes_ = classes.get_all()
    restaurant_classes_ = restaurant_classes.get_all()
    reviews_ = reviews.reviews_for_index()
    dictionary_stars = {}
    dictionary_count = {}
    for restaurant in restaurants_:
        dictionary_stars[restaurant[0]] = 0
        dictionary_count[restaurant[0]] = 0
    for review in reviews_:
        dictionary_stars[review[1]] += review[0]
        dictionary_count[review[1]] += 1
    reviewslist_ = []
    for key, item in dictionary_stars.items():
        count = dictionary_count[key]
        reviewslist_.append((key, item, count))
    return render_template("index.html", restaurants=restaurants_, classes=classes_, restaurant_classes=restaurant_classes_, reviewslist=reviewslist_)

# gathers data for main page view, where content is sorted by ratings
@app.route("/sorted")
def sorted():
    restaurants_ = restaurants.restaurants_for_index()
    classes_ = classes.get_all()
    restaurant_classes_ = restaurant_classes.get_all()
    reviews_ = reviews.reviews_for_index()
    dictionary_stars = {}
    dictionary_count = {}
    for restaurant in restaurants_:
        dictionary_stars[restaurant[0]] = 0
        dictionary_count[restaurant[0]] = 0
    for review in reviews_:
        dictionary_stars[review[1]] += review[0]
        dictionary_count[review[1]] += 1
    reviewslist_ = []
    for key, item in dictionary_stars.items():
        count = dictionary_count[key]
        reviewslist_.append((key, item, count))
    reviewslist_.sort(key=lambda x: x[1]/x[2] if x[1] != 0 and x[2] != 0 else 0, reverse=True)
    return render_template("sorted.html", restaurants=restaurants_, classes=classes_, restaurant_classes=restaurant_classes_, reviewslist=reviewslist_)

#gathers data for search result view
@app.route("/search")
def result():
    query = request.args["query"]
    matches = restaurants.search(query)
    return render_template("search.html", matches=matches)

#handles logging in
@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    user = users.check(username)
    if not user:
        return render_template("index.html", error="Invalid username")
    else:
        hash_value = user.password
        if not check_password_hash(hash_value, password):
            return render_template("index.html", error="Invalid password")
    session["username"] = username
    session["csrf_token"] = secrets.token_hex(16)
    return redirect("/")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/")

#handles user creation
@app.route("/createuser", methods=["POST", "GET"])
def createuser():
    if request.method == "POST":
        username = request.form["username"]
        if len(username) < 3:
            return render_template("createuser.html", error="Username is too short")
        if len(username) > 16:
            return render_template("createuser.html", error="Username is too long")
        password = request.form["password"]
        if len(password) < 8:
            return render_template("createuser.html", error="Password is too short")
        if len(password) > 32:
            return render_template("createuser.html", error="Password length must be within 32 characters")
        user = users.check(username)
        if user:
            return render_template("createuser.html", error="Username already exists")
        users.create(username, password)
        session["username"] = username
        return redirect("/")
    else:
        return render_template("createuser.html")

#gathers data for showing restaurant creation page
@app.route("/newrestaurant")
def newrestaurant():
    classes_ = classes.get_all()
    return render_template("newrestaurant.html", classes=classes_)

#gathers data for showing class editing page
@app.route("/tagedit")
def tagedit():
    classes_ = classes.get_all()
    return render_template("tagedit.html", classes=classes_)

#handles modification of classes table
@app.route("/tagcreate", methods=["POST"])
def tagcreate():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    deletions = request.form.getlist("deletions")
    classes.delete(deletions)
    answers = request.form.getlist("answer")
    classes.insert(answers)
    return redirect("/tagedit")

#handles creation of new restaurant entry
@app.route("/createrestaurant", methods=["POST"])
def createrestaurant():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    name = request.form["name"]
    description = request.form["description"]
    restaurant_id = restaurants.new(name, description)
    tags = request.form.getlist("tag")
    restaurant_classes.insert(restaurant_id, tags)
    return redirect("/")

#gathers data needed for restaurant info editing view
@app.route("/editrestaurant/<int:id>")
def editrestaurant(id):
    restaurant = restaurants.restaurant_edit(id)
    restaurant_classes_ = restaurant_classes.for_editing(id)
    classes_ = classes.get_all()
    return render_template("editrestaurant.html", classes=classes_, restaurant=restaurant, restaurant_classes=restaurant_classes_)

#handles updating of restaurant information
@app.route("/updaterestaurant", methods=["POST"])
def updaterestaurant():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    name = request.form["name"]
    description = request.form["description"]
    restaurant_id = request.form["id"]
    restaurant_id = restaurants.update(name, description, restaurant_id)
    restaurant_classes.delete(restaurant_id)
    tags = request.form.getlist("tag")
    restaurant_classes.insert(restaurant_id, tags)
    return redirect("/")

#gathers data needed for new review page
@app.route("/newreview/<int:id>")
def newreview(id):
    restaurant = restaurants.for_review(id)
    return render_template("newreview.html", id=id, restaurant=restaurant)

#handles creation of new review
@app.route("/review", methods=["POST"])
def review():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    restaurant_id = request.form["id"]
    stars = request.form["stars"]
    textreview = request.form["textreview"]
    if len(textreview) > 500:
        restaurant = request.form["restaurant"]
        return render_template("newreview.html", error="Review text is too long", restaurant=restaurant, id=restaurant_id, stars=stars, textreview=textreview)
    reviewer = request.form["reviewer"]
    reviews.new(restaurant_id, stars, textreview, reviewer)
    return redirect("/reviewspage/" + str(restaurant_id))

#gathers data for showing review page of restaurant in question
@app.route("/reviewspage/<int:id>")
def reviewspage(id):
    restaurant = restaurants.restaurant_edit(id)
    reviews_ = reviews.reviews_for_restaurant(id)
    return render_template("reviewspage.html", reviews=reviews_, restaurant=restaurant)

#handles review deletion
@app.route("/deletereview/<int:id>")
def deletereview(id):
    restaurant_id = reviews.delete(id)
    return redirect("/reviewspage/" + str(restaurant_id))

#handles restaurant deletion
@app.route("/deleterestaurant/<int:id>")
def deleterestaurant(id):
    restaurants.delete(id)
    return redirect("/")