"""Models and database functions for hackbright project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the SQLite database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


#model definitions

class User(db.Model):
    """User of website"""

    __tablename__="users"


    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        return "<User user_id=%s email=%s password=%s>" % (self.user_id,self.email, self.password)


class Marker(db.Model):
    """pin/marker for features on map"""

    __tablename__="markers"

    marker_id = db.Column(db.Integer,primary_key=True)
    longitude = db.Column(db.float)
    latitude = db.Column(db.float)
    marker_name = db.Column(db.String)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    # this defines the back reference marker relationship to the user and category
    user= db.relationship("User",
                           backref = db.backref("markers", order_by=marker_id))

    user= db.relationship("Category",
                           backref = db.backref("markers", order_by=marker_id))


class Category(db.Model):
    """category of marker"""

    __tablename__="categories"

    category_id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String)
    sub_type = db.Column(db.String)
    icon = db.Column(db.String)


class Marker_Detail(db.Model):
    """marker info"""

    __tablename__="marker_details"

    detail_id = db.Column(db.Integer,primary_key=True)
    open_time = db.Column(db.DateTime)
    close_time = db.Column(db.DateTime)
    days_open = db.Column(db.String)
    days_closed = db.Column(db.String)
    marker_name = db.Column(db.Integer, db.ForeignKey('markers.marker_name'))

    user= db.relationship("Marker",
                           backref = db.backref("marker_detail", order_by=detail_id))



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
    print "Connected to DB."