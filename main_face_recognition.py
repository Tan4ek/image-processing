import configparser

from image_face_recognition.face_recognition_processing import FaceRecognitionMessageProcessing
from util.abstract_image_processing import ImageProcessing

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')

    message_processing = FaceRecognitionMessageProcessing(etalon_faces_path=config['main']['RootPathEtalonFaces'])
    image_processing = ImageProcessing(kafka_host=config['kafka']['Host'],
                                       kafka_image_recognise_topic=config['kafka']['ImageFaceRecogniseTopic'],
                                       kafka_image_recognise_result_topic=config['kafka']
                                       ['ImageFaceRecogniseResultTopic'],
                                       kafka_response_topic=config['kafka']['ImageRecogniseResultTopic'],
                                       message_processing=message_processing)
    image_processing.start()
