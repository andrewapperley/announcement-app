from flask import Flask
import flask
import database
from database import Base
from flask import jsonify
from flask.ext.restful import Resource
from sqlalchemy import Column, String, DateTime, SmallInteger, ForeignKey, exc, Integer, not_, exists, BLOB, desc
from sqlalchemy.orm import *
from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper

app = Flask(__name__)


class Announcement_Creator(Base):
    __tablename__ = 'announcement_creators'
    announcement_creator_id = Column(Integer(), primary_key=True)
    announcement_creator = Column(Integer())
    announcement_creator_name = Column(String(255))

    def __init__(self, announcement_creator, announcement_creator_name):
        self.announcement_creator_id = None
        self.announcement_creator = announcement_creator
        self.announcement_creator_name = announcement_creator_name

class Announcement(Base):
    __tablename__ = 'announcement'
    announcement_id = Column(Integer(), primary_key=True)
    announcement_date = Column(Integer())
    announcement_title = Column(String(255))
    announcement_content = Column(String(255))
    announcement_location = Column(String(255))
    announcement_calendar_event = Column(SmallInteger())
    announcement_end_date = Column(Integer())
    announcement_creator = Column(Integer())

    def __init__(self, announcement_title, announcement_creator, announcement_date=None, announcement_content=None, announcement_location=None, announcement_calendar_event=None, announcement_end_date=None):
        self.user_id = None
        self.announcement_date = announcement_date
        self.announcement_title = announcement_title
        self.announcement_content = announcement_content
        self.announcement_location = announcement_location
        self.announcement_calendar_event = announcement_calendar_event
        self.announcement_end_date = announcement_end_date
        self.announcement_creator = announcement_creator

    def __repr__(self):
        return "<Announcement('%i', '%s', '%s', '%s', '%i', '%i')>" % (self.announcement_date, self.announcement_title, self.announcement_content, self.announcement_location, self.announcement_calendar_event, self.announcement_end_date)

# School

# Clubs

# Sports

database.createDatabase()


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

@app.route('/settings', methods=["GET"])
@crossdomain(origin='*')
def settings():

    session = database.DBSession()
    c = session.query(Announcement_Creator).all()

    _creators = []
    for _c in c:
        _creators.append({
            "name": _c.announcement_creator_name,
            "id": _c.announcement_creator
        })
    response = jsonify(creators=_creators)
    session.close()
    return response


@app.route('/announcements', methods=["GET"])
@crossdomain(origin='*')
def announcements():
    req = flask.request.args
    page_limit = 20
    page = int(req["page"])
    subscriptions = req["subscriptions"].split(",")
    session = database.DBSession()
    _subscriptions = []
    for s in subscriptions:
        _subscriptions.append(int(s))

    _announcements = session.query(Announcement).filter(Announcement.announcement_creator.in_(_subscriptions)).order_by(desc(Announcement.announcement_date)).limit(page_limit).offset((page - 1) * page_limit).all()

    _announcement_objects = []

    if len(_announcements) > 0:
        for announcement in _announcements:
            _announcement_objects.append(serialized_announcement(announcement))

    response = jsonify(announcements=_announcement_objects)
    session.close()
    return response


def serialized_announcement(announcement):
    return {
        "announcement_date": announcement.announcement_date,
        "announcement_title": announcement.announcement_title,
        "announcement_content": announcement.announcement_content,
        "announcement_location": announcement.announcement_location,
        "announcement_calendar_event": announcement.announcement_calendar_event,
        "announcement_end_date": announcement.announcement_end_date,
        "announcement_creator": announcement.announcement_creator
    }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
