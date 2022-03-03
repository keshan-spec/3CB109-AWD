from sqlalchemy.orm import relationship
from marshmallow import fields, Schema
from . import db


class WorkPlaceModel(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255))
    joined_on = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey("user_model.id"))

    # Relationships
    user = relationship("UserModel")

    def __repr__(self):
        return self.name

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class WorkPlaceSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    location = fields.String()
    joined_on = fields.DateTime()
    user_id = fields.Integer()
