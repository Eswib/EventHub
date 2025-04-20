from extensions import db
from flask_login import UserMixin

class Bruker(db.Model, UserMixin):
    __tablename__ = 'bruker'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    epost = db.Column(db.String(45), unique=True, nullable=False)
    passord = db.Column(db.String(200), nullable=False)
    navn = db.Column(db.String(45), nullable=False)

    # Relationship to Arrangementer (one-to-many)
    arrangementer = db.relationship('Arrangement', backref='bruker', lazy=True)

    # Relationship to Påmeldinger (one-to-many)
    påmeldinger = db.relationship('Påmelding', backref='bruker', lazy=True)

    def __repr__(self):
        return f"<bruker id={self.id}, navn='{self.navn}', epost='{self.epost}'>"

class Arrangement(db.Model):
    __tablename__ = 'arrangement'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bruker_id = db.Column(db.Integer, db.ForeignKey('bruker.id'), nullable=False)
    navn = db.Column(db.String(45), nullable=False)
    beskrivelse = db.Column(db.String(200), nullable=False)
    dato = db.Column(db.DateTime, nullable=False)
    sted = db.Column(db.String(100), nullable=False)
    bilde = db.Column(db.String(200), nullable=True)

    # Relationship to Påmeldinger (one-to-many)
    påmeldinger = db.relationship('Påmelding', backref='arrangement', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<arrangement id={self.id}, navn='{self.navn}', dato='{self.dato}'>"

class Påmelding(db.Model):
    __tablename__ = 'påmelding'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bruker_id = db.Column(db.Integer, db.ForeignKey('bruker.id'), nullable=False)
    arrangement_id = db.Column(db.Integer, db.ForeignKey('arrangement.id', ondelete='CASCADE'), nullable=False)
    
    # Prevent duplicate sign-up (Also checked in join_event)
    __table_args__ = (db.UniqueConstraint('bruker_id', 'arrangement_id', name='unique_registration'),)