import logging
import time
import traceback
from multiprocessing import Process

__DELAY_BETWEEN_RERUN__ = 60


class AbstractProcess(Process):

    def __init__(self, process_name):
        super().__init__()
        self.process_name = process_name

    def _run(self):
        raise NotImplementedError

    def run(self):
        while True:
            try:
                self._run()
            except Exception as e:
                ex_traceback = traceback.format_exc()
                logging.error('Processor %s rerun. Exception %s. %s', self.process_name, str(e), ex_traceback)
                logging.warning('Sleep process %s for %s seconds.', self.process_name, str(__DELAY_BETWEEN_RERUN__))
                time.sleep(__DELAY_BETWEEN_RERUN__)
