"""Models and database functions for Mapster"""

from flask_sqlalchemy import SQLAlchemy
# This is the connection to the SQLite database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


#model definitions

class User(db.Model):
    """User info"""

    __tablename__="users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(64), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        return "<User user_id=%s email=%s password=%s>" % (self.user_id,self.email, self.password)


class User_Marker(db.Model):
    """user and marker association table to show relationship, one user has many markers"""

    __tablename__="user_markers"

    user_marker_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    marker_id = db.Column(db.Integer, db.ForeignKey('markers.marker_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))


class Marker(db.Model):
    """pin/marker info"""

    __tablename__="markers"

    marker_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)
    place_id = db.Column(db.String)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)

    # Define relationship to user and category; only have to do this in one class bc User_Marker/Marker_Categorites are pure association table
    # params for relationship(class name, table name, name to call class markers
    users = db.relationship("User", secondary='user_markers', backref=db.backref("markers"))
    categories = db.relationship("Category", secondary='marker_categories', backref=db.backref("markers"))

class Category(db.Model):
    """category of marker, one marker has many categories"""

    __tablename__="categories"

    category_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    category_type = db.Column(db.String)


class Marker_Category(db.Model):
    """marker and category association table to show relationship, one marker has many categories"""

    __tablename__="marker_categories"

    marker_cat_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'))
    marker_id = db.Column(db.Integer,db.ForeignKey('markers.marker_id'))


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.
    from server import app
    connect_to_db(app)
    print "Connected to Mapster DB."