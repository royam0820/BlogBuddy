import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-for-blog")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///blog.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize the app with the extension
db.init_app(app)

# Import models and forms after app initialization
from models import Post
from forms import PostForm

# Create tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    """Homepage showing all posts from newest to oldest"""
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('index.html', posts=posts)

@app.route('/create', methods=['GET', 'POST'])
def create_post():
    """Create a new blog post"""
    form = PostForm()
    
    if form.validate_on_submit():
        try:
            post = Post(
                title=form.title.data,
                content=form.content.data,
                category=form.category.data,
                image_url=form.image_url.data,
                created_at=datetime.utcnow()
            )
            db.session.add(post)
            db.session.commit()
            flash('Ton article a été créé avec succès! 🎉', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash('Oups! Une erreur s\'est produite. Essaie encore! 😊', 'error')
            logging.error(f"Error creating post: {e}")
    
    return render_template('create_post.html', form=form)

@app.route('/post/<int:post_id>')
def post_detail(post_id):
    """Show individual post detail"""
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', post=post)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
