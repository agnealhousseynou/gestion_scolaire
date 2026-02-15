from app import create_app
from models import db, Etudiant, Matiere, Note

app = create_app()

with app.app_context():
    etudiant = Etudiant.query.filter_by(matricule='ETU001').first()
    matieres = Matiere.query.all()
    
    if etudiant and matieres:
        # Ajout de quelques notes pour l'étudiant
        notes_data = [
            ('Algorithme', 15.5),
            ('Base de données', 14.0),
            ('Framework web', 12.5),
            ('Anglais', 16.0),
            ('Droit', 9.0)
        ]
        
        for m_nom, val in notes_data:
            matiere = next((m for m in matieres if m.nom == m_nom), None)
            if matiere:
                # Vérifier si la note existe déjà
                existing = Note.query.filter_by(etudiant_id=etudiant.id, matiere_id=matiere.id).first()
                if not existing:
                    n = Note(etudiant_id=etudiant.id, matiere_id=matiere.id, valeur=val)
                    db.session.add(n)
        
        db.session.commit()
        print("Notes de test ajoutées avec succès !")
