from flask_jwt_extended import create_access_token
from flask_restful import Resource, reqparse
from rest_framework import status

post_parser = reqparse.RequestParser()
post_parser.add_argument('name', required=True)
post_parser.add_argument('key', required=True)


class Application(object):
    def __init__(self, id, name, key):
        self.id = id
        self.name = name
        self.key = key


class Auth(Resource):
    def __init__(self, **kwargs):
        apps = [Application(i, a['name'], a['key']) for i, a in enumerate(kwargs['apps'], start=1)]
        self.appsMap = {a.name: a for a in apps}

    def post(self):
        args = post_parser.parse_args()
        app = self.appsMap.get(args.name, None)

        if (app is None) or (app.key != args.key):
            return {}, status.HTTP_401_UNAUTHORIZED

        return {
            'access_token': create_access_token(identity=args.name, expires_delta=False)
        }
