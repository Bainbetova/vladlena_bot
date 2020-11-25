from pprint import pprint
from io import BytesIO
from typing import Tuple, Optional, Union, BinaryIO

import exifread

# Функция возвращает файл
def get_exif_data(file: Union[BytesIO, BinaryIO]) -> dict:
    return exifread.process_file(file)

# Функция возвращает координаты
def get_location(exif_data: dict) -> Optional[Tuple[float, float]]:
    lat = None #широта
    lon = None #долгота

    gps_latitude = exif_data.get('GPS GPSLatitude')
    gps_latitude_ref = exif_data.get('GPS GPSLatitudeRef')
    gps_longitude = exif_data.get('GPS GPSLongitude')
    gps_longitude_ref = exif_data.get('GPS GPSLongitudeRef')

    print(gps_latitude, gps_latitude_ref)
    print(gps_longitude, gps_longitude_ref)

    if gps_longitude and gps_longitude_ref and gps_latitude and gps_latitude_ref:
        lat = convert_to_degrees(gps_latitude)
        if gps_latitude_ref.values[0] != 'N':
            lat = 0 - lat #изменение знака для западной стороны света
        lon = convert_to_degrees(gps_longitude)
        if gps_longitude_ref.values[0] != 'E':
            lon = 0 - lon #изменение знака для западной стороны света

    return lat, lon

# Функция конвертирует GPS данные в градусы
def convert_to_degrees(value):
    d = float(value.values[0].num) / float(value.values[0].den)
    m = float(value.values[1].num) / float(value.values[1].den)
    s = float(value.values[2].num) / float(value.values[2].den)

    return d + (m / 60.0) + (s / 3600.0)


#with open('2.jpg', 'rb') as f:
#    my_data = get_exif_data(f)
#my_location = get_location(my_data)
#print(my_location)
