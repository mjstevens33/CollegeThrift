from app import app, db
from app.models import Category, Post
import random


def add_categories():
    categories = ['Tech', 'School', 'Clothes']
    for name in categories:
        category = Category(name=name)
        db.session.add(category)
    db.session.commit()


def add_posts():
    for i in range(20):
        post = Post(
            title=f'Item {i}',
            description=f'Description for item {i}',
            price=random.uniform(10.0, 500.0),
            category_id=random.randint(1, 3),  # Assuming 3 categories
            image=f'image_{i}.jpg',
        )
        db.session.add(post)
    db.session.commit()


# Create and push an application context
with app.app_context():
    add_categories()
    add_posts()
