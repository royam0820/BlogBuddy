from app import db
from datetime import datetime

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
