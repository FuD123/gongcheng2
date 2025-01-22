from app import create_app
from app.models import User, db

app = create_app()
with app.app_context():
    db.session.query(User).filter(User.username == 'testuser').delete()
    db.session.commit()
    print("Test user deleted successfully")
