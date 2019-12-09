import configparser
import logging
import os
import uuid
from datetime import datetime

from PIL import Image
from kafka import KafkaConsumer, KafkaProducer
from kafka import OffsetAndMetadata
from kafka import TopicPartition

from image_recognition.recogniser import FaceRecogniser
from util.message_processing import AbstractMessageProcessing
from util.util import kafka_json_deserializer, kafka_json_serializer, get_hostname

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


class ImageProcessing(object):

    def __init__(self, kafka_host, kafka_image_recognise_topic, kafka_image_recognise_result_topic, cropped_faces_path):
        kafka_consumer_group = "face_recognise_{}".format(get_hostname())
        self.kafka_image_recognise_topic = kafka_image_recognise_topic
        self.kafka_image_recognise_result_topic = kafka_image_recognise_result_topic
        self.cropped_faces_path = cropped_faces_path
        self.consumer = KafkaConsumer(kafka_image_recognise_topic, bootstrap_servers=[kafka_host],
                                      auto_offset_reset='earliest',
                                      enable_auto_commit=False, group_id=kafka_consumer_group,
                                      value_deserializer=kafka_json_deserializer, max_poll_records=1,
                                      request_timeout_ms=400001,
                                      session_timeout_ms=400000,  # fix for:
                                      # Commit cannot be completed since the group has already rebalanced and
                                      # assigned the partitions to another member.
                                      max_poll_interval_ms=500000)

        self.consumer_id = "{}_{}".format(str(uuid.uuid4()), get_hostname())

        logging.info(str(self.consumer.metrics()))

        self.producer = KafkaProducer(bootstrap_servers=kafka_host, value_serializer=kafka_json_serializer,
                                      retries=5, reconnect_backoff_ms=10000)

        self.message_processing = ImageRecogniseMessageProcessing(crop_image=True,
                                                                  crop_face_location_path=cropped_faces_path)

    def start(self):
        for msg in self.consumer:
            logging.info(msg)
            value = msg.value
            topic_partition = TopicPartition(self.kafka_image_recognise_topic, msg.partition)
            offset = OffsetAndMetadata(msg.offset, '')

            message_id = value['message_id']
            message_payload = value['payload']

            try:
                process_image_result = self.message_processing.process_message(message_payload)

                if process_image_result is not None:

                    response_message = {
                        'payload': process_image_result,
                        'message_id': str(uuid.uuid4()),
                        'consumer_id': self.consumer_id,
                        'host': get_hostname()
                    }
                    self.consumer.commit(offsets={topic_partition: offset})

                    future_send = self.producer.send(config['kafka']['ImageRecogniseResultTopic'], response_message)
                    future_send.get(2 * 60)
                    logging.info('Save ')
                else:
                    logging.error("Can't process message '%s' on consumer '%s', skip it", message_id, self.consumer_id)
            except Exception as e:
                logging.error('Exception ', e)
