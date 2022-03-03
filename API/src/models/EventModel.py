from sqlalchemy.orm import relationship
from marshmallow import fields, Schema
from models.UserModel import UserModel
from . import db


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
    user = relationship("UserModel", backref="events")
    workplaces = relationship("WorkPlaceModel", backref="events")

    def __repr__(self):
        return f"Event<id={self.id}, name={self.name}, user_id={self.user_id}, work_id={self.work_id}>"

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def get_by_user(id):
        events = EventModel.query.join(UserModel, EventModel.user_id == id).all()
        _events = []

        for event in events:
            _events.append(
                {
                    "id": event.id,
                    "name": event.name,
                    "description": event.description,
                    "start": event.start,
                    "finish": event.finish,
                    "repeat": event.repeat,
                    "work": event.workplaces,
                }
            )

        return _events

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
