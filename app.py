import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from datetime import datetime
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from functools import wraps
import markdown
from flask_wtf import FlaskForm
import re

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

# Flask-Login setup
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Import models and forms after app initialization
from models import Post, User, MessageBoard, Comment
from forms import PostForm, LoginForm, RegisterForm, MessageBoardForm, CommentForm, ResetPasswordForm, AdminReplyForm

# Create tables
with app.app_context():
    db.create_all()

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Accès réservé aux administrateurs.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def remove_invalid_surrogates(text):
    if not text:
        return text
    return re.sub(r'[\ud800-\udfff]', '', text)

class DummyForm(FlaskForm):
    pass

@app.route('/')
def index():
    """Homepage showing all posts from newest to oldest"""
    posts = Post.query.order_by(Post.created_at.desc()).all()
    form = DummyForm()
    for post in posts:
        post.html_content = markdown.markdown(post.content)
        post.comment_count = Comment.query.filter_by(post_id=post.id).count()
    return render_template('index.html', posts=posts, form=form)

@app.route('/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_post():
    """Create a new blog post"""
    form = PostForm()
    
    if form.validate_on_submit():
        try:
            post = Post(
                title=remove_invalid_surrogates(form.title.data),
                content=remove_invalid_surrogates(form.content.data),
                category=form.category.data,
                image_url=remove_invalid_surrogates(form.image_url.data),
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

@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    html_content = markdown.markdown(post.content)
    form = CommentForm()
    if form.validate_on_submit() and current_user.is_authenticated:
        comment = Comment(
            post_id=post.id,
            author_id=current_user.id,
            content=remove_invalid_surrogates(form.content.data)
        )
        db.session.add(comment)
        db.session.commit()
        flash('Commentaire ajouté !', 'success')
        return redirect(url_for('post_detail', post_id=post.id))
    comments = Comment.query.filter_by(post_id=post.id).order_by(Comment.timestamp.asc()).all()
    comment_count = Comment.query.filter_by(post_id=post.id).count()
    return render_template('post_detail.html', post=post, html_content=html_content, form=form, comments=comments, comment_count=comment_count)

@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_post(post_id):
    """Edit an existing blog post"""
    post = Post.query.get_or_404(post_id)
    form = PostForm(obj=post)
    
    if form.validate_on_submit():
        try:
            post.title = form.title.data
            post.content = form.content.data
            post.category = form.category.data
            post.image_url = form.image_url.data
            db.session.commit()
            flash('Ton article a été modifié avec succès! ✨', 'success')
            return redirect(url_for('post_detail', post_id=post.id, from_edit=1))
        except Exception as e:
            db.session.rollback()
            flash('Oups! Une erreur s\'est produite. Essaie encore! 😊', 'error')
            logging.error(f"Error editing post: {e}")
    
    return render_template('edit_post.html', form=form, post=post, editing=True)

@app.route('/delete/<int:post_id>', methods=['POST'])
@login_required
@admin_required
def delete_post(post_id):
    """Delete a blog post"""
    post = Post.query.get_or_404(post_id)
    
    try:
        db.session.delete(post)
        db.session.commit()
        flash('Ton article a été supprimé! 🗑️', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Oups! Impossible de supprimer l\'article. 😔', 'error')
        logging.error(f"Error deleting post: {e}")
    
    return redirect(url_for('index'))

@app.route('/like/<int:post_id>', methods=['POST'])
def like_post(post_id):
    """Incrémente le nombre de likes pour un article"""
    post = Post.query.get_or_404(post_id)
    try:
        post.likes += 1
        db.session.commit()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': True, 'likes': post.likes})
        flash('Merci pour ton like ! ❤️', 'success')
    except Exception as e:
        db.session.rollback()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'error': str(e)}), 500
        flash("Oups ! Impossible d'ajouter un like.", 'error')
    return redirect(request.referrer or url_for('post_detail', post_id=post_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Bienvenue, {user.username} ! 🌈', 'success')
            return redirect(url_for('index'))
        else:
            flash('Nom d\'utilisateur ou mot de passe incorrect.', 'error')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('À bientôt ! Tu es bien déconnecté(e).', 'success')
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Ce nom d\'utilisateur existe déjà.', 'error')
        elif User.query.filter_by(email=form.email.data).first():
            flash('Cet email est déjà utilisé.', 'error')
        else:
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Inscription réussie ! Connecte-toi maintenant.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/board', methods=['GET', 'POST'])
@login_required
def board():
    # Suppression de la restriction pour les admins
    form = MessageBoardForm()
    if form.validate_on_submit():
        msg = MessageBoard(author_id=current_user.id, content=remove_invalid_surrogates(form.content.data))
        db.session.add(msg)
        db.session.commit()
        flash('Message envoyé !', 'success')
        return redirect(url_for('board'))
    messages = MessageBoard.query.order_by(MessageBoard.timestamp.desc()).all()
    return render_template('board.html', form=form, messages=messages)

@app.route('/admin/board', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_board():
    messages = MessageBoard.query.order_by(MessageBoard.timestamp.desc()).all()
    reply_forms = {msg.id: AdminReplyForm() for msg in messages}
    return render_template('admin_board.html', messages=messages, reply_forms=reply_forms)

@app.route('/admin/message/<int:msg_id>/reply', methods=['POST'])
@login_required
@admin_required
def admin_reply(msg_id):
    msg = MessageBoard.query.get_or_404(msg_id)
    form = AdminReplyForm()
    if form.validate_on_submit():
        msg.admin_reply = form.reply.data
        msg.admin_info = form.info.data
        msg.admin_user = current_user.username
        db.session.commit()
        flash('Réponse envoyée !', 'success')
    else:
        flash('Erreur dans le formulaire de réponse.', 'error')
    return redirect(url_for('admin_board'))

@app.route('/admin/message/<int:msg_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_message(msg_id):
    msg = MessageBoard.query.get_or_404(msg_id)
    db.session.delete(msg)
    db.session.commit()
    flash('Message supprimé.', 'success')
    return redirect(url_for('admin_board'))

@app.route('/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    post_id = comment.post_id
    db.session.delete(comment)
    db.session.commit()
    flash('Commentaire supprimé.', 'success')
    return redirect(url_for('post_detail', post_id=post_id))

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        # Ici, on simule l'envoi d'un email
        flash('Si cet email existe, un lien de réinitialisation a été envoyé.', 'success')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
