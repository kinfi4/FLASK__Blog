import os
import secrets
from PIL import Image

from app import app


def save_pic(filename):
    file_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(filename)
    picture_fn = file_hex + file_ext
    picture_path = os.path.join(app.root_path, 'static/media/users_avatars', picture_fn)

    return picture_path, picture_fn


def save_form_pic(form_pic):
    out_size = (255, 255)
    img = Image.open(form_pic)
    img.thumbnail(out_size)

    picture_path, new_filename = save_pic(form_pic.filename)
    form_pic.save(picture_path)

    img.save(picture_path)
    return new_filename
