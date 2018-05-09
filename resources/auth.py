from flask_jwt_extended import create_access_token
from flask_restful import Resource, reqparse, http_status_message

post_parser = reqparse.RequestParser()
post_parser.add_argument('name')
post_parser.add_argument('key')


class Application(object):
    def __init__(self, id, name, key):
        self.id = id
        self.name = name
        self.key = key


# TODO: refactor this to be config managed or behind KeyCloack
apps = [
    Application(1, 'sportoffice', ';aslkjhf;adsljhy;oiubyhr')
]

appsMap = {a.name: a for a in apps}


class Auth(Resource):
    def post(self):
        args = post_parser.parse_args()
        app = appsMap.get(args.name, None)

        if (app.key != args.key):
            return http_status_message(401)

        return {
            'access_token': create_access_token(identity=args.name)
        }
