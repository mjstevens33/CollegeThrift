import os
import urllib

from flask import render_template, flash, redirect, url_for, request, current_app
from app import app, db
from app.forms import LoginForm, RegistrationForm, ItemForm
from app.models import User, Post, Category
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename

# merging to main

@app.route('/')
@app.route('/Home')
def Home():
    posts = Post.query.order_by(Post.created_at.desc()).limit(6).all()
    return render_template('index.html', title='Home', posts=posts)


@app.route('/post/<int:post_id>')
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)  # Fetch the post or return 404 if not found
    return render_template('post_detail.html', post=post)  # Assume you have a template named 'post_detail.html'


@app.route('/browse')
def browse():
    query = request.args.get('query', '')
    category_id = request.args.get('category', None)
    category_name = None  # Initialize category_name

    items = Post.query

    if query:
        search = "%{}%".format(query)
        items = items.filter(
            db.or_(
                Post.title.ilike(search),
                Post.description.ilike(search)
            )
        )

    if category_id:
        category = Category.query.get(category_id)  # Get the category object
        if category:  # If a category is found
            category_name = category.name  # Set category_name
            items = items.filter_by(category_id=category.id)  # Filter items by category

    items = items.all()
    categories = Category.query.all()
    # Pass category_name to the template
    return render_template('browse.html', items=items, categories=categories, query=query, category_id=category_id, category_name=category_name)




@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('Home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urllib.parse.urlsplit(next_page).netloc != '':
            next_page = url_for('Home')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

#jh
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('Home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('Home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, firstname=form.firstName.data, lastname=form.lastName.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('Home'))
    return render_template('register.html', title='Register', form=form)

@app.route('/reset_db')
def reset_db():
    flash("Resetting database: deleting old data and repopulating with dummy data")
    # clear all data from all tables
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print('Clear table {}'.format(table))
        db.session.execute(table.delete())
    db.session.commit()
    categories = ['Tech', 'School', 'Clothes']
    for name in categories:
        category = Category(name=name)
        db.session.add(category)
    db.session.commit()
    return render_template('index.html', title='Home')



@app.route('/add_item', methods=['GET', 'POST'])
# @login_required  # Ensure only logged-in users can add items
def add_item():
    form = ItemForm()
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]
    if form.validate_on_submit():
        # Save the image
        if form.image.data:
            image_file = form.image.data
            filename = secure_filename(image_file.filename)
            file_path = os.path.join(current_app.root_path, 'static/images', filename)
            image_file.save(file_path)

        item = Post(
            title=form.name.data,
            description=form.description.data,
            price=form.price.data,
            category_id=form.category_id.data,
            image_url="default.jpeg" #filename   Assuming you have an image_url field in your Post model
        )
        db.session.add(item)
        db.session.commit()
        flash('Item has been added!', 'success')
        return redirect(url_for('browse'))
    return render_template('add_item.html', title='Add New Item', form=form)

@app.route('/about')
def About():
    return render_template('about.html', title='About')
