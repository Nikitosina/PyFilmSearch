from flask import jsonify, redirect
from flask_restful import reqparse, abort, Api, Resource


def abort_if_users_not_found(id):
    if not USERS.get(id):
        abort(404, message="Users {} not found".format(id))


class Users(Resource):
    def get(self, id):
        abort_if_users_not_found(id)
        return jsonify({'users:': USERS.get(id)})

    def delete(self, id):
        abort_if_users_not_found(id)
        NEWS.delete(id)
        return jsonify({'success': 'OK'})

    def put(self, id):
        abort_if_news_not_found(id)
        args = users_parser.parse_args()
        USERS.replace(id, args['username'], args['password'])
        return jsonify({'success': 'OK'})
