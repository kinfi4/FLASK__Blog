from app import db


def delete_object(cls, id_):
    obj = cls.query.get(id_)

    if not obj:
        return None

    db.session.delete(obj)
    db.session.commit()

    return obj
