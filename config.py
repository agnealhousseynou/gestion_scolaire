import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'une-cle-secrete-tres-difficile-a-deviner'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'student_mgmt.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
