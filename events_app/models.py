"""Create database models to represent tables."""
from events_app import db
from sqlalchemy.orm import backref

class Guest(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  email = db.Column(db.String)
  phone = db.Column(db.Integer)
  events_attending = db.relationship('Event', secondary='guest_event')

class Event(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String)
  description = db.Column(db.String)
  date_and_time = db.Column(db.DateTime)
  event_type = db.Column(db.Enum)
  guest = db.relationship('Guest', secondary='guest_event')

guest_event_table = db.Table('guest_event',
  db.Column('event_id', db.Integer, db.ForeignKey('event.id')),
  db.Column('guest_id', db.Integer, db.ForeignKey('guest.id'))
)