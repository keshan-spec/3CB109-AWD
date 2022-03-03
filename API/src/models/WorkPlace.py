from sqlalchemy.orm import relationship
from marshmallow import fields, Schema
from . import db
from models.UserModel import UserModel


class WorkPlaceModel(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255))
    joined_on = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey("user_model.id"))

    # Relationships
    user = relationship("UserModel")

    def __repr__(self):
        return f"WorkPlace<id={self.id}, name={self.name}, user_id={self.user_id}>"

    @classmethod
    def get_all(cls):
        results = []
        for result in cls.query.all():
            _ = result.__dict__.pop("user_id")
            results.append(result.__dict__)

        return results

    def get_by_user(id):
        return WorkPlaceModel.query.join(UserModel, WorkPlaceModel.user_id == id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class WorkPlaceSchema(Schema):
    id = fields.Integer()
    user_id = fields.Integer()
    joined_on = fields.DateTime()
    name = fields.String()
    location = fields.String()
