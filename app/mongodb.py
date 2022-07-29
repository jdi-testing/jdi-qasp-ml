import pymongo

client = pymongo.MongoClient("host.docker.internal", 27017)
mongo_db = client.jdn


def get_session_id():
    session_id_entry = mongo_db.sesion_id_collection.find_one()
    if session_id_entry:
        result = session_id_entry["session_id"]
        mongo_db.sesion_id_collection.update_one(
            {}, {"$set": {"session_id": result + 1}}
        )
        return result
    else:
        mongo_db.sesion_id_collection.insert_one({"session_id": 1})
        return 1
