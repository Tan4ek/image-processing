import unittest

from image_recognition.image_processing import ImageRecogniseMessageProcessing


class ImageProcessing(unittest.TestCase):

    def test_image_recognise_message_processing(self):
        image_recognise_message_processing = ImageRecogniseMessageProcessing(crop_image=False)
        message_payload = {
            'path': '../resources/FACE.jpg',
            'file': 'FACE.jpg',
            'simple_hash': 'aaaa',
            'a_hash': 'bbb',
            'db_id': str('stub_db_id')
        }
        result = image_recognise_message_processing.process_message(message_payload)
        self.assertEqual(result['original_path'], message_payload['path'])
        self.assertEqual(result['original_file'], message_payload['file'])
        self.assertEqual(result['a_hash'], message_payload['a_hash'])
        self.assertEqual(result['simple_hash'], message_payload['simple_hash'])
        self.assertEqual(result['db_id'], message_payload['db_id'])
        self.assertEqual(len(result['recognised_objects']), 1)
