from app import app, db
from models import User

with app.app_context():
    db.create_all()
    username = "admin"
    email = "royam0820@gmail.com"
    password = "Parisfeb20!"
    if not User.query.filter_by(username=username).first():
        admin = User(username=username, email=email, is_admin=True)
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
        print("Admin créé avec succès !")
    else:
        print("Un utilisateur admin existe déjà.")