from flask import Blueprint, render_template, redirect, url_for, flash, request, send_file
from flask_login import login_required, current_user
from models import db, User, Etudiant, Classe, Matiere, Note, Absence, Filiere
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')

@bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        stats = {
            'etudiants': Etudiant.query.count(),
            'classes': Classe.query.count(),
            'matieres': Matiere.query.count()
        }
        return render_template('dashboard/admin.html', stats=stats)
    elif current_user.role == 'enseignant':
        return render_template('dashboard/enseignant.html')
    else:
        etudiant = Etudiant.query.filter_by(user_id=current_user.id).first()
        return render_template('dashboard/etudiant.html', etudiant=etudiant)

@bp.route('/etudiants')
@login_required
def list_etudiants():
    etudiants = Etudiant.query.all()
    return render_template('etudiants/index.html', etudiants=etudiants)

@bp.route('/classes')
@login_required
def list_classes():
    classes = Classe.query.all()
    return render_template('classes/index.html', classes=classes)

@bp.route('/matieres')
@login_required
def list_matieres():
    matieres = Matiere.query.all()
    return render_template('matieres/index.html', matieres=matieres)

@bp.route('/notes/saisie', methods=['GET', 'POST'])
@login_required
def saisie_notes():
    if current_user.role not in ['admin', 'enseignant']:
        flash('Accès refusé.')
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        etudiant_id = request.form.get('etudiant_id')
        matiere_id = request.form.get('matiere_id')
        valeur = float(request.form.get('note'))
        
        note = Note(etudiant_id=etudiant_id, matiere_id=matiere_id, valeur=valeur)
        db.session.add(note)
        db.session.commit()
        flash('Note enregistrée.')
        
    etudiants = Etudiant.query.all()
    matieres = Matiere.query.all()
    return render_template('notes/saisie.html', etudiants=etudiants, matieres=matieres)

@bp.route('/bulletin/<int:etudiant_id>')
@login_required
def bulletin(etudiant_id):
    etudiant = Etudiant.query.get_or_404(etudiant_id)
    if current_user.role == 'etudiant' and etudiant.user_id != current_user.id:
        flash('Accès refusé.')
        return redirect(url_for('main.dashboard'))
    
    notes = Note.query.filter_by(etudiant_id=etudiant_id).all()
    
    # Calcul des moyennes
    moyennes_matiere = {}
    total_points = 0
    total_coefs = 0
    total_credits_obtenus = 0
    
    for m in Matiere.query.all():
        m_notes = [n.valeur for n in notes if n.matiere_id == m.id]
        if m_notes:
            moy = sum(m_notes) / len(m_notes)
            moyennes_matiere[m.id] = moy
            total_points += moy * m.coefficient
            total_coefs += m.coefficient
            if moy >= 10:
                total_credits_obtenus += m.credit
                
    moyenne_generale = total_points / total_coefs if total_coefs > 0 else 0
    
    return render_template('bulletin/view.html', 
                           etudiant=etudiant, 
                           notes=notes, 
                           moyennes=moyennes_matiere,
                           moyenne_generale=moyenne_generale,
                           credits=total_credits_obtenus,
                           matieres=Matiere.query.all())
