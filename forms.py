from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, URLField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, URL, Email, EqualTo
import markdown

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

class LoginForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    remember = BooleanField('Se souvenir de moi')
    submit = SubmitField('Connexion')

class RegisterForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Confirme ton mot de passe', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Inscription')

class MessageBoardForm(FlaskForm):
    content = TextAreaField('Ton message', validators=[DataRequired(), Length(min=2, max=500)], render_kw={'placeholder': 'Écris ton message ici...', 'rows': 4})
    submit = SubmitField('Envoyer')

class CommentForm(FlaskForm):
    content = TextAreaField('Ton commentaire', validators=[DataRequired(), Length(min=2, max=500)], render_kw={'placeholder': 'Écris ton commentaire ici...', 'rows': 3})
    submit = SubmitField('Commenter')

class ResetPasswordForm(FlaskForm):
    email = StringField('Ton email', validators=[DataRequired(), Email()])
    submit = SubmitField('Envoyer le lien de réinitialisation')

class AdminReplyForm(FlaskForm):
    reply = TextAreaField('Réponse de l’admin', render_kw={'rows': 2, 'placeholder': 'Répondre à ce message…'})
    info = TextAreaField('Information (optionnel)', render_kw={'rows': 1, 'placeholder': 'Ajouter une information visible sur le mur...'})
    submit = SubmitField('Envoyer la réponse')
