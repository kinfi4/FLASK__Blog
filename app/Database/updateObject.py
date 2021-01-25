from app import db


def update_object(cls, id_, **kwargs):
    obj = cls.query.get(id_)
    for attr, value in kwargs.items():
        setattr(obj, attr, value)

    db.session.commit()
    return obj
