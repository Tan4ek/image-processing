import logging
import os
import uuid
from datetime import datetime

import face_recognition
import numpy as np

from util.message_processing import RecogniseObject
from util.util import current_milli_time

FACE_RECOGNISE_TYPE = 'FACE_DETECTION'


class AbstractRecogniser(object):

    def recognise_type(self) -> str:
        """
        Тип распознования: лицо, объекты и пр.
        """
        raise NotImplementedError

    def recognise(self, pil_image, file_path) -> RecogniseObject:
        """
        Распознать объекты типа recognise_type на изображении
        :param pil_image: An :py:class:`~PIL.Image.Image` object.
        :param file_path: str : путь до файла распознования, None если не определен
        :return dict {'recognise_objects': array RecogniseObject, 'recognise_type': 'SMILE_RECOGNITION',
                        'metadata': dict}
        """
        raise NotImplementedError


class FaceRecogniser(AbstractRecogniser):
    __RECOGNISE_OBJECT_ = 'face'

    def __init__(self, crop_face=False, crop_face_location_path=''):
        self.crop_face = crop_face
        if crop_face and not crop_face_location_path:
            raise ValueError("'crop_face_location_path' should exist when 'crop_face' enabled")
        self.crop_face_location_path = crop_face_location_path.rstrip('/') + '/'

    def recognise_type(self) -> str:
        return FACE_RECOGNISE_TYPE

    def recognise(self, pil_image, file_path):
        start_execution_datetime = str(datetime.utcnow())
        time_before_face_location = current_milli_time()

        # faces - (top, right, bottom, left)
        im = pil_image.convert('RGB')
        np_array_image = np.array(im)
        face_location = face_recognition.face_locations(np_array_image)
        time_after_face_location = current_milli_time()

        file_name_full = os.path.basename(file_path)
        file_name, extension = os.path.splitext(file_name_full)

        recognise_objects = []
        cropped_faces = []
        for top, right, bottom, left in face_location:
            recognise_object = RecogniseObject(object_type=FaceRecogniser.__RECOGNISE_OBJECT_,
                                               coordinate={'top': top, 'right': right, 'bottom': bottom, 'left': left})
            if self.crop_face:
                cropped_faces.append(self._crop_face(pil_image, file_name, extension, bottom, left, right, top))
            recognise_objects.append(recognise_object)

        result = {
            'recognise_objects': recognise_objects,
            'recognise_type': self.recognise_type(),
            'metadata': {
                'execution_time_ms': time_after_face_location - time_before_face_location,
                'start_execution_datetime': start_execution_datetime
            }
        }
        if self.crop_face:
            result['cropped_faces'] = cropped_faces

        return result

    def _crop_face(self, pil_image, file_name, extension, bottom, left, right, top):
        cropped = pil_image.crop((left, top, right, bottom))
        crop_face_image_id = '{}__{}'.format(file_name, str(uuid.uuid4()))
        face_image_path = self.crop_face_location_path + crop_face_image_id + extension
        cropped.save(face_image_path)
        logging.info('Saving crop image %s.', face_image_path)
        return {
            'face_image_path': face_image_path,
            'crop_face_id': crop_face_image_id,
            'face_location': {
                'top': top,
                'right': right,
                'bottom': bottom,
                'left': left
            }
        }
