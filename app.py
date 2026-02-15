from flask import Flask
from config import Config
from models import db, User
from flask_login import LoginManager

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from routes import bp as main_bp
    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()
        # Initialisation des matières si elles n'existent pas
        from models import Matiere
        if not Matiere.query.first():
            matieres_data = [
                ('Algorithme', 2.0, 8),
                ('Base de données', 2.0, 8),
                ('Framework web', 2.0, 8),
                ('Gestion de projets', 1.5, 6),
                ('Anglais', 1.0, 4),
                ('Technique de communication', 1.0, 4),
                ('Droit', 1.0, 6),
                ('Réseau Telecom', 2.0, 8),
                ('Électronique', 2.0, 8)
            ]
            for nom, coef, cred in matieres_data:
                m = Matiere(nom=nom, coefficient=coef, credit=cred)
                db.session.add(m)
            db.session.commit()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
