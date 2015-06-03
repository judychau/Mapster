"""Mapster Server"""
from scripts import query_api #, gmaps_request
from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
#from model import User, User_Points, Marker, Category, connect_to_db, db
from model import connect_to_db, db, User, Marker, User_Marker, Category, Marker_Category, Neighborhood, Marker_Nbhd

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


@app.route('/searchresults', methods=['GET'])
def yelp_results():
    """use user input as the query parameter of url to display search results in results.html"""
    #add sort parameter
    term = str(request.args.get('term'))
    location = str(request.args.get('location'))
    sort = int(request.args.get('sort'))

    data = query_api(term, location, sort)

    return render_template('results.html', data=data)


# @app.route("/gmaps_data", methods=['POST'])
# def gmaps_results():
#     """use user input as the query parameter of url to display search results in gmaps_data.html"""

#     search = request.form['term'] 
#     destination = request.form['location']

#     json = gmaps_request(search, destination) #results from scripts gmaps_api function

#     return render_template("gmaps_data.html",json=json) #return info to html gmaps_data


@app.route("/savemarker", methods=['POST'])
def save_marker():
    """Lets users who are logged in save markers/location (save markers to db)"""

    name = request.form.get("name") #request.args.get is when you use the "GET" method
    address = request.form.get("address")
    city = request.form.get("city")
    state = request.form.get("state")
    zipcode = request.form.get("zipcode")
    phone = request.form.get("phone")
    business_id = request.form.get("business_id")
    yelp_url = request.form.get("yelp_url")
    rating = request.form.get("rating")
    rating_img = request.form.get("rating_img")
    review_count = request.form.get("review_count")
    longitude = request.form.get("longitude")
    latitude = request.form.get("latitude")
    category = request.form.get("category")
    neighborhood = request.form.get("neighborhood")

    user_id = session.get("user_id")

    # #This will be inserted into the marker table of the DB (model.py) --dont forget to parse the category and neighborhood field
    new_marker = Marker(name=name, address=address, city=city, state=state, zipcode=zipcode,
    phone=phone, business_id=business_id, yelp_url=yelp_url, rating=rating, rating_img=rating_img, review_count=review_count, longitude=longitude, latitude=latitude)
    db.session.add(new_marker)
    db.session.commit()

    # new_cat = category(=cat_type)
    # new_nbhd = neighborhood()

    marker_id = new_marker.marker_id
    # cat_id = new_cat.cat_id
    # nbhd_id = new_nbhd.nbhd_id

    new_user_marker = User_Marker(user_id=user_id, marker_id=marker_id)
    db.session.add(new_user_marker)
    db.session.commit()

@app.route("/mymap", methods=['GET'])
def display_marker():
    """display user's markers"""

    user_id = session.get("user_id") #check if user is logged in
    user = User.query.get(user_id) #query db for user in session
    print user
    
    user_markers = User_Marker.query.filter(User_Marker.user_id==user_id).all()
    print user_markers

    markers = Marker.query.filter(Marker.marker_id==User_Marker.marker_id).all()
    print markers

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
        # json_compiled[marker.marker_id]['category'] = marker.category
        # json_compiled[marker.marker_id]['neighborhood'] = marker.neighborhood

    return render_template("mymap.html", markers=json_compiled)
    print json_compiled

@app.route("/mymap/<int:marker_id>", methods=['POST'])
def marker_note():
    """user can add/edit marker note"""

    note = str(request.form["note"])

    user_id = session.get("user_id")
    if not user_id:
        raise Exception("No user logged in.")

    user_marker = User_Marker.query.filter_by(user_id=user_id, marker_id=marker_id).first()

    if user_marker:
        user_marker.note = note
        flash("Note updated.")

    else:
        user_marker = User_Marker(user_id=user_id, marker_id=marker_id, note=note)
        flash("Note added.")
        db.session.add(user_marker)

    db.session.commit()

    return redirect("/mymaps/%s") % marker_id 






if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()