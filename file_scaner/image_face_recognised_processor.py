import logging
from multiprocessing import Process

from bson.objectid import ObjectId
from kafka import KafkaConsumer, TopicPartition, OffsetAndMetadata

from file_scaner.db_service import DbImageService
from util.util import kafka_json_deserializer


class CropFaceRecognisedProcessor(Process):

    def __init__(self, db_uri, db_image_name, kafka_host, kafka_face_recognise_result_topic):
        super().__init__()
        self.kafka_face_recognise_result_topic = kafka_face_recognise_result_topic
        self.db_uri = db_uri
        self.db_image_name = db_image_name
        self.kafka_host = kafka_host
        logging.info('Initialise %s process completed', self.__class__.__name__)

    def run(self):
        consumer = KafkaConsumer(self.kafka_face_recognise_result_topic,
                                 bootstrap_servers=[self.kafka_host], auto_offset_reset='earliest',
                                 enable_auto_commit=False, group_id='recognised_faces',
                                 value_deserializer=kafka_json_deserializer, max_poll_records=20)
        db_image_service = DbImageService(self.db_uri, self.db_image_name)
        for msg in consumer:
            message_v = msg.value
            message_payload = message_v['payload']

            crop_face_image_id = message_payload['db_id']
            crop_face_image_document = db_image_service.find_crop_face_by_id(crop_face_image_id)

            if crop_face_image_document:
                recognised_faces = crop_face_image_document['recognised_faces']
                db_image_service.update_crop_face_recognise(crop_face_image_id, recognised_faces)
            else:
                logging.warning("Can't find crop face image by %s", str({'_id': ObjectId(message_payload['db_id'])}))

            topic_partition = TopicPartition(self.kafka_face_recognise_result_topic, msg.partition)
            offset = OffsetAndMetadata(msg.offset, '')
            consumer.commit(offsets={topic_partition: offset})
            logging.info("after commit %s", message_v['consumer_id'])
