# MiniMonde

MiniMonde est une application de blog ludique et colorée, conçue pour permettre aux enfants et à leurs parents de partager leurs histoires et aventures. L'interface est conviviale, en français, et chaque article peut être catégorisé avec des emojis pour plus de fun !

---

## 📚 Documentation détaillée

### Fonctionnalités principales
- Création, édition et suppression d'articles de blog (admin uniquement)
- Catégorisation des articles (voyage, cuisine, art, scolarité, musique, autres) avec emoji
- Ajout d'une image à chaque article (via URL)
- Système de likes sur chaque article (like possible depuis la page d'accueil et la page de détail, feedback immédiat sans rechargement)
- Système de commentaires sur chaque article (suppression par admin)
- Mur de communication (message board) pour tous les utilisateurs, avec modération et réponses admin
- Interface responsive et moderne (Bootstrap, CSS pastel personnalisé)
- Validation des formulaires et messages d'erreur en français
- Confirmation avant suppression d'un article ou d'un commentaire
- Affichage des articles du plus récent au plus ancien
- Navigation simple et intuitive
- Protection CSRF sur tous les formulaires
- Sécurité renforcée (seuls les admins peuvent modifier ou supprimer des contenus)

### Architecture technique
- **Backend** : Python 3.11+, Flask, Flask-SQLAlchemy, Flask-WTF, Flask-Login
- **Frontend** : Jinja2, Bootstrap 5, CSS personnalisé, Font Awesome, Google Fonts
- **Base de données** : SQLite (par défaut), support PostgreSQL via `DATABASE_URL`
- **Sécurité** : CSRF, gestion des sessions, validation des entrées, rôles utilisateur
- **Déploiement** : Gunicorn, configuration via variables d'environnement

### Structure de la base de données

#### Utilisateurs (`User`)
- `id` (int, PK)
- `username` (str, unique, requis)
- `email` (str, unique, requis)
- `password_hash` (str, requis)
- `is_admin` (bool, par défaut False)

#### Articles (`Post`)
- `id` (int, PK)
- `title` (str, requis)
- `content` (text, requis)
- `category` (str, requis, choix limités)
- `image_url` (str, optionnel)
- `created_at` (datetime, auto)
- `likes` (int, par défaut 0)

#### Commentaires (`Comment`)
- `id` (int, PK)
- `post_id` (int, FK vers Post)
- `author_id` (int, FK vers User)
- `content` (text, requis)
- `timestamp` (datetime, auto)

#### Mur de discussion (`MessageBoard`)
- `id` (int, PK)
- `author_id` (int, FK vers User)
- `content` (text, requis)
- `timestamp` (datetime, auto)
- `reviewed` (bool, par défaut False)
- `is_offensive` (bool, par défaut False)
- `admin_reply` (text, optionnel)
- `admin_info` (text, optionnel)
- `admin_user` (str, optionnel)

### Rôles et permissions
- **Administrateur** :
  - Peut créer, éditer, supprimer des articles
  - Peut supprimer n'importe quel commentaire
  - Peut répondre et modérer le mur de discussion
  - Peut poster sur le mur de discussion
- **Utilisateur authentifié** :
  - Peut lire, liker et commenter les articles
  - Peut poster sur le mur de discussion
- **Visiteur non connecté** :
  - Peut lire les articles et les commentaires

---

## Structure du projet
```
BlogBuddy/
  app.py           # Application Flask principale (routes, logique)
  main.py          # Point d'entrée (lance l'app)
  models.py        # Modèles de données (Post, User, Comment, MessageBoard)
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

## Utilisation
- **Seuls les administrateurs** peuvent créer, éditer ou supprimer des articles.
- **Tous les utilisateurs** peuvent lire, liker et commenter les articles, et poster sur le mur de communication.
- **Like instantané** : cliquez sur le bouton "Like" (cœur) sur la page d'accueil ou la page d'un article. Le compteur s'incrémente sans rechargement.
- **Commentaires** : ajoutez un commentaire sous chaque article. Les admins peuvent supprimer les commentaires.
- **Mur de communication** : accessible à tous, avec modération et réponses admin.
- **Catégories** : chaque article peut être classé par thème, illustré par un emoji.

## Accès à la base de données SQLite
Les articles sont stockés dans le fichier `instance/blog.db` (base SQLite).

## Configuration
- Par défaut, la base SQLite est utilisée (`instance/blog.db`).
- Pour la production, configurez les variables d'environnement :
  - `SESSION_SECRET` : clé secrète Flask
  - `DATABASE_URL` : URL de la base de données (ex : PostgreSQL)

## Auteur
Créé par Juliette Nick Pay.

---

*MiniMonde est un projet éducatif et ludique pour découvrir le web en famille !* 

---

### 1. **Database Rollback (Undo Last Change in Code)**
If you want to undo the last database schema change (for example, removing the `likes` column you just added):

- **With SQLite,** there is no built-in migration/rollback unless you use a tool like Flask-Migrate/Alembic.
- If you want to remove the `likes` column, you must:
  1. Edit `models.py` to remove the `likes` field.
  2. Manually alter the database (using a tool like DB Browser for SQLite or SQL commands) to drop the column.
  3. Or, delete `instance/blog.db` to reset the database (you will lose all posts).

---

### 2. **Code Rollback (Undo File Changes)**
If you want to undo recent code changes:
- If you use git, you can run:
  ```bash
  git checkout -- <filename>
  ```
  or to reset all changes:
  ```bash
  git reset --hard
  ```
- If you want to revert to a previous commit:
  ```bash
  git log  # find the commit hash
  git checkout <commit-hash>
  ```