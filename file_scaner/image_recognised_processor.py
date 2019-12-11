import logging

from bson.objectid import ObjectId
from kafka import KafkaConsumer, TopicPartition, OffsetAndMetadata

from file_scaner.abstract_process import AbstractProcess
from file_scaner.db_service import DbImageService
from util.util import kafka_json_deserializer


class RecognisedProcessor(AbstractProcess):

    def __init__(self, db_uri, db_image_name, kafka_host, kafka_image_recognised_result_topic):
        super().__init__('RecognisedProcessor')
        self.kafka_image_recognised_result_topic = kafka_image_recognised_result_topic
        self.db_uri = db_uri
        self.db_image_name = db_image_name
        self.kafka_image_recognised_result_topic = kafka_image_recognised_result_topic
        self.kafka_host = kafka_host
        logging.info('Initialise %s process completed', self.__class__.__name__)

    def _run(self):
        consumer = KafkaConsumer(self.kafka_image_recognised_result_topic,
                                 bootstrap_servers=[self.kafka_host], auto_offset_reset='earliest',
                                 enable_auto_commit=False, group_id='recognised_faces',
                                 value_deserializer=kafka_json_deserializer, max_poll_records=20)
        db_image_service = DbImageService(self.db_uri, self.db_image_name)
        for msg in consumer:
            message_v = msg.value
            message_payload = message_v['payload']
            recognised_objects = message_payload['recognised_objects']
            logging.info('Receive message - consumer-id: %s', message_v['consumer_id'])
            image_document = db_image_service.find_image_by_id_path(message_payload['db_id'],
                                                                    message_payload['original_path'])
            if image_document:
                db_image_service.update_image_faces_process_step(message_payload['db_id'],
                                                                 message_payload['original_path'],
                                                                 recognised_objects,
                                                                 message_payload['timestamp'])

                cropped_faces = []
                for r in recognised_objects:
                    for c in r['cropped_faces']:
                        cropped_faces.append({
                            'image_id': image_document['_id'],
                            'crop_face_image_path': c['face_image_path'],
                            'crop_face_id': c['crop_face_id'],
                            'face_location': c['face_location'],
                            'face_recognised': False,
                            'face_recognised_in_queue': False,
                            'recognised': None
                        })

                for c in cropped_faces:
                    db_image_service.insert_crop_face_image(c)

            else:
                logging.warning("Can't find image by %s", str({'_id': ObjectId(message_payload['db_id']),
                                                               'path': message_payload['original_path']}))

            topic_partition = TopicPartition(self.kafka_image_recognised_result_topic, msg.partition)
            offset = OffsetAndMetadata(msg.offset, '')
            consumer.commit(offsets={topic_partition: offset})
            logging.info("after commit %s", message_v['consumer_id'])
