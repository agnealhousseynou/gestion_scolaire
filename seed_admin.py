from app import create_app
from models import db, User

app = create_app()

with app.app_context():
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', nom='Admin', prenom='System', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("Admin créé avec succès (admin / admin123)")
    else:
        print("Admin existe déjà")
