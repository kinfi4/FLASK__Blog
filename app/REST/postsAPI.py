from flask import jsonify
from flask_restful import Resource, request
from app.Database.postsControll import get_all_posts
from app import api


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


api.add_resource(PostApi, '/json_posts')



