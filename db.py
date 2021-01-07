from pymongo.errors import CollectionInvalid


def init_temperatures(mongo):
    try:
        mongo.db.create_collection('temperatures', capped=True, size=1073742000)
    except CollectionInvalid:
        pass
