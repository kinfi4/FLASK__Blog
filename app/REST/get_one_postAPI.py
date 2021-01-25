from flask import abort

from flask_restful import Resource, marshal_with
from app import api
from app.REST.constants import resource_post_fields, request_post_parser
from app.Database.checkObjectExistence import object_exist
from app.Database.getCertainObject import get_object_from_db

from app.models import Post


class OnePostApi(Resource):
    @marshal_with(resource_post_fields)
    def get(self, id_):
        if not object_exist(Post, id_):
            abort(404)

        return get_object_from_db(Post, id_)


api.add_resource(OnePostApi, '/json_posts/<int:id_>')



