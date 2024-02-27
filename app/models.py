from app import db, ma
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(84), nullable=False)
    email = db.Column(db.String(84), nullable=False, unique=True, index=True)
    password = db.Column(db.String(255), nullable=False)

    def __str__(self):
        return self.name
    
    def toJSON(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'password': self.password,
        }


class Occurrences(db.Model):
    __tablename__ = "occurrences"
    id = db.Column(db.Integer, primary_key=True, index=True)
    create_date = db.Column(db.DateTime)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    tel = db.Column(db.String(200))
    tipomanifest = db.Column(db.String(200))
    valortipomanifest = db.Column(db.String(200))
    rua = db.Column(db.String(200))
    numero = db.Column(db.Integer)
    bairro = db.Column(db.String(200))
    cep = db.Column(db.Integer)
    lat = db.Column(db.Float)
    long = db.Column(db.Float)

    def __str__(self):
        return self.name

class OccurrencesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Occurrences