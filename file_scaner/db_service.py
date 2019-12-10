import logging

from bson.objectid import ObjectId
from pymongo import MongoClient


class DbImageService:

    def __init__(self, db_uri, db_image_name):
        self._mongo_client = MongoClient(db_uri)

        self._db = self._mongo_client[db_image_name]
        self._image_collection = self._db['images']
        self._crop_face_image_collection = self._db['crop_face_image']

    def insert_image(self, image_document):
        insert_result = self._image_collection.insert_one(image_document)
        return insert_result.inserted_id

    def insert_crop_face_image(self, crop_face_image_document):
        insert_result = self._crop_face_image_collection.insert_one(crop_face_image_document)
        return insert_result.inserted_id

    def remove_image(self, _id_str):
        result = self._image_collection.delete_one({'_id': ObjectId(_id_str)})
        return True if result.deleted_count > 0 else False

    def find_image_by_path_simple_hash(self, path, simple_hash):
        return self._image_collection.find_one({'path': path, 'simple_hash': simple_hash})

    def find_crop_face_not_in_queue(self, limit=50):
        return self._crop_face_image_collection.find({'face_recognised_in_queue': False,
                                                      'face_recognised': False}, limit=limit)

    def update_crop_face_in_queue(self, _id_str, in_queue=True):
        self._crop_face_image_collection.update_one({'_id': ObjectId(_id_str)},
                                                    {"$set": {
                                                        'face_recognised_in_queue': in_queue
                                                    }}, upsert=False)

    def update_crop_face_recognise(self, _id_str, recognised):
        self._crop_face_image_collection.update_one({'_id': ObjectId(_id_str)},
                                                    {
                                                        "$set": {
                                                            'face_recognised_in_queue': False,
                                                            'face_recognised': True,
                                                            'recognised': recognised
                                                        }
                                                    }, upsert=False)

    def update_image_faces_process_step(self, _id_str, path, recognised, crop_timestamp):
        query = {'_id': ObjectId(_id_str),
                 'path': path}

        logging.info("Update image with '_id' %s. Process step: FACE_DETECTION", _id_str)
        self._image_collection.update_one(query,
                                          {"$set": {
                                              "recognised": recognised
                                          },
                                              "$push": {
                                                  "process_steps": {
                                                      'name': 'FACE_DETECTION',
                                                      'timestamp': crop_timestamp
                                                  }
                                              }}, upsert=False)

    def find_image_by_id_path(self, _id_str, path):
        query = {'_id': ObjectId(_id_str),
                 'path': path}
        return self._image_collection.find_one(query)

    def find_crop_face_by_id(self, _id_str):
        return self._crop_face_image_collection.find_one({'_id': ObjectId(_id_str)})
