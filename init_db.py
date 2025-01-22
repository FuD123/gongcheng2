from app import db
from app.models import User
from werkzeug.security import generate_password_hash

def init_database():
    # 手动创建所有表
    db.reflect()
    db.drop_all()
    db.create_all()
    
    # 添加默认管理员账号
    admin = User(
        username='admin',
        email='admin@example.com'
    )
    admin.set_password('admin123')
    db.session.add(admin)
    db.session.commit()

if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        init_database()
        print("Database initialized successfully!")
