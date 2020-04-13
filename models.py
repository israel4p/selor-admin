from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Users(db.Model):
    now = datetime.now()
    hora = ('%02d:%02d:%02d' % (now.hour, now.minute, now.second))
    data = ('%d-%02d-%02d' % (now.year, now.month, now.day))

    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))
    uid = db.Column(db.Integer)
    gid = db.Column(db.Integer)
    home = db.Column(db.String(255))
    maildir = db.Column(db.String(255))
    date_add = db.Column(db.DateTime, default=data)
    time_add = db.Column(db.DateTime, default=hora)
    domain = db.Column(db.String(128))
    name = db.Column(db.String(150))
    ok = db.Column(db.Integer, default=1)
    quota = db.Column(db.String(20))
    dlocal = db.Column(db.String(255))


class Domain(db.Model):
    name = db.Column(db.String(128), primary_key=True, unique=True)
    company = db.Column(db.String(255))


class Administrator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(15), unique=True)
    password = db.Column(db.String(128))

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymour(self):
        return True

    def get_id(self):
        return self.id
