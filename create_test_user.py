from datetime import datetime, timedelta, UTC
from app import create_app
from app.models import User, db
from werkzeug.security import generate_password_hash

app = create_app()
with app.app_context():
    user = User(
        username='testuser',
        email='testuser@example.com',
        password_hash=generate_password_hash('testpassword'),
        role='user',
        password_expiry=datetime.now(UTC) + timedelta(days=30)
    )
    db.session.add(user)
    db.session.commit()
    print("Test user created successfully")
