import os
from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# -----------------------------------------------------------------------------
# 1. Determine absolute path to this script’s directory
# -----------------------------------------------------------------------------
#    This ensures that no matter where you run the app from, we
#    always point SQLAlchemy at the correct cafes.db file next to app.py.
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'cafes.db')

# -----------------------------------------------------------------------------
# 2. Flask application setup
# -----------------------------------------------------------------------------
app = Flask(__name__)
# Tell Flask‑SQLAlchemy where our SQLite file lives.
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
# Disable the overhead of tracking every object modification.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# -----------------------------------------------------------------------------
# 3. Initialize the database extension
# -----------------------------------------------------------------------------
#    This creates a `db` object that we’ll use to define models and sessions.
db = SQLAlchemy(app)

# -----------------------------------------------------------------------------
# 4. Define the Cafe model
# -----------------------------------------------------------------------------
#    This class maps directly to a `cafe` table in SQLite.
class Cafe(db.Model):
    __tablename__ = 'cafe'  # Explicit table name

    # Columns in the `cafe` table:
    id             = db.Column(db.Integer, primary_key=True)
    name           = db.Column(db.String(250), unique=True, nullable=False)
    map_url        = db.Column(db.String(500), nullable=False)
    img_url        = db.Column(db.String(500), nullable=False)
    location       = db.Column(db.String(250), nullable=False)
    seats          = db.Column(db.String(250), nullable=False)
    has_toilet     = db.Column(db.Boolean, nullable=False)
    has_wifi       = db.Column(db.Boolean, nullable=False)
    has_sockets    = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price   = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        """
        Convert this Cafe object into a dictionary.
        Useful for JSON APIs or for quickly introspecting all attributes.
        """
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

# -----------------------------------------------------------------------------
# 5. Auto-create tables before the first HTTP request
# -----------------------------------------------------------------------------
#    If the `cafe` table (or `cafes.db` itself) doesn't yet exist, this
#    hook will create it automatically on startup.
@app.before_first_request
def create_tables():
    db.create_all()

# -----------------------------------------------------------------------------
# 6. Route definitions
# -----------------------------------------------------------------------------

@app.route("/")
def home():
    """
    Render the home page.
    Template: templates/index.html
    """
    return render_template("index.html")


@app.route("/cafes")
def show_cafes():
    """
    Query all Cafe rows, ordered by name, and render them.
    Template: templates/cafes.html
    """
    cafes = (
        db.session
          .execute(db.select(Cafe).order_by(Cafe.name))
          .scalars()
          .all()
    )
    return render_template("cafes.html", cafes=cafes)


@app.route("/add-cafe", methods=["GET", "POST"])
def add_cafe_page():
    """
    - GET:  Show an HTML form to add a new cafe.
    - POST: Process form data, create a Cafe object, commit to DB, and redirect.
    Template (GET): templates/add_cafe.html
    """
    if request.method == "POST":
        # Build a Cafe instance from form fields
        new = Cafe(
            name=request.form["name"],
            map_url=request.form["map_url"],
            img_url=request.form["img_url"],
            location=request.form["location"],
            seats=request.form["seats"],
            has_toilet=bool(request.form.get("has_toilet")),
            has_wifi=bool(request.form.get("has_wifi")),
            has_sockets=bool(request.form.get("has_sockets")),
            can_take_calls=bool(request.form.get("can_take_calls")),
            coffee_price=request.form["coffee_price"],
        )
        # Add and commit the new row
        db.session.add(new)
        db.session.commit()
        # Redirect to the cafes listing page
        return redirect(url_for("show_cafes"))

    # If GET, just render the form
    return render_template("add_cafe.html")


@app.route("/delete-cafe/<int:cafe_id>", methods=["POST"])
def delete_cafe_page(cafe_id):
    """
    Handle deletion of a cafe. Triggered via a POST form on the cafes page.
    - Fetch the cafe by ID (404 if not found)
    - Delete and commit
    - Redirect back to /cafes
    """
    cafe = db.get_or_404(Cafe, cafe_id)
    db.session.delete(cafe)
    db.session.commit()
    return redirect(url_for("show_cafes"))

# -----------------------------------------------------------------------------
# 7. Start the Flask dev server
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    # debug=True reloads on file changes and shows detailed error pages.
    app.run(debug=True)
