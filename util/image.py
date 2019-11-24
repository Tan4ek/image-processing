import hashlib
import os
from collections import namedtuple

import imagehash
from PIL.ExifTags import GPSTAGS
from PIL.ExifTags import TAGS

ImageMetadata = namedtuple('ImageMetadata', ['exif', 'GPS'])


def _replace_not_str_key(diction):
    keys = list(diction.keys())
    for key in keys:
        if isinstance(diction[key], dict):
            _replace_not_str_key(diction[key])
        if not isinstance(key, str):
            value = diction[key]
            del diction[key]
            diction[str(key)] = value


def _get_labeled_exif(exif):
    labeled = {}
    for (key, val) in exif.items():
        labeled[TAGS.get(key)] = val
    if None in labeled:
        del labeled[None]
    _replace_not_str_key(labeled)
    return labeled


def _get_geotagging(exif):
    if not exif:
        raise ValueError("No EXIF metadata found")

    geotagging = {}
    for (idx, tag) in TAGS.items():
        if tag == 'GPSInfo':
            if idx in exif:
                for (key, val) in GPSTAGS.items():
                    if key in exif[idx]:
                        geotagging[val] = exif[idx][key]

    return geotagging


def _get_decimal_from_dms(dms, ref):
    degrees = dms[0][0] / dms[0][1]
    minutes = dms[1][0] / dms[1][1] / 60.0
    seconds = dms[2][0] / dms[2][1] / 3600.0

    if ref in ['S', 'W']:
        degrees = -degrees
        minutes = -minutes
        seconds = -seconds

    return round(degrees + minutes + seconds, 5)


def _get_coordinates(geo_tags):
    lat = _get_decimal_from_dms(geo_tags['GPSLatitude'], geo_tags['GPSLatitudeRef'])

    lon = _get_decimal_from_dms(geo_tags['GPSLongitude'], geo_tags['GPSLongitudeRef'])

    return {'lat': lat, 'lon': lon}


def get_image_exif(pil_image) -> ImageMetadata:
    exif = pil_image._getexif()
    if not exif:
        return ImageMetadata({}, None)
    labeled_exif = _get_labeled_exif(exif)
    geo_tags = _get_geotagging(exif)
    coordinates = None
    coordinates_labels = ['GPSLatitude', 'GPSLatitudeRef', 'GPSLongitude', 'GPSLongitudeRef']
    all_coordinate_labels = [x for x in coordinates_labels if x in geo_tags]
    if geo_tags and len(coordinates_labels) == len(all_coordinate_labels):
        coordinates = _get_coordinates(geo_tags)

    return ImageMetadata(labeled_exif, coordinates)


# return (wight, height)
def get_image_dimention(pil_image) -> (float, float):
    return pil_image.size


def get_image_size_bytes(pil_image) -> int:
    filename = pil_image.filename

    return os.path.getsize(filename)


def get_average_image_hash(pil_image) -> str:
    return str(imagehash.average_hash(pil_image))


# Вычисляет хэш файла из пути и размера файла, основная идея - не читать файл
def get_simple_image_hash(file_path) -> str:
    size = os.path.getsize(file_path)
    return hashlib.md5((str(size) + file_path).encode('utf-8')).hexdigest()
