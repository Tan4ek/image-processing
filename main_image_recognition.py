import configparser

from image_recognition.image_processing import ImageRecogniseMessageProcessing
from util.abstract_image_processing import ImageProcessing

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    message_processing = ImageRecogniseMessageProcessing(crop_image=True,
                                                         crop_face_location_path=config['main']['CroppedFacesPath'])
    image_processing = ImageProcessing(kafka_host=config['kafka']['Host'],
                                       kafka_image_recognise_topic=config['kafka']['ImageRecogniseTopic'],
                                       kafka_image_recognise_result_topic=config['kafka']['ImageRecogniseResultTopic'],
                                       kafka_response_topic=config['kafka']['ImageRecogniseResultTopic'],
                                       message_processing=message_processing)
    image_processing.start()
