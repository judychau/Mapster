"""Mapster Server"""
from scripts import gmaps_request
from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
#from model import User, User_Points, Marker, Category, connect_to_db, db

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



@app.route("/gmaps_data", methods=['POST'])
def gmaps_results():
    """use user input (from homepage) as the query parameter of url to display search results in gmaps_data.html"""

    search = request.form['search'] 
    destination = request.form['destination']

    json= gmaps_request(search, destination) #results from scripts gmaps_api function

    return render_template("gmaps_data.html",json=json) #return info to html gmaps_data

# @app.route("", methods=['POST'])
# def user_markers():
#     """Let user save markers/location (save markers to db)"""




if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    # connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()