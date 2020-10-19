"""Blogly application."""

from flask import Flask, render_template, redirect, flash, request
from models import db, connect_db
from flask_debugtoolbar import DebugToolbarExtension

from models import db,  connect_db, User, Post, Tag, PostTag

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

"""User's Routes"""

@app.route('/')
def get_users():
    posts = Post.query.order_by(Post.created_at.desc()).limit(5)
    return render_template('home.html', posts=posts)

@app.route('/users')
def display_users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/new')
def create_user():
    return render_template('create_user.html')

@app.route('/users/new', methods=["POST"])
def submit_user():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["picture"]

    new_user  = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    flash("This user was successfully added...","success")
    return redirect(f'/users/{new_user.id}')

@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Show details about a single user"""
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter(Post.user_id==user_id)
    return render_template("user_details.html", user=user,posts=posts)

@app.route("/users/<int:user_id>/edit")
def edit_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("edit_user.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["picture"]

    user = User.query.get(user_id)
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.commit()
    flash("This user was successfully edited...","success")
    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    flash("This user was successfully deleted...","success")
    return redirect('/users')

"""Post Routes"""

@app.route('/users/<int:user_id>/posts/new')
def create_post(user_id):
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('create_post.html', user = user, tags = tags)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def submit_post(user_id):
    title = request.form["title"]
    content = request.form["content"]
    tags = request.form.getlist('tags')
    new_post = Post(title=title, content=content, user_id=user_id)
    db.session.add(new_post)
    for tag in tags:
        tag_query = Tag.query.filter(Tag.name == tag).first()
        tag_obj = Tag.query.get(tag_query.id)
        tag_obj.posts.append(new_post)
    db.session.commit()
    flash("This post was successfully added...","success")
    return redirect('/users')

@app.route("/posts/<int:post_id>")
def show_post(post_id):
    post = Post.query.get(post_id)
    user = User.query.get(post.user_id)
    return render_template('show_post.html',post=post,user=user)

@app.route("/posts/<int:post_id>/edit")
def edit_form_post(post_id):
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template("edit_post.html", post=post, tags=tags)

@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post(post_id):
    title = request.form["title"]
    content = request.form["content"]
    tags = request.form.getlist('tags')
 
    post = Post.query.get(post_id)
    post.title = title
    post.content = content
    post.tags.clear()
    for tag in tags:
        tag_obj = Tag.query.filter(Tag.name == tag).first()
        post.tags.append(tag_obj)

    db.session.commit()
    flash("This post was successfully edited...","success")
    return redirect('/users')

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    flash("This post was successfully deleted...","success")
    return redirect('/users')

#Error Handling

@app.errorhandler(404)
def not_found(e): 
    return render_template("404.html")

#Tags Routes

@app.route('/tags')
def list_tags():
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def show_tag_posts(tag_id):
    tag = Tag.query.get(tag_id)
    return render_template('show_tag.html',tag=tag)

@app.route('/tags/new')
def create_tag():
    return render_template('create_tag.html', )

@app.route('/tags/new', methods=["POST"])
def submit_tag():
    tag_name = request.form["tag_name"]
    new_tag = Tag(name=tag_name.lower().title())
    db.session.add(new_tag)
    db.session.commit()
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def edit_tag(tag_id):
    tag_name = request.form["tag_name"]
    tag = Tag.query.get(tag_id)

    tag.name = tag_name
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    tag = Tag.query.get(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect('/tags')














