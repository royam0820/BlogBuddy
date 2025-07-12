from app import app, db
from models import Post

with app.app_context():
    Post.query.delete()
    db.session.commit()
    print("Tous les articles ont été supprimés.")