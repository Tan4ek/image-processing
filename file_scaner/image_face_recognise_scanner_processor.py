import logging
import os
import time
import uuid

from kafka import KafkaProducer

from file_scaner.abstract_process import AbstractProcess
from file_scaner.db_service import DbImageService
from util.util import kafka_json_serializer, get_hostname

__DELAY_BETWEEN_CROP_FACE_SCANNING__ = 5 * 60


class CropFaceRecogniseScannerProcessor(AbstractProcess):

    def __init__(self, db_uri, db_image_name, kafka_host, kafka_face_recognise_topic):
        super().__init__('CropFaceRecogniseScannerProcessor')
        self.kafka_host = kafka_host
        self.db_uri = db_uri
        self.db_image_name = db_image_name
        self.kafka_face_recognise_topic = kafka_face_recognise_topic

    def _run(self):
        producer = KafkaProducer(bootstrap_servers=self.kafka_host, value_serializer=kafka_json_serializer)

        db_image_service = DbImageService(db_uri=self.db_uri, db_image_name=self.db_image_name)

        while True:
            try:
                self.scan_crop_face_image(db_image_service, producer)
                logging.info('Crop face scanner: sleeping for %s seconds', __DELAY_BETWEEN_CROP_FACE_SCANNING__)
                time.sleep(__DELAY_BETWEEN_CROP_FACE_SCANNING__)
            except Exception as e:
                logging.error(e)

    def scan_crop_face_image(self, db_image_service, producer):
        crop_face_not_in_queue = db_image_service.find_crop_face_not_in_queue()
        for crop_face_document in crop_face_not_in_queue:
            kafka_recognise_face_task_message = {
                'message_id': str(uuid.uuid4()),
                'host': get_hostname(),
                'payload': {
                    'path': crop_face_document['crop_face_image_path'],
                    'file': os.path.split(crop_face_document['crop_face_image_path'])[1],
                    'db_id': str(crop_face_document['_id'])
                }
            }
            future_send = producer.send(self.kafka_face_recognise_topic, kafka_recognise_face_task_message)
            future_send.get(2 * 60)
            logging.info('Save ')

            db_image_service.update_crop_face_in_queue(str(crop_face_document['_id']), in_queue=True)
