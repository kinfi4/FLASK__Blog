from app import db


def add_object_to_bd(cls, **kwargs):
    obj = cls()
    for key, value in kwargs.items():
        setattr(obj, key, value)

    db.session.add(obj)
    db.session.commit()

    return obj