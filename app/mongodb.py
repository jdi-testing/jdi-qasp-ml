import json

import motor.motor_asyncio
import pymongo
from bson.json_util import dumps

client = pymongo.MongoClient("mongodb", 27017)
mongo_db = client.jdn

async_client = motor.motor_asyncio.AsyncIOMotorClient("mongodb", 27017)
async_mongo_db = async_client.jdn


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


def create_logs_json_file():
    logs_collection = mongo_db.logs
    all_logs = logs_collection.find()

    with open("logs.json", "w") as output_file:
        json.dump(json.loads(dumps(all_logs)), output_file)


def create_initial_log_entry(logging_info):
    logs_collection = mongo_db.logs
    logs_collection.insert_one(logging_info.dict())


async def enrich_logs_with_generated_locators(
    session_id, website_url, full_xpath, nesting_num, result, start_time, task_duration
):
    logs_collection = async_mongo_db.logs
    await logs_collection.update_one(
        {"session_id": session_id, "website_url": website_url},
        {
            "$push": {
                "locator_list": {
                    "jdn-hash": result["id"],
                    "full_xpath": full_xpath,
                    "nesting_num": nesting_num,
                    "generated_locator": result["result"],
                    "start_time": start_time,
                    "task_duration": task_duration,
                }
            }
        },
    )
