def object_exist(cls, id_):
    obj = cls.query.get(id_)
    return bool(obj)
