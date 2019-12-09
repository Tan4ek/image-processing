import logging
import os
from collections import namedtuple
from datetime import datetime

import face_recognition
import numpy as np
from PIL import Image

from file_scaner.file_scanner_processor import FileScanner
from util.message_processing import AbstractMessageProcessing
from util.util import current_milli_time

EtalonFaceModel = namedtuple('EtalonFaceModel', ['name', 'path', 'face_encodings'])


class FaceRecognitionMessageProcessing(AbstractMessageProcessing):

    def __init__(self, etalon_faces_path):
        etalon_faces_path = etalon_faces_path.rstrip('/') + '/'
        self.etalon_faces_path = etalon_faces_path
        self.__etalon_faces = self._load_etalon_faces(etalon_faces_path)

    def _load_etalon_faces(self, etalon_faces_path):
        etalon_faces = []

        for file_name in (i for i in os.listdir(etalon_faces_path) if self._file_is_image(i)):
            (face_name, ext) = os.path.splitext(file_name)
            file_path = os.path.join(etalon_faces_path, file_name)
            etalon_image = face_recognition.load_image_file(file_path)
            etalon_face_encoding = face_recognition.face_encodings(etalon_image)[0]
            etalon_faces.append(EtalonFaceModel(face_name, file_path, etalon_face_encoding))

        return etalon_faces

    def _file_is_image(self, file_name):
        return FileScanner.is_image(file_name)

    def process_message(self, message_payload):
        file_path = message_payload['path']
        file_name = message_payload['file']
        time_before_face_compare = current_milli_time()
        tolerance = 0.5

        with Image.open(file_path) as image:
            rgb_image = image.convert('RGB')
            start_execution_datetime = str(datetime.utcnow())

            unknown_image = np.array(rgb_image)
            face_encodings = face_recognition.face_encodings(unknown_image)
            if len(face_encodings) > 0:
                known_faces = [f.face_encodings for f in self.__etalon_faces]
                compare_result = face_recognition.compare_faces(known_faces, face_encodings[0], tolerance=tolerance)
                recognised_faces = [{'name': etalon_face.name,
                                     'etalon_path': etalon_face.path,
                                     'tolerance': tolerance}
                                    for etalon_face, is_etalon_face in zip(self.__etalon_faces, compare_result)
                                    if is_etalon_face]
            else:
                recognised_faces = []
            time_after_face_compare = current_milli_time()
            execution_time_ms = time_after_face_compare - time_before_face_compare
            logging.info('Recognise faces: %s , for image: %s , in %s ms', str([f['name'] for f in recognised_faces]),
                         file_path, str(execution_time_ms))
            return {
                'original_path': file_path,
                'original_file': file_name,
                'db_id': message_payload['db_id'],
                'recognised_faces': recognised_faces,
                'timestamp': str(datetime.utcnow()),
                'metadata': {
                    'execution_time_ms': execution_time_ms,
                    'start_execution_datetime': start_execution_datetime
                }
            }
