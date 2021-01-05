import os
import secrets

from app import app


def save_pic(filename):
    file_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(filename)
    picture_fn = file_hex + file_ext
    picture_path = os.path.join(app.root_path, 'static/media/users_avatars', picture_fn)

    return picture_path, picture_fn

