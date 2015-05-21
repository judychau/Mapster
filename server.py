"""Mapster Server"""
import requests
import json

from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from model import User, Marker, Category, Marker_detail, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined

@app.route("", methods=['GET'])
def gmaps_data():
    """shows info about a place"""

    query='' #request.form.(name of place)

    gmaps_key = 'AIzaSyCn6VQGxBbY14uHWiaIoRbPdx7OA4_RI7o'
    search_url= 'https://maps.googleapis.com/maps/api/place/textsearch/json?query=%s&key=%s' %query %gmaps_key

    api_data = requests.get(search_url)
    data = api_data.json()

    for item in data ['results']:
        name = item['name']
        place_id = item['place_id']
        address = item['formatted_address']
        latitude = item['geometry']['location']['lat']
        longitude = item['geometry']['location']['lng']
        category = item['types']

    return render_template("gmaps_data.html",
        name=name,
        place_id=place_id,
        address=address,
        latitude=latitude,
        longitude=longitude,
        category=category
        )

@app.route("", methods=['POST'])
def user_markers():
    """Let user save markers/location (save markers to db)"""




if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()