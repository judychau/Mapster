"""Models and database functions for Mapster"""

from flask_sqlalchemy import SQLAlchemy
# This is the connection to the SQLite database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()




class User(db.Model):
    """User info"""

    __tablename__="users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    email = db.Column(db.String(50), nullable=True)
    password = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s name=%s age=%s email=%s>" % (self.user_id, self.name, self.age, self.email)


class User_Marker(db.Model):
    """user and marker association table to show relationship, one user has many markers"""

    __tablename__="user_markers"

    user_marker_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    marker_id = db.Column(db.Integer, db.ForeignKey('markers.marker_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    

    def __repr__(self):
        return "<User_Marker user_marker_id=%s marker_id=%s user_id=%s" % (self.user_marker_id, self.marker_id, self.user_id)

class Marker(db.Model):
    """pin/marker info"""

    __tablename__="markers"

    marker_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(200), nullable=True)
    address = db.Column(db.String(500), nullable=True)
    city = db.Column(db.String(200), nullable=True)
    state = db.Column(db.String(200), nullable=True)
    zipcode = db.Column(db.String(50), nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    business_id = db.Column(db.String(500), nullable=True)
    yelp_url = db.Column(db.String(500), nullable=True)
    rating = db.Column(db.Float(5), nullable=True)
    rating_img = db.Column(db.String(500), nullable=True)
    review_count = db.Column(db.Integer, nullable=True)
    longitude = db.Column(db.Float(50),nullable=True)
    latitude = db.Column(db.Float(50), nullable=True)
    map_cat = db.Column(db.String(100), nullable=True)
    neighborhood = db.Column(db.String(500), nullable=True)
    note = db.Column(db.String(500), nullable=True)
    
    def __repr__(self):

        return "<Marker marker_id=%s" % (self.marker_id)


    # Define relationship to user and marker; only have to do this in one class bc User_Marker/Marker_Categorites are pure association table
    # params for relationship(class name, table name, name to call class markers
    users = db.relationship("User", secondary='user_markers', backref=db.backref("markers"))


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our postgresql database
    # Create database connection
    DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql:///judychau")
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    # So that we can use Flask-SQLAlchemy, we'll make a Flask app
    from flask import Flask
    app = Flask(__name__)
    connect_to_db(app)
    print "Connected to Mapster DB."