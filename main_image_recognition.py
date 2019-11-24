import configparser

from image_recognition.image_processing import ImageProcessing

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    image_processing = ImageProcessing(kafka_host=config['kafka']['Host'],
                                       kafka_image_recognise_topic=config['kafka']['ImageRecogniseTopic'],
                                       kafka_image_recognise_result_topic=config['kafka']['ImageRecogniseResultTopic'],
                                       cropped_faces_path=config['main']['CroppedFacesPath'])
    image_processing.start()
