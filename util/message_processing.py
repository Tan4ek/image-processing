from collections import namedtuple

# coordinate = { 'top': 10, 'right': 20, 'bottom': 30, 'left': 40 }
RecogniseObject = namedtuple('RecogniseObject', ['object_type', 'coordinate'])


class AbstractMessageProcessing(object):

    def process_message(self, message_payload):
        """
         Обработка сообщения из очереди
        :message_payload - тело сообщения
        :rtype: None - если не было обработано, причина, например - файл не найден,
                dict - объект который будет обработан далее по логике
        """
        raise NotImplementedError
