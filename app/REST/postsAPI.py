from datetime import datetime

from flask import jsonify
from flask_restful import Resource, request, marshal_with
from app.Database.postsControll import get_all_posts
from app.Database.addObject import add_object_to_bd

from app.REST.constants import request_post_parser, resource_post_fields
from app import api
from app.models import Post


class PostApi(Resource):
    def get(self):
        posts, has_prev, has_next, prev_num, next_num = get_all_posts(request.args)
        return jsonify({
            'posts': [post.serialize() for post in posts],
            'pagination': {
                'has_prev': has_prev,
                'has_next': has_next,
                'prev_num': prev_num,
                'next_num': next_num
            }
        })

    @marshal_with(resource_post_fields)
    def post(self):
        args = request_post_parser.parse_args()
        args.update({
            'timespan': datetime.utcnow()
        })

        post = add_object_to_bd(Post, **args)

        return post


api.add_resource(PostApi, '/json_posts')



