import logging
import os

__IMG_EXTENTIONS__ = ('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')


class FileScanner:

    def __init__(self, root_path_for_scanning, ignore_paths=[]):
        self.root_path = root_path_for_scanning
        self.ignore_paths = ignore_paths

    @staticmethod
    def is_image(name, root=''):
        (_, ext) = os.path.splitext(name)
        return ext.lower() in __IMG_EXTENTIONS__

    def iterate(self):
        if os.path.isdir(self.root_path):
            for root, dirs, files in os.walk(self.root_path):
                if root in self.ignore_paths:
                    logging.debug('Skip scan directory %s. Reason: in ignore list', root)
                    continue
                logging.debug('Scanning files in %s directory', root)
                for name in files:
                    file_path = os.path.join(root, name)
                    if FileScanner.is_image(name, root) and os.path.isfile(file_path):
                        yield file_path, root, name
        else:
            raise ValueError("Root path for scanning images is not a dir. {}".format(self.root_path))
