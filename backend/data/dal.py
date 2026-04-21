from pymongo import MongoClient
from bson import ObjectId
from bson.errors import InvalidId
import os

class ItemDAL:
    def __init__(self):
        mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017")
        self.client = MongoClient(mongo_url)
        self.db = self.client["item_manager"]
        self.collection = self.db["items"]

    def _serialize_item(self, item: dict | None) -> dict | None:
        if item is None:
            return None

        item["id"] = str(item["_id"])
        del item["_id"]
        return item

    def _to_object_id(self, item_id: str) -> ObjectId | None:
        try:
            return ObjectId(item_id)
        except InvalidId:
            return None

    def create_item(self, item_data: dict) -> dict:
        result = self.collection.insert_one(item_data)
        return self._serialize_item(self.collection.find_one({"_id": result.inserted_id}))
    
    def get_item(self, item_id: str) -> dict | None:
        object_id = self._to_object_id(item_id)
        if object_id is None:
            return None

        return self._serialize_item(self.collection.find_one({"_id": object_id}))
    
    def get_all_items(self) -> list[dict]:
        return [self._serialize_item(item) for item in self.collection.find()]
    
    def update_item(self, item_id: str, item_data: dict) -> dict | None:
        object_id = self._to_object_id(item_id)
        if object_id is None:
            return None

        self.collection.update_one({"_id": object_id}, {"$set": item_data})
        return self._serialize_item(self.collection.find_one({"_id": object_id}))

    def delete_item(self, item_id: str) -> dict | None:
        object_id = self._to_object_id(item_id)
        if object_id is None:
            return None

        return self._serialize_item(self.collection.find_one_and_delete({"_id": object_id}))
