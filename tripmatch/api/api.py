from flask import jsonify, make_response, render_template, json, Blueprint, g
from flask_restful import Resource, Api
from sqlalchemy.orm import subqueryload

from ..db.tripmatch_model import TripDetails, Destinations, Users
from ..utils import login_required

api = Blueprint('api', __name__)


class UserAPI(Resource):
    @login_required
    def get(self, user_id):
        user = g.db_session.query(Users).filter_by(id=user_id).one()
        return jsonify(user.to_dict())

    @login_required
    def delete(self, user_id):
        user = g.db_session.query(Users).filter_by(id=user_id).one()
        if not user:
            g.db_session.delete(user)


class TripAPI(Resource):
    def get(self, trip_id):
        trip = g.db_session.query(TripDetails).options(subqueryload(TripDetails.destinations)).filter_by(id=trip_id).one()
        return jsonify(trip.to_dict_ex())

    @login_required
    def delete(self, trip_id):
        trip = g.db_session.query(TripDetails).filter_by(id=trip_id).one()
        if not trip:
            g.db_session.delete(trip)


class TripsByDateAPI(Resource):
    def get(self, offset=0, limit=12):
        trips = g.db_session.query(TripDetails).order_by(TripDetails.date_start.desc()).all()
        resp = make_response(render_template('timeline_standalone.html', trips=trips), 200,
                             {'Content-Type': 'text/html'})
        return resp


class TripsByPostAPI(Resource):
    def get(self, offset=0, limit=12):
        trips = g.db_session.query(TripDetails).order_by(TripDetails.date_create.desc()).all()
        return make_response(render_template('timeline_standalone.html', trips=trips), 200,
                             {'Content-Type': 'text/html'})


class DestinationAPI(Resource):
    @login_required
    def get(self, destination_id) -> json:
        destination = g.db_session.query(Destinations).filter_by(id=destination_id).one()
        return jsonify(destination.to_dict())

    def delete(self, destination_id):
        destination = g.db_session.query(Destinations).filter_by(id=destination_id).one()
        if not destination:
            g.db_session.delete(destination)


flask_api = Api(api)
flask_api.add_resource(UserAPI, '/user_api/<int:user_id>')
flask_api.add_resource(TripAPI, '/trip_api/<int:trip_id>')
flask_api.add_resource(TripsByDateAPI, '/trips_api/order_by_trip_date')
flask_api.add_resource(TripsByPostAPI, '/trips_api/order_by_post_date')
flask_api.add_resource(DestinationAPI, '/destination_api/<int:destination_id>')
