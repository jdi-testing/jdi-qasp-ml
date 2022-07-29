import pymongo

client = pymongo.MongoClient("mongodb", 27017)
mongo_db = client.jdn


def get_session_id():
    session_id_entry = mongo_db.sesion_id_collection.find_one()
    if session_id_entry:
        new_result = session_id_entry["session_id"] + 1
        mongo_db.sesion_id_collection.update_one(
            {}, {"$set": {"session_id": new_result}}
        )
        return new_result
    else:
        mongo_db.sesion_id_collection.insert_one({"session_id": 1})
        return 1
