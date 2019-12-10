import logging
import uuid
from datetime import datetime

from kafka import KafkaConsumer, KafkaProducer, TopicPartition, OffsetAndMetadata

from util.util import get_hostname, kafka_json_deserializer, kafka_json_serializer, current_milli_time


class ImageProcessing(object):

    def __init__(self, kafka_host, kafka_consumer_topic, kafka_response_topic, message_processing):
        kafka_consumer_group = "face_recognise_{}".format(get_hostname())
        self.kafka_consumer_topic = kafka_consumer_topic
        self.kafka_response_topic = kafka_response_topic
        self.consumer = KafkaConsumer(kafka_consumer_topic, bootstrap_servers=[kafka_host],
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

        self.message_processing = message_processing

    def start(self):
        for msg in self.consumer:
            logging.info(msg)
            value = msg.value
            topic_partition = TopicPartition(self.kafka_consumer_topic, msg.partition)
            offset = OffsetAndMetadata(msg.offset, '')

            message_id = value['message_id']
            message_payload = value['payload']

            try:
                start_execution_datetime = str(datetime.utcnow())
                time_before_face_location = current_milli_time()
                process_image_result = self.message_processing.process_message(message_payload)
                time_after_face_location = current_milli_time()

                if process_image_result is not None:

                    response_message = {
                        'payload': process_image_result,
                        'message_id': str(uuid.uuid4()),
                        'consumer_id': self.consumer_id,
                        'host': get_hostname(),
                        'execution_time_ms': time_after_face_location - time_before_face_location,
                        'start_execution_datetime': start_execution_datetime
                    }
                    self.consumer.commit(offsets={topic_partition: offset})

                    future_send = self.producer.send(self.kafka_response_topic, response_message)
                    future_send.get(2 * 60)
                    logging.info('Save ')
                else:
                    logging.error("Can't process message '%s' on consumer '%s', skip it", message_id, self.consumer_id)
            except Exception as e:
                logging.error('Exception ', e)
