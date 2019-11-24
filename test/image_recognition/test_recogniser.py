import unittest

from PIL import Image

from image_recognition.recogniser import FaceRecogniser


class TestFaceRecogniser(unittest.TestCase):

    def test_recognise(self):
        face_recogniser = FaceRecogniser()
        self.assertEqual(face_recogniser.recognise_type(), 'FACE_RECOGNITION')
        file_path = '../resources/FACE.jpg'
        with Image.open(file_path) as image:
            recognise = face_recogniser.recognise(image, file_path)
            self.assertEqual(len(recognise['recognise_objects']), 1)
            self.assertEqual(len(recognise['metadata']), 1)
