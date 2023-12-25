from math import radians, cos, sin, asin, sqrt
from exif import Image
from datetime import datetime

# https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Determines return value unit as km.
    r += 400 # ISS orbits earth (https://www.esa.int/Science_Exploration/Human_and_Robotic_Exploration/Lessons_online/Life_in_Space#:~:text=The%20ISS%20is%20orbiting%20400,be%20taken%20there%20from%20Earth.)
    return c * r

# ---------- data points approach ----------
# source of data points: https://docs.google.com/spreadsheets/d/1RjPEp2IHVB6For65wuUQdWntsg1H5sHWpYUtLzK9LCM/edit#gid=671905630

# data points 1 and 300
distanceInKm = haversine(66.77867751,-20.2800441,69.11392852,-17.45516549)
timeInS = 63
speedInKmPerS1 = distanceInKm / timeInS
print(distanceInKm, "km in", timeInS, "s =", speedInKmPerS1, "km/s")

# data points 1117 and 1396
distanceInKm = haversine(75.77266642,-8.716663614,77.96575012,-5.672454996)
timeInS = 60
speedInKmPerS2 = distanceInKm / timeInS
print(distanceInKm, "km in", timeInS, "s =", speedInKmPerS2, "km/s")

# data points 36509 and 36784
distanceInKm = haversine(171.5097129,47.64335562,176.3749973,45.99076451)
timeInS = 60
speedInKmPerS3 = distanceInKm / timeInS
print(distanceInKm, "km in", timeInS, "s =", speedInKmPerS3, "km/s")

# data points 47309 and 47584
distanceInKm = haversine(-69.50729155,-49.8513892,-63.8963865,-50.79717797)
timeInS = 60
speedInKmPerS4 = distanceInKm / timeInS
print(distanceInKm, "km in", timeInS, "s =", speedInKmPerS4, "km/s")

# data points 49920 and 50220
distanceInKm = haversine(-18.00219328,-46.90519689,-13.0462651,-45.05238817)
timeInS = 63
speedInKmPerS5 = distanceInKm / timeInS
print(distanceInKm, "km in", timeInS, "s =", speedInKmPerS5, "km/s")

avgSpeedInKmPerS = (speedInKmPerS1 + speedInKmPerS2 + speedInKmPerS3 + speedInKmPerS4 +speedInKmPerS5) / 5

print("Avg. travel speed across 5 data points: %.4f" % avgSpeedInKmPerS, "km/s")
print("Actual travel speed of the ISS: 7.66kmps") # https://projects.raspberrypi.org/en/projects/astropi-iss-speed/7

print("----------")

# ---------- photos approach ----------
# source of photos: https://www.flickr.com/photos/raspberrypi/collections/72157722152451877/

def print_exif(image):
    with open(image, 'rb') as image_file:
        img = Image(image_file)
        for data in img.list_all():
            print(data)

def get_time(image):
    with open(image, 'rb') as image_file:
        img = Image(image_file)
        time_str = img.get("datetime_original")
        time = datetime.strptime(time_str, '%Y:%m:%d %H:%M:%S')
        # https://pynative.com/python-datetime-to-seconds/
        epoch_time = datetime(1970, 1, 1)
        delta = (time - epoch_time)
        
    return delta.total_seconds()

def get_location(image):
    with open(image, 'rb') as image_file:
        img = Image(image_file)
        
        lat_ref_str = img.get("gps_latitude_ref")
        lat_str = img.get("gps_latitude") # tuple of degrees, minutes, and seconds
        lon_ref_str = img.get("gps_longitude_ref")
        lon_str = img.get("gps_longitude") # tuple of degrees, minutes, and seconds
        
        lat = convert_to_degress(lat_str)
        if lat_ref_str != 'N':
            lat = 0 - lat
        
        lon = convert_to_degress(lon_str)
        if lon_ref_str != 'E':
            lon = 0 - lon
        # how to convert to degrees:
        # - https://gist.github.com/snakeye/fdc372dbf11370fe29eb
        # - https://stackoverflow.com/questions/4764932/in-python-how-do-i-read-the-exif-data-for-an-image
        # - https://stackoverflow.com/questions/6460381/translate-exif-dms-to-dd-geolocation-with-python
    return lon, lat

def convert_to_degress(value):
    degrees = value[0]
    minutes = value[1]
    seconds = value[2] 

    return degrees + (minutes / 60.0) + (seconds / 3600.0)
    

#print_exif('photos/1.jpg')
#print(get_time('photos/photo_232.jpg'))
# GPS Latitude Ref - North
# GPS Latitude - 48 deg 12' 26.30"
# GPS Longitude Ref - East
# GPS Longitude - 19 deg 38' 33.20"
#print(get_location('photos/photo_232.jpg'))

t0 = get_time('photos/1.jpg')
t1 = get_time('photos/2.jpg')
timeInS = t1 - t0

loc0 = get_location('photos/1.jpg')
loc1 = get_location('photos/2.jpg')
distanceInKm = haversine(loc1[0],loc1[1],loc0[0],loc0[1])

speedInKmPerS = distanceInKm / timeInS
print(distanceInKm, "km in", timeInS, "s =", speedInKmPerS, "km/s")
