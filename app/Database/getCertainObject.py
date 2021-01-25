def get_object_from_db(cls, id_):
    return cls.query.get(id_)
