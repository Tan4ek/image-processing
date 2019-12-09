import os
import unittest

from image_face_recognition.face_recognition_processing import FaceRecognitionMessageProcessing


class FaceProcessing(unittest.TestCase):

    def test_face_recognition(self):
        image_recognition_message_processing = FaceRecognitionMessageProcessing(
            etalon_faces_path='../resources/etalon_paths')
        dmitri_faces_path = '../resources/dmitri_faces'
        db_id = '1'
        for file_name in os.listdir(dmitri_faces_path):
            abs_image_path = os.path.join(dmitri_faces_path, file_name)

            result = image_recognition_message_processing.process_message({'path': abs_image_path,
                                                                           'file': file_name,
                                                                           'db_id': db_id})
            self.assertEqual(result['original_path'], abs_image_path)
            self.assertEqual(result['original_file'], file_name)
            self.assertEqual(result['db_id'], db_id)
            self.assertTrue(result['metadata']['execution_time_ms'] > 0)
            self.assertTrue(len(result['recognised_faces']) > 0)
