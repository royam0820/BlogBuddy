# MiniMonde

MiniMonde est une application de blog ludique et colorée, conçue pour permettre aux enfants et à leurs parents de partager leurs histoires et aventures. L'interface est conviviale, en français, et chaque article peut être catégorisé avec des emojis pour plus de fun !

## Fonctionnalités principales
- Création, édition et suppression d'articles de blog
- Catégorisation des articles (voyage, cuisine, art, scolarité, musique, autres) avec emoji
- Ajout d'une image à chaque article (via URL)
- Interface responsive et moderne (Bootstrap, CSS personnalisé)
- Validation des formulaires et messages d'erreur en français
- Confirmation avant suppression d'un article
- Affichage des articles du plus récent au plus ancien
- Navigation simple et intuitive

## Structure du projet
```
BlogBuddy/
  app.py           # Application Flask principale
  main.py          # Point d'entrée (lance l'app)
  models.py        # Modèle de données (Post)
  forms.py         # Formulaires WTForms
  instance/blog.db # Base de données SQLite
  static/          # Fichiers statiques (CSS, JS)
  templates/       # Templates HTML (Jinja2)
  pyproject.toml   # Dépendances Python
```

## Technologies utilisées
- Python 3.11+
- Flask
- Flask-SQLAlchemy
- Flask-WTF & WTForms
- Bootstrap 5
- Jinja2
- Font Awesome, Google Fonts

## Installation
1. **Cloner le dépôt**
```bash
git clone <url-du-repo>
cd BlogBuddy
```
2. **Créer un environnement virtuel**
```bash
python3 -m venv venv
source venv/bin/activate
```
3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```
Ou, si vous utilisez Poetry :
```bash
poetry install
```
4. **Lancer l'application**
```bash
python main.py
```
L'application sera accessible sur [http://localhost:5000](http://localhost:5000)

## Accès à la base de données SQLite
Les articles sont stockés dans le fichier `instance/blog.db` (base SQLite).

### Explorer la base de données
- **Avec un outil graphique** :
  - [DB Browser for SQLite](https://sqlitebrowser.org/) (Windows/Mac/Linux)
  - Ouvrez le fichier `instance/blog.db` pour visualiser, éditer ou exporter les données.
- **En ligne de commande** :
  ```bash
  sqlite3 instance/blog.db
  # Puis dans l'invite SQLite :
  .tables           # Voir les tables
  SELECT * FROM post;  # Voir tous les articles
  .exit             # Quitter SQLite
  ```

## Configuration
- Par défaut, la base SQLite est utilisée (`instance/blog.db`).
- Pour la production, configurez les variables d'environnement :
  - `SESSION_SECRET` : clé secrète Flask
  - `DATABASE_URL` : URL de la base de données (ex : PostgreSQL)

## Auteur
Créé par Juliette Nick Pay.

---

*MiniMonde est un projet éducatif et ludique pour découvrir le web en famille !* 