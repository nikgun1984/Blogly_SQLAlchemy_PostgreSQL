"""Blogly application."""

from flask import Flask, render_template, redirect, flash, request
from models import db, connect_db
from flask_debugtoolbar import DebugToolbarExtension

from models import db,  connect_db, User

app = Flask(__name__)

""" Configurations """

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'whateverpassword'
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.config["DEBUG_TB_HOSTS"] = ["dont-show-debug-toolbar"]

"""Debugger Initialiqzation"""
debug  = DebugToolbarExtension(app)

"""Connect to Database and create all tables"""
connect_db(app)
db.create_all()

@app.route('/')
def get_users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/create_user')
def create_user():
    return render_template('create_user.html')

@app.route('/create_user', methods=["POST"])
def submit_user():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["picture"]

    new_user  = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect(f'/{new_user.id}')

@app.route("/<int:user_id>")
def show_user(user_id):
    """Show details about a single user"""
    user = User.query.get_or_404(user_id)
    return render_template("user_details.html", user=user)

