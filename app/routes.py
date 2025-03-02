import logging
from flask import Blueprint, render_template, url_for, flash, redirect, request
from app import mongo, bcrypt
from app.forms import RegistrationForm, LoginForm,NewArticleForm
from app.models import create_article, add_comment, User
from flask_login import login_user, current_user, logout_user, login_required
from bson.objectid import ObjectId

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    return render_template('home.html')

# AUTHENTICATION
@main.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = {"username": form.username.data, "email": form.email.data, "password": hashed_password}
        mongo.db.users.insert_one(user)
        flash('Your account has been created!', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)

@main.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        print("Form validated successfully")  # Debug statement
        user = mongo.db.users.find_one({"email": form.email.data})
        if user and bcrypt.check_password_hash(user['password'], form.password.data):
            user_obj = User(user)
            login_user(user_obj, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    else:
        print(form.errors)  # Print validation errors

    return render_template('login.html', title='Login', form=form)


@main.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

# ARTICLE MANAGEMENT
@main.route("/articles", methods=['GET'])
def articles():
    articles = mongo.db.articles.find()
    return render_template('articles.html', articles=articles)

@main.route("/articles/<article_id>", methods=['GET'])
def article(article_id):
    article = mongo.db.articles.find_one({"_id": ObjectId(article_id)})
    if not article:
        flash('Article not found', 'danger')
        return redirect(url_for('main.articles'))
    return render_template('article.html', article=article)

@main.route("/articles/new", methods=['GET', 'POST'])
@login_required
def new_article():
    form = NewArticleForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        create_article(title, content, current_user.id)
        flash('Your article has been created!', 'success')
        return redirect(url_for('main.articles'))
    return render_template('new_article.html', form=form)

@main.route("/articles/<article_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = mongo.db.articles.find_one({"_id": ObjectId(article_id)})
    if not article:
        flash('Article not found', 'danger')
        return redirect(url_for('main.articles'))
    if article['author_id'] != current_user.id:
        flash('You are not authorized to edit this post.', 'danger')
        return redirect(url_for('main.articles'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        mongo.db.articles.update_one({"_id": ObjectId(article_id)}, {"$set": {"title": title, "content": content}})
        flash('Your article has been updated!', 'success')
        return redirect(url_for('main.article', article_id=article_id))
    return render_template('edit_article.html', article=article)

@main.route("/articles/<article_id>/delete", methods=['POST'])
@login_required
def delete_article(article_id):
    article = mongo.db.articles.find_one({"_id": ObjectId(article_id)})
    if not article:
        flash('Article not found', 'danger')
        return redirect(url_for('main.articles'))
    if article['author_id'] != current_user.id:
        flash('You are not authorized to delete this post.', 'danger')
        return redirect(url_for('main.articles'))
    mongo.db.articles.delete_one({"_id": ObjectId(article_id)})
    flash('Your article has been deleted!', 'success')
    return redirect(url_for('main.articles'))

# COMMENT MANAGEMENT
@main.route("/articles/<article_id>/comments", methods=['POST'])
@login_required
def comment(article_id):
    article = mongo.db.articles.find_one({"_id": ObjectId(article_id)})
    if not article:
        flash('Article not found', 'danger')
        return redirect(url_for('main.articles'))
    content = request.form['content']
    add_comment(article_id, content,current_user.username, current_user.id)
    flash('Your comment has been added!', 'success')
    return redirect(url_for('main.article', article_id=article_id))

@main.route("/articles/<article_id>/comments/<comment_id>/delete", methods=['POST'])
@login_required
def delete_comment(article_id, comment_id):
    article = mongo.db.articles.find_one({"_id": ObjectId(article_id)})

    if not article:
        flash('Article not found', 'danger')
        print("Article not found")
        return redirect(url_for('main.articles'))
    comment = next((comment for comment in article['comments'] if str(comment['_id']) == comment_id), None)
    if not comment:
        flash('Comment not found', 'danger')
        print("Comment not found")
        return redirect(url_for('main.article', article_id=article_id))
    if comment['author_id'] != current_user.id:
        flash('You are not authorized to delete this comment.', 'danger')
        print("You are not authorized to delete this comment.")
        return redirect(url_for('main.article', article_id=article_id))
    mongo.db.articles.update_one({"_id": ObjectId(article_id)}, {"$pull": {"comments": {"_id": comment_id}}})
    flash('Your comment has been deleted!', 'success')
    print("Your comment has been deleted!")
    return redirect(url_for('main.article', article_id=article_id))
