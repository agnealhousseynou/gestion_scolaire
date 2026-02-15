from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    nom = db.Column(db.String(64), nullable=False)
    prenom = db.Column(db.String(64), nullable=False)
    role = db.Column(db.String(20), nullable=False) # 'admin', 'enseignant', 'etudiant'
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Filiere(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(64), nullable=False) # Licence
    niveau = db.Column(db.String(10), nullable=False) # L1, L2, L3
    annee = db.Column(db.String(20), nullable=False) # 2025-2026

class Classe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(64), nullable=False)
    filiere_id = db.Column(db.Integer, db.ForeignKey('filiere.id'))
    filiere = db.relationship('Filiere', backref='classes')

class Matiere(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    coefficient = db.Column(db.Float, default=1.0)
    credit = db.Column(db.Integer, default=0)

class Etudiant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    matricule = db.Column(db.String(20), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    classe_id = db.Column(db.Integer, db.ForeignKey('classe.id'))
    
    user = db.relationship('User', backref=db.backref('etudiant_profile', uselist=False))
    classe = db.relationship('Classe', backref='etudiants')

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    etudiant_id = db.Column(db.Integer, db.ForeignKey('etudiant.id'))
    matiere_id = db.Column(db.Integer, db.ForeignKey('matiere.id'))
    valeur = db.Column(db.Float, nullable=False)
    date_ajout = db.Column(db.DateTime, default=datetime.utcnow)
    
    etudiant = db.relationship('Etudiant', backref='notes')
    matiere = db.relationship('Matiere', backref='notes')

class Absence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    etudiant_id = db.Column(db.Integer, db.ForeignKey('etudiant.id'))
    date = db.Column(db.Date, default=datetime.utcnow().date())
    justifiee = db.Column(db.Boolean, default=False)
    
    etudiant = db.relationship('Etudiant', backref='absences')
