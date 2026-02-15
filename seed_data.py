from app import create_app
from models import db, User, Filiere, Classe, Etudiant, Matiere

app = create_app()

with app.app_context():
    # 1. Création de la Filière
    filiere = Filiere.query.filter_by(niveau='L1').first()
    if not filiere:
        filiere = Filiere(nom='Informatique', niveau='L1', annee='2025-2026')
        db.session.add(filiere)
        db.session.commit()

    # 2. Création de la Classe
    classe = Classe.query.filter_by(nom='INFO-L1-A').first()
    if not classe:
        classe = Classe(nom='INFO-L1-A', filiere_id=filiere.id)
        db.session.add(classe)
        db.session.commit()

    # 3. Création d'un Enseignant
    prof = User.query.filter_by(username='prof1').first()
    if not prof:
        prof = User(username='prof1', nom='Dupont', prenom='Jean', role='enseignant')
        prof.set_password('prof123')
        db.session.add(prof)
        db.session.commit()

    # 4. Création d'un Étudiant
    user_etudiant = User.query.filter_by(username='etudiant1').first()
    if not user_etudiant:
        user_etudiant = User(username='etudiant1', nom='Sarr', prenom='Moussa', role='etudiant')
        user_etudiant.set_password('etudiant123')
        db.session.add(user_etudiant)
        db.session.commit()
        
        etudiant = Etudiant(matricule='ETU001', user_id=user_etudiant.id, classe_id=classe.id)
        db.session.add(etudiant)
        db.session.commit()

    print("Données de test initialisées avec succès !")
