"""Mapster Server"""
import os 
from scripts import query_api #, gmaps_request
from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Marker, User_Marker

app = Flask(__name__)


# Required to use Flask sessions and the debug toolbar
SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', 'ABC')
app.secret_key = SECRET_KEY

# Fix Jinja undefined variable when it silently fails
app.jinja_env.undefined = StrictUndefined


##################
# HOMEPAGE ROUTE #
##################

@app.route("/", methods=['GET'])
def index():
    """shows homepage where user will put in info"""

    return render_template("homepage.html")


##################
#   USER LOGIN   #
##################

@app.route('/login', methods=['GET'])
def login_form():
    """Show login form for user to log in"""

    return render_template("login_form.html")


##################
# LOGIN PROCESS  #
##################

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


##################
#     LOGOUT     #
##################

@app.route('/logout')
def logout():
    """Log out user from session"""

    del session["user_id"]
    flash("You are now logged out")
    return redirect("/")


##################
#    REGISTER    #
##################

@app.route('/register', methods=['GET'])
def register_form():
    """Show form for user to register/signup."""

    return render_template("register_form.html")


####################
# REGISTER PROCESS #
####################

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


##################
#  YELP RESULTS  #
##################

@app.route('/searchresults', methods=['GET'])
def yelp_results():
    """use user input as the query parameter of url to display search results in results.html"""
    #add sort parameter
    term = str(request.args.get('term'))
    location = str(request.args.get('location'))
    sort = int(request.args.get('sort'))

    data = query_api(term, location, sort)

    return render_template('results.html', data=data)


###################
#   SAVE MARKER   #
###################

@app.route("/savemarker", methods=['POST'])
def save_marker():
    """Lets users who are logged in save markers/location (save markers to db)"""

    name = request.form.get("name") #request.args.get is when you use the "GET" method
    address = request.form.get("address")
    city = request.form.get("city")
    state = request.form.get("state")
    zipcode = request.form.get("zipcode")
    phone = request.form.get("phone")
    business_id = request.form.get("id")
    yelp_url = request.form.get("yelpUrl")
    rating = request.form.get("rating")
    rating_img = request.form.get("urlRatingStars")
    review_count = request.form.get("reviewCount")
    longitude = request.form.get("longitude")
    latitude = request.form.get("latitude")
    map_cat = request.form.get("category")
    neighborhood = request.form.get("neighborhoods")
    note = request.form.get("note")

    user_id = session.get("user_id")

    #This will be inserted into the marker table of the DB (model.py)
    new_marker = Marker(name=name, address=address, city=city, state=state, zipcode=zipcode,
    phone=phone, business_id=business_id, yelp_url=yelp_url, rating=rating, rating_img=rating_img, 
    review_count=review_count, longitude=longitude, latitude=latitude, map_cat=map_cat, neighborhood=neighborhood, note=note)
    db.session.add(new_marker)
    db.session.commit()

    marker_id = new_marker.marker_id

    new_user_marker = User_Marker(user_id=user_id, marker_id=marker_id)
    db.session.add(new_user_marker)
    db.session.commit()


###################
# DISPLAY MARKERS #
###################

@app.route("/mymap", methods=['GET'])
def display_marker():
    """get all user marker data from db to display on map"""

    user_id = session.get("user_id") #check if user is logged in
    user = User.query.get(user_id) #query db for user in session

    user_markers = User_Marker.query.filter(User_Marker.user_id==user_id).all()
    markers = Marker.query.filter(Marker.marker_id==User_Marker.marker_id).all()

    json_compiled = {}

    for marker in markers:
        json_compiled[marker.marker_id] = {}
        json_compiled[marker.marker_id]['marker_id'] = marker.marker_id
        json_compiled[marker.marker_id]['name'] = marker.name
        json_compiled[marker.marker_id]['address'] = marker.address
        json_compiled[marker.marker_id]['city'] = marker.city
        json_compiled[marker.marker_id]['state'] = marker.state
        json_compiled[marker.marker_id]['zipcode'] = marker.zipcode
        json_compiled[marker.marker_id]['phone'] = marker.phone
        json_compiled[marker.marker_id]['yelp_url'] = marker.yelp_url
        json_compiled[marker.marker_id]['rating'] = marker.rating
        json_compiled[marker.marker_id]['rating_img'] = marker.rating_img
        json_compiled[marker.marker_id]['review_count'] = marker.review_count
        json_compiled[marker.marker_id]['longitude'] = marker.longitude
        json_compiled[marker.marker_id]['latitude'] = marker.latitude
        json_compiled[marker.marker_id]['map_cat'] = marker.map_cat
        json_compiled[marker.marker_id]['neighborhood'] = marker.neighborhood
        json_compiled[marker.marker_id]['note'] = marker.note

    return render_template("mymap.html", markers=json_compiled)




    
###########################################
if __name__ == "__main__":

    connect_to_db(app)

    #heroku
    PORT = int(os.environ.get("PORT", 5000))
    DEBUG = "NO_DEBUG" not in os.environ

    app.run(debug=DEBUG, host="0.0.0.0", port=PORT)