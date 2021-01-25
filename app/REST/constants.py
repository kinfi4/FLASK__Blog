from flask_restful import reqparse, fields

request_post_parser = reqparse.RequestParser()
request_post_parser.add_argument('user_id', type=int)
request_post_parser.add_argument('body', type=str)

resource_post_fields = {
    'user_id': fields.Integer,
    'body': fields.String,
    'timespan': fields.DateTime,
}
