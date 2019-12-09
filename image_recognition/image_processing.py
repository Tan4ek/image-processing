import configparser
import logging
import os
from datetime import datetime

from PIL import Image

from image_recognition.recogniser import FaceRecogniser
from util.message_processing import AbstractMessageProcessing

config = configparser.ConfigParser()
config.read('config.ini')


class ImageRecogniseMessageProcessing(AbstractMessageProcessing):

    def __init__(self, crop_image=False, crop_face_location_path=''):
        self.recognisers = [FaceRecogniser(crop_face=crop_image, crop_face_location_path=crop_face_location_path)]

    def process_message(self, message_payload):
        file_path = message_payload['path']
        file_name = message_payload['file']
        logging.info(file_path)

        if os.path.exists(file_path):
            recognise_objects = []
            with Image.open(file_path) as image:
                for recogniser in self.recognisers:
                    recognised = recogniser.recognise(image, file_path)
                    recognise_objects.append(recognised)

            return {
                'original_path': file_path,
                'original_file': file_name,
                'a_hash': message_payload['a_hash'],
                'simple_hash': message_payload['simple_hash'],
                'db_id': message_payload['db_id'],
                'recognised_objects': recognise_objects,
                'timestamp': str(datetime.utcnow()),
            }
        else:
            logging.info("file doesn't exist {}".format(file_path))
            return None


