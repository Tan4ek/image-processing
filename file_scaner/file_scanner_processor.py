import logging
import time
import uuid
from datetime import datetime

from PIL import Image
from kafka import KafkaProducer

from file_scaner.abstract_process import AbstractProcess
from file_scaner.db_service import DbImageService
from file_scaner.file_scanner import FileScanner
from util.image import get_image_exif, get_image_dimention, get_image_size_bytes, get_average_image_hash, \
    get_simple_image_hash
from util.util import kafka_json_serializer, current_milli_time

__DELAY_BETWEEN_FILE_SCANNING__ = 10 * 60


class FileScannerProcessor(AbstractProcess):

    def __init__(self, db_uri, db_image_name, root_path_for_scanning, ignore_path_for_scanning, kafka_host,
                 kafka_image_topic):
        super().__init__('FileScannerProcessor')
        self.db_uri = db_uri
        self.db_image_name = db_image_name

        self.root_path_for_scanning = root_path_for_scanning
        self.kafka_host = kafka_host
        self.kafka_image_topic = kafka_image_topic
        #
        self.file_scanner = FileScanner(root_path_for_scanning, ignore_paths=[ignore_path_for_scanning])

    def _process_file(self, file_path, root, file_name):
        logging.info('scan {}'.format(file_path))
        simple_hash = get_simple_image_hash(file_path)

        # важно открывать изображение один раз!
        with Image.open(file_path) as image:
            time_before_hashing = current_milli_time()
            average_hash = get_average_image_hash(image)

            image_metadata = get_image_exif(image)

            wight, height = get_image_dimention(image)
            bytes_size = get_image_size_bytes(image)

            logging.info("size {}x{}, bytes: {}".format(wight, height, bytes_size))

            time_after_hashing = current_milli_time()
            logging.info(
                "time for hash: {}, hash - {}".format(time_after_hashing - time_before_hashing, average_hash))

            image_document = {
                'path': file_path,
                'simple_hash': simple_hash,
                'a_hash': average_hash,
                'name': file_name,
                'scan_datetime': datetime.utcnow(),
                'w': wight,
                'h': height,
                'byte_size': bytes_size,
                'EXIF': image_metadata.exif,
                'gps': image_metadata.GPS,
                'process_steps': []
            }

            inserted_document_id = self._db_image_service.insert_image(image_document)

            message = {
                'message_id': str(uuid.uuid4()),
                'payload': {
                    'path': file_path,
                    'file': file_name,
                    'simple_hash': simple_hash,
                    'a_hash': average_hash,
                    'db_id': str(inserted_document_id)
                }
            }

            try:
                future = self._producer.send(self.kafka_image_topic, message)
                self._producer.flush()
                future.get()
            except Exception as e:
                self._db_image_service.remove_image(inserted_document_id)
                raise e

    def _scan_files(self):
        for file_path, root, file_name in self.file_scanner.iterate():
            try:
                logging.info('scan {}'.format(file_path))
                simple_hash = get_simple_image_hash(file_path)

                image_document = self._db_image_service.find_image_by_path_simple_hash(file_path, simple_hash)
                if image_document is not None:
                    logging.info('Skip file %s. Already exist', file_path)
                    continue

                self._process_file(file_path, root, file_name)

            except Exception as e:
                logging.warning("Can't iterate over file %s. Error: %s", file_path, e)
                # raise e

    def _run(self):
        self._producer = KafkaProducer(bootstrap_servers=self.kafka_host, value_serializer=kafka_json_serializer)

        self._db_image_service = DbImageService(db_uri=self.db_uri, db_image_name=self.db_image_name)

        while True:
            self._scan_files()
            logging.info('File scanner: sleeping for %s seconds', __DELAY_BETWEEN_FILE_SCANNING__)
            time.sleep(__DELAY_BETWEEN_FILE_SCANNING__)
