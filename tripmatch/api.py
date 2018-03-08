from flask import jsonify, make_response, render_template, json
from flask import session as login_session
from flask_restful import Resource
from sqlalchemy.orm import subqueryload

from db import Session
from model.tripmatch_model import Users, TripDetails, Destinations


class UserAPI(Resource):
    def get(self, user_id):
        db_session = Session()
        user = db_session.query(Users).filter_by(id=user_id).one()
        return jsonify(user.to_dict())

    def delete(self, user_id):
        db_session = Session()
        user = db_session.query(Users).filter_by(id=user_id).one()
        if not user:
            db_session.delete(user)


class TripAPI(Resource):
    def get(self, trip_id):
        db_session = Session()
        trip = db_session.query(TripDetails).options(subqueryload(TripDetails.destinations)).filter_by(id=trip_id).one()
        return jsonify(trip.to_dict_ex())

    def delete(self, trip_id):
        db_session = Session()
        trip = db_session.query(TripDetails).filter_by(id=trip_id).one()
        if not trip:
            db_session.delete(trip)


class TripsByDateAPI(Resource):
    def get(self, offset=0, limit=12):
        db_session = Session()
        trips = db_session.query(TripDetails).order_by(TripDetails.date_start.desc()).all()
        resp = make_response(render_template('timeline_standalone.html', trips=trips), 200,
                             {'Content-Type': 'text/html'})
        return resp


class TripsByPostAPI(Resource):
    def get(self, offset=0, limit=12):
        db_session = Session()
        trips = db_session.query(TripDetails).order_by(TripDetails.date_create.desc()).all()
        return make_response(render_template('timeline_standalone.html', trips=trips), 200,
                             {'Content-Type': 'text/html'})


class DestinationAPI(Resource):
    def get(self, destination_id) -> json:
        db_session = Session()
        destination = db_session.query(Destinations).filter_by(id=destination_id).one()
        return jsonify(destination.to_dict())

    def delete(self, destination_id):
        db_session = Session()
        destination = db_session.query(Destinations).filter_by(id=destination_id).one()
        if not destination:
            db_session.delete(destination)
