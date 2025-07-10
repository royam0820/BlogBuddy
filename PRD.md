# Product Requirements Document (PRD) — MiniMonde

## 1. Vision
Créer un espace sécurisé, ludique et accessible où les enfants et leurs parents peuvent partager, lire et illustrer leurs histoires du quotidien.

## 2. Utilisateurs cibles
- Enfants (7-14 ans) souhaitant raconter leurs aventures
- Parents accompagnant ou modérant la publication

## 3. Parcours utilisateur principal
1. L'utilisateur arrive sur la page d'accueil et découvre les derniers articles publiés.
2. Il clique sur « Écrire mon histoire » pour accéder au formulaire de création.
3. Il remplit le formulaire (titre, catégorie, histoire, image optionnelle) et publie.
4. Son article apparaît sur la page d'accueil, visible par tous.
5. Il peut consulter, modifier ou supprimer ses propres articles.

## 4. Fonctionnalités clés
- **Accueil** : liste des articles, triés du plus récent au plus ancien, avec aperçu, catégorie (emoji), date, image.
- **Création d’article** : formulaire simple, validation, messages d’erreur clairs.
- **Édition/Suppression** : accessible depuis chaque article, confirmation avant suppression.
- **Catégories** : voyage, cuisine, art, scolarité, musique, autres (avec emoji).
- **Ajout d’image** : champ URL, image affichée si valide.
- **Interface responsive** : adaptée mobile/tablette/desktop.
- **Sécurité** : protection CSRF, validation des entrées, clé secrète session.

## 5. Exigences techniques
- Python 3.11+, Flask, SQLAlchemy, WTForms
- Base SQLite par défaut, support PostgreSQL
- Bootstrap 5, CSS personnalisé, Font Awesome
- Hébergement possible sur Replit, Heroku, etc.

## 6. Critères de succès
- Un enfant peut publier une histoire en moins de 2 minutes
- L’interface est compréhensible sans tutoriel
- Les erreurs sont explicites et non techniques
- L’application fonctionne sur mobile et desktop
- Les parents peuvent accompagner/modérer facilement

---

*MiniMonde — Le blog magique pour petits et grands !* 