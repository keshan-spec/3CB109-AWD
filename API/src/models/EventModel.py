from sqlalchemy.orm import relationship
from marshmallow import fields, Schema
from . import db
import datetime


class EventModel(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    start = db.Column(db.DateTime)
    finish = db.Column(db.DateTime)
    repeat = db.Column(db.String(255), default="Never")
    work_id = db.Column(db.Integer, db.ForeignKey("work_place_model.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user_model.id"))

    # Relationships
    user = relationship("UserModel")
    workplaces = relationship("WorkPlaceModel")

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


class EventSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    description = fields.String()
    start = fields.DateTime()
    finish = fields.DateTime()
    repeat = fields.String()
    work_id = fields.Integer()
    user_id = fields.Integer()
