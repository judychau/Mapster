"""Mapster Server"""
from scripts import gmaps_request
from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
#from model import User, User_Points, Marker, Category, connect_to_db, db
from model import connect_to_db, db, User, Marker, User_Marker, Category, Marker_Category

app = Flask(__name__)
# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"
# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined



@app.route("/", methods=['GET'])
def index():
    """shows homepage where user will put in info"""

    return render_template("homepage.html")


@app.route('/login', methods=['GET'])
def login_form():
    """Show login form for user to log in"""

    return render_template("login_form.html")


@app.route('/login', methods=['POST'])
def login_process():
    """Log in user by checking to see if user is in user db and putting user in session"""

    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("User does not exist")
        return redirect("/login")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("%s, you are now logged in" % user.name)
    return redirect("/")


@app.route('/logout')
def logout():
    """Log out user from session"""

    del session["user_id"]
    flash("You are now logged out")
    return redirect("/")

@app.route('/register', methods=['GET'])
def register_form():
    """Show form for user to register/signup."""

    return render_template("register_form.html")


@app.route('/register', methods=['POST'])
def register_process():
    """Registration process, adding a new user to the db"""

    name = request.form["name"]
    age = request.form["age"]
    email = request.form["email"]
    password = request.form["password"]

    check = User.query.filter_by(email=email).all()

    if check:
        flash("This username already exists.")
        return redirect('/register')
    else:
        new_user = User(name=name, age=age, email=email, password=password)

        db.session.add(new_user)
        db.session.commit()

        session["user_id"] = new_user.user_id

        flash("%s is now registered" % name)
        return redirect("/")


@app.route("/gmaps_data", methods=['POST'])
def gmaps_results():
    """use user input (from homepage) as the query parameter of url to display search results in gmaps_data.html"""

    search = request.form['search'] 
    destination = request.form['destination']

    json = gmaps_request(search, destination) #results from scripts gmaps_api function

    return render_template("gmaps_data.html",json=json) #return info to html gmaps_data


@app.route("/save_marker", methods=['POST'])
def save_marker():
    """Lets users who are logged in save markers/location (save markers to db)"""

    name = request.form.get("name") #request.args.get is when you use the "GET" method
    address = request.form.get("address")
    place_id = request.form.get("placeId")
    longitude = request.form.get("longitude")
    latitude = request.form.get("latitude")
    category = request.form.get("category")

    user_id = session.get("user_id")

    check = Marker.query.filter_by(place_id=place_id).first()

    if not check:
    # #This will be inserted into the marker table of the DB (model.py) --dont forget to parse the category field
        new_marker = Marker(name=name, address=address, place_id=place_id, longitude=longitude, latitude=latitude)
        db.session.add(new_marker)
        db.session.commit()

        marker_id = new_marker.marker_id

        new_user_marker = User_Marker(user_id=user_id, marker_id=marker_id)
        db.session.add(new_user_marker)
        db.session.commit()

        flash("Location added")
        print new_marker
        print new_user_marker
    else:
        flash("You already saved this location")

    return "saved to database successfully"


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()