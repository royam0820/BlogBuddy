from app import app
from models import db, Post, Comment, MessageBoard, User

def remove_invalid_unicode(text):
    if not isinstance(text, str):
        return text
    return ''.join(c for c in text if not (0xD800 <= ord(c) <= 0xDFFF))

with app.app_context():
    # Clean Posts
    for post in Post.query.all():
        changed = False
        for field in ['title', 'content', 'category', 'image_url']:
            value = getattr(post, field)
            cleaned = remove_invalid_unicode(value)
            if cleaned != value:
                setattr(post, field, cleaned)
                changed = True
        if changed:
            print(f"Cleaned Post {post.id}")

    # Clean MessageBoard
    for msg in MessageBoard.query.all():
        changed = False
        for field in ['content', 'admin_reply', 'admin_info', 'admin_user']:
            value = getattr(msg, field)
            cleaned = remove_invalid_unicode(value)
            if cleaned != value:
                setattr(msg, field, cleaned)
                changed = True
        if changed:
            print(f"Cleaned MessageBoard {msg.id}")

    # Clean Comments
    for comment in Comment.query.all():
        value = comment.content
        cleaned = remove_invalid_unicode(value)
        if cleaned != value:
            comment.content = cleaned
            print(f"Cleaned Comment {comment.id}")

    # Clean Users
    for user in User.query.all():
        changed = False
        for field in ['username', 'email']:
            value = getattr(user, field)
            cleaned = remove_invalid_unicode(value)
            if cleaned != value:
                setattr(user, field, cleaned)
                changed = True
        if changed:
            print(f"Cleaned User {user.id}")

    db.session.commit()
    print("Database cleaned of invalid Unicode surrogates.")

    # Verification scan for any remaining surrogates
    import re
    def has_surrogate(text):
        if not isinstance(text, str):
            return False
        return bool(re.search(r'[\ud800-\udfff]', text))

    found = False
    for post in Post.query.all():
        for field in ['title', 'content', 'category', 'image_url']:
            value = getattr(post, field)
            if has_surrogate(value):
                print(f"Surrogate in Post {post.id} field {field}: {repr(value)}")
                found = True
    for msg in MessageBoard.query.all():
        for field in ['content', 'admin_reply', 'admin_info', 'admin_user']:
            value = getattr(msg, field)
            if has_surrogate(value):
                print(f"Surrogate in MessageBoard {msg.id} field {field}: {repr(value)}")
                found = True
    for comment in Comment.query.all():
        if has_surrogate(comment.content):
            print(f"Surrogate in Comment {comment.id}: {repr(comment.content)}")
            found = True
    for user in User.query.all():
        for field in ['username', 'email']:
            value = getattr(user, field)
            if has_surrogate(value):
                print(f"Surrogate in User {user.id} field {field}: {repr(value)}")
                found = True
    if not found:
        print("Verification complete: No surrogate code points found in database.")
    else:
        print("WARNING: Some surrogate code points remain. See above for details.") 