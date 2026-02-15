#!/bin/bash

# Arrêter les instances précédentes
pkill -f gunicorn

# Installer les dépendances
pip3 install -r requirements.txt

# Initialiser les données si nécessaire
python3 seed_admin.py
python3 seed_data.py
python3 seed_notes.py

# Lancer avec Gunicorn en arrière-plan
# --bind 0.0.0.0:5000 : Écouter sur toutes les interfaces
# --workers 4 : Nombre de processus travailleurs pour gérer la charge
# --daemon : Lancer en arrière-plan
gunicorn --bind 0.0.0.0:5000 --workers 4 --daemon wsgi:app

echo "L'application EduManager est maintenant en ligne en mode production !"
