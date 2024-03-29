import configparser

from file_scaner.file_scanner_processor import FileScannerProcessor
from file_scaner.image_face_recognise_scanner_processor import CropFaceRecogniseScannerProcessor
from file_scaner.image_face_recognised_processor import CropFaceRecognisedProcessor
from file_scaner.image_recognised_processor import RecognisedProcessor

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    recognised_processor = RecognisedProcessor(db_uri=config['mongo']['Uri'],
                                               db_image_name=config['mongo']['ImageDb'],
                                               kafka_host=config['kafka']['Host'],
                                               kafka_image_recognised_result_topic=config['kafka'][
                                                   'ImageRecogniseResultTopic'])

    file_scanner_processor = FileScannerProcessor(db_uri=config['mongo']['Uri'],
                                                  db_image_name=config['mongo']['ImageDb'],
                                                  root_path_for_scanning=config['main']['RootPathForScanning'],
                                                  ignore_path_for_scanning=config['main']['IgnorePathForScanning'],
                                                  kafka_host=config['kafka']['Host'],
                                                  kafka_image_topic=config['kafka']['ImageRecogniseTopic'])
    crop_face_scanner_processor = CropFaceRecogniseScannerProcessor(db_uri=config['mongo']['Uri'],
                                                                    db_image_name=config['mongo']['ImageDb'],
                                                                    kafka_host=config['kafka']['Host'],
                                                                    kafka_face_recognise_topic=config['kafka'][
                                                                        'ImageFaceRecogniseTopic'])
    crop_face_recognised_processor = CropFaceRecognisedProcessor(db_uri=config['mongo']['Uri'],
                                                                 db_image_name=config['mongo']['ImageDb'],
                                                                 kafka_host=config['kafka']['Host'],
                                                                 kafka_face_recognise_result_topic=config['kafka'][
                                                                     'ImageFaceRecogniseResultTopic'])
    recognised_processor.start()
    file_scanner_processor.start()
    crop_face_scanner_processor.start()
    crop_face_recognised_processor.start()

    recognised_processor.join()
    file_scanner_processor.join()
    crop_face_scanner_processor.join()
    crop_face_recognised_processor.join()
