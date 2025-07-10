from app import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship

class Post(db.Model):
    """Blog post model"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    likes = db.Column(db.Integer, default=0)  # Nouveau champ pour compter les likes
    
    def __repr__(self):
        return f'<Post {self.title}>'
    
    @property
    def category_emoji(self):
        """Return emoji for each category"""
        emoji_map = {
            'voyage': '\u2708\ufe0f',
            'cuisine': '\ud83c\udf73',
            'art': '\ud83c\udfa8',
            'scolarité': '\ud83d\udcda',
            'musique': '\ud83c\udfb5',
            'autres': '\ud83c\udf1f'
        }
        return emoji_map.get(self.category, '\ud83c\udf1f')
    
    @property
    def formatted_date(self):
        """Return formatted date in French"""
        return self.created_at.strftime('%d %B %Y à %H:%M')

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class MessageBoard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed = db.Column(db.Boolean, default=False)
    is_offensive = db.Column(db.Boolean, default=False)
    author = relationship('User', backref='messages')

    def __repr__(self):
        return f'<MessageBoard {self.id}>'
