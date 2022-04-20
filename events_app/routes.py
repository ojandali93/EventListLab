"""Import packages and modules."""
import os
from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime
from events_app.models import Event, Guest

from events_app import app, db

main = Blueprint('main', __name__)

@main.route('/')
def index():
  events = Event.query.all()
  return render_template('index.html', events=events)


@main.route('/create', methods=['GET', 'POST'])
def create():
  if request.method == 'POST':
    new_event_title = request.form.get('title')
    new_event_description = request.form.get('description')
    date = request.form.get('date')
    time = request.form.get('time')
    try:
      date_and_time = datetime.strptime(
      f'{date} {time}',
      '%Y-%m-%d %H:%M')
    except ValueError:
      return render_template('create.html', 
        error='Incorrect datetime format! Please try again.')
    event = Event(title = new_event_title, description = new_event_description, date_and_time = date_and_time)
    db.session.add(event)
    db.session.commit()
    flash('Event created.')
    return redirect(url_for('main.index'))
  else:
    return render_template('create.html')


@main.route('/event/<event_id>', methods=['GET'])
def event_detail(event_id):
  event = Event.query.filter_by(id = event_id)
  return render_template('event_detail.html')


@main.route('/event/<event_id>', methods=['POST'])
def rsvp(event_id):
  event = Event.query.filter_by(id = event_id)
  is_returning_guest = request.form.get('returning')
  guest_name = request.form.get('guest_name')

  if is_returning_guest:
    guest = Guest.query.filter_BY(name = guest_name)
    if guest:
      return render_template('event_detail.htmls', error='Guest could not be located in our records')
    else:
      guest.events_attening.append(event)
      db.session.add(guest)
      db.session.commit()
  else:
    guest_email = request.form.get('email')
    guest_phone = request.form.get('phone')
    create_guest = Guest(name = guest_name, email = guest_email, phone = guest_phone)
    create_guest.events_attening.append(event)
    db.session.add(create_guest)
    db.session.commit()
  
  flash('You have successfully RSVP\'d! See you there!')
  return redirect(url_for('main.event_detail', event_id=event_id))


@main.route('/guest/<guest_id>')
def guest_detail(guest_id):
  giest = Guest.query.filter_by(id = guest_id)
  return render_template('guest_detail.html')
