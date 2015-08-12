   save marker function
   request from api:
    # categories = request.form.get("categories")
    # neighborhood = request.form.get("neighborhood")
    parsing category field:
    # catergoy list insert to db
    # split_cat = categories.replace(" ", "").split(",")
    # for item in split_cat:
    #     new_category = Category(category_type=item)
    #     category_id = new_category.category_id
    #     db.session.add(new_category)
    #     db.session.commit()
    
    # new_marker_cat = Marker_Category(marker_id=marker_id, category_id=category_id)

    # db.session.add(new_marker_cat)
    # db.session.commit()

    # new_nbhd = neighborhood()
    # nbhd_id = new_nbhd.nbhd_id

model.py for neighborhoods when applicable
#     neighborhoods = db.relationship("Neighborhood", secondary='marker_nbhd', backref=db.backref("markers"))


# class Neighborhood(db.Model):
#     """neighhborhood of marker, one marker has many neighborhoods"""

#     __tablename__="neighborhoods"

#     nbhd_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     nbhd_name = db.Column(db.String)


# class Marker_Nbhd(db.Model):
#     """marker and neighborhood association table to show relationship, one marker has many neighborhoods"""

#     __tablename__="marker_nbhd"

#     marker_nbdh_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     nbhd_id = db.Column(db.Integer, db.ForeignKey('neighborhoods.nbhd_id'))
#     marker_id = db.Column(db.Integer,db.ForeignKey('markers.marker_id'))


gmaps route to api request
@app.route("/gmaps_data", methods=['POST'])
def gmaps_results():
    """use user input as the query parameter of url to display search results in gmaps_data.html"""

    search = request.form['term'] 
    destination = request.form['location']

    json = gmaps_request(search, destination) #results from scripts gmaps_api function

    return render_template("gmaps_data.html",json=json) #return info to html gmaps_data

server
@app.route("/mymap", methods=['POST'])
def marker_note():
    """user can add/edit marker note""" 

    marker = Marker.query.get("marker_id")

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


mymap
         var contentString = '<div class="window-content">' +
            '<p><strong>Name: </strong>' + markers[key]['name'] + '</p>' +
            '<p><strong>Address: </strong>' + markers[key]['address'] + ' ' + markers[key]['city'] + ' ' + markers[key]['state'] + ' ' + markers[key]['zipcode'] + '</p>' +
            '<p><strong>Phone: </strong>' + markers[key]['phone'] + '</p>' +
            '<p><strong>Good for: </strong>' + markers[key]['map_cat'] + '</p>' +
            '<p><strong>Neighborhood: </strong>' + markers[key]['neighborhood'] + '</p>' +
            '<p><strong>Yelp: </strong>' + markers[key]['yelp_url'] + '</p>' +
            '<form action="mymap/' + markers[key]['marker_id'] + '" method="POST"><div class="form-group"><label>Notes:<input type="text" name="note" required class="form-control"></label></div><div class="form-group"><input type="submit" value="save" class="button"></div></form>' +
                '</div>';


delete a marker




gmaps api connection:
secrets.sh
export gmaps_key='AIzaSyCn6VQGxBbY14uHWiaIoRbPdx7OA4_RI7o'

def gmaps_request(search, destination):
    """requests info about a place using query parameter"""

    GMAPS_KEY=os.environ['gmaps_key'] 
    pre_query = search + '+' + destination
    QUERY = pre_query.replace(' ', '+') 

    url= 'https://maps.googleapis.com/maps/api/place/textsearch/json?query=%s&key=%s' %(QUERY, GMAPS_KEY)

    api_data = requests.get(url)
    data = api_data.json()

    #*******************test*******************
    pprint.pprint(data, indent=2)
    # return data #dictionary from json








          