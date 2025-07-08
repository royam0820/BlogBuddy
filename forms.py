from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, URLField
from wtforms.validators import DataRequired, Length, Optional, URL

class PostForm(FlaskForm):
    """Form for creating blog posts"""
    title = StringField(
        'Titre de ton article',
        validators=[
            DataRequired(message='N\'oublie pas le titre! 📝'),
            Length(min=3, max=200, message='Le titre doit faire entre 3 et 200 caractères')
        ],
        render_kw={'placeholder': 'Ex: Ma super aventure au parc!'}
    )
    
    content = TextAreaField(
        'Raconte ton histoire',
        validators=[
            DataRequired(message='Raconte-nous ton histoire! ✍️'),
            Length(min=10, message='Écris au moins 10 caractères')
        ],
        render_kw={
            'placeholder': 'Raconte-nous tout! Qu\'est-ce qui s\'est passé? Comment tu t\'es senti?',
            'rows': 8
        }
    )
    
    category = SelectField(
        'Catégorie',
        choices=[
            ('voyage', '✈️ Voyage'),
            ('cuisine', '🍳 Cuisine'),
            ('art', '🎨 Art'),
            ('scolarité', '📚 École'),
            ('musique', '🎵 Musique'),
            ('autres', '🌟 Autres')
        ],
        validators=[DataRequired(message='Choisis une catégorie! 🏷️')]
    )
    
    image_url = URLField(
        'Image (lien URL)',
        validators=[
            Optional(),
            URL(message='Assure-toi que c\'est un lien valide! 🔗')
        ],
        render_kw={'placeholder': 'https://exemple.com/mon-image.jpg (optionnel)'}
    )
