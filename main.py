from datetime import datetime, timedelta
from time import sleep
from math import radians, cos, sin, asin, sqrt
from exif import Image
from datetime import datetime
from logzero import logger

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
    r = 6371 # Earth's mean radius in kilometers. Determines return value unit as km.
    # - https://sci.esa.int/web/solar-system/-/35649-earth
    r += 420 # ISS orbits earth at ~420km altitude as per ESA ISS tracker info
    # - https://www.esa.int/Science_Exploration/Human_and_Robotic_Exploration/International_Space_Station/Where_is_the_International_Space_Station
    # - https://www.esa.int/Science_Exploration/Human_and_Robotic_Exploration/Lessons_online/Life_in_Space#:~:text=The%20ISS%20is%20orbiting%20400,be%20taken%20there%20from%20Earth.
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

avgSpeedInKmPerS = (speedInKmPerS1 + speedInKmPerS2 + speedInKmPerS3 + speedInKmPerS4 + speedInKmPerS5) / 5

print("Avg. travel speed across 5 data points: %.5f" % avgSpeedInKmPerS, "km/s")
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
        # TODO: if time_str, else value? handling?
        time = datetime.strptime(time_str, '%Y:%m:%d %H:%M:%S')
        # https://pynative.com/python-datetime-to-seconds/
        epoch_time = datetime(1970, 1, 1)
        delta = (time - epoch_time)
        
    return delta.total_seconds() # TODO: absolute value?

def get_location(image):
    with open(image, 'rb') as image_file:
        img = Image(image_file)
        
        lat_ref_str = img.get("gps_latitude_ref")
        lat_str = img.get("gps_latitude") # tuple of degrees, minutes, and seconds
        lon_ref_str = img.get("gps_longitude_ref")
        lon_str = img.get("gps_longitude") # tuple of degrees, minutes, and seconds
        
        if lat_ref_str and lat_str and lon_ref_str and lon_str: # TODO: else value? handling?
            lat = convert_to_degress(lat_str)
            if lat_ref_str != 'N':
                lat = 0 - lat
        
            lon = convert_to_degress(lon_str)
            if lon_ref_str != 'E':
                lon = 0 - lon
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

t0 = get_time('photos/photo_232.jpg')
t1 = get_time('photos/photo_237.jpg')
timeInS = t1 - t0

loc0 = get_location('photos/photo_232.jpg')
loc1 = get_location('photos/photo_237.jpg')
distanceInKm = haversine(loc1[0],loc1[1],loc0[0],loc0[1])

speedInKmPerS1 = distanceInKm / timeInS # TODO: absolute value?
print(distanceInKm, "km in", timeInS, "s =", speedInKmPerS1, "km/s")

t0 = get_time('photos/photo_237.jpg')
t1 = get_time('photos/photo_242.jpg')
timeInS = t1 - t0

loc0 = get_location('photos/photo_237.jpg')
loc1 = get_location('photos/photo_242.jpg')
print(loc1)
distanceInKm = haversine(loc1[0],loc1[1],loc0[0],loc0[1])

speedInKmPerS2 = distanceInKm / timeInS # TODO: absolute value?
print(distanceInKm, "km in", timeInS, "s =", speedInKmPerS2, "km/s")

t0 = get_time('photos/Andromeda_0025.jpg')
t1 = get_time('photos/Andromeda_0041.jpg')
timeInS = t1 - t0

loc0 = get_location('photos/Andromeda_0025.jpg')
loc1 = get_location('photos/Andromeda_0041.jpg')
print(loc1)
distanceInKm = haversine(loc1[0],loc1[1],loc0[0],loc0[1])

speedInKmPerS3 = distanceInKm / timeInS # TODO: absolute value?
print(distanceInKm, "km in", timeInS, "s =", speedInKmPerS3, "km/s")

avgSpeedInKmPerS = (speedInKmPerS1 + speedInKmPerS2 + speedInKmPerS3) / 3

print("Avg. travel speed across 3 photos: %.5f" % avgSpeedInKmPerS, "km/s")
print("Actual travel speed of the ISS: 7.66kmps") # https://projects.raspberrypi.org/en/projects/astropi-iss-speed/7

######################################################################################################################

# "CONSTANTS"
IMAGE_PATH = "photos/"
MAX_DURATION_IN_MINS = 1 # for testing, use 9 for deployment
MAX_ITERATIONS = 3 # for testing, use 42 for deployment
SLEEP_TIMEOUT_IN_SECS = 5 # for testing, TODO for deployment

# returns image time in seconds since Epoch time (1/1/1970)
def get_time_in_seconds_since_epoch(image):
    time_str = image.get("datetime_original")
    # TODO: if time_str, else value? handling?
    time = datetime.strptime(time_str, '%Y:%m:%d %H:%M:%S')
    # https://pynative.com/python-datetime-to-seconds/
    epoch_time = datetime(1970, 1, 1)
    delta = (time - epoch_time)

    return delta.total_seconds()

def get_location_as_lat_lon(image):
    lat_ref_str = image.get("gps_latitude_ref")
    lat_str = image.get("gps_latitude") # tuple of degrees, minutes, and seconds
    lon_ref_str = image.get("gps_longitude_ref")
    lon_str = image.get("gps_longitude") # tuple of degrees, minutes, and seconds

    if lat_ref_str and lat_str and lon_ref_str and lon_str: # TODO: else value? handling?
        lat = convert_to_degress(lat_str)
        if lat_ref_str != 'N':
            lat = 0 - lat

        lon = convert_to_degress(lon_str)
        if lon_ref_str != 'E':
            lon = 0 - lon

    return lat, lon

def get_image_meta_data(i):
    with open(f"{IMAGE_PATH}{i}.jpg", 'rb') as image_file: # open read, binary
        image = Image(image_file)
        time_in_seconds = get_time_in_seconds_since_epoch(image)
        lat, lon = get_location_as_lat_lon(image)

    return time_in_seconds, lat, lon

def take_picture(i):
    logger.info(f"taking picture {i}.jpg")

def calc_speed_from_pictures(i):
    if i <= 0:
        logger.info("nothing to compare")
        return -1 # we define a negative speed as an "invalid" value to indicate that we couldn't calculate

    logger.info(f"comparing pictures {i}.jpg and {i - 1}.jpg")

    time_in_seconds_cur, lat_cur, lon_cur = get_image_meta_data(i)
    logger.info(f"current: {time_in_seconds_cur}, {lat_cur}, {lon_cur}")

    time_in_seconds_prev, lat_prev, lon_prev = get_image_meta_data(i - 1)
    logger.info(f"prev: {time_in_seconds_cur}, {lat_cur}, {lon_cur}")

    time_in_seconds = time_in_seconds_cur - time_in_seconds_prev
    distance_in_km = haversine(lon_cur, lat_cur, lon_prev, lat_prev)
    logger.info(f"distance between images in km: {distance_in_km}")
    logger.info(f"time between images in s: {time_in_seconds}")

    speed_in_kmps = distance_in_km / time_in_seconds
    logger.info(f"speed in km/s: {speed_in_kmps}")

    return abs(speed_in_kmps) # absolute value just in case

## https://projects.raspberrypi.org/en/projects/mission-space-lab-creator-guide/3

logger.info("started")

start_time = datetime.now()
now_time = datetime.now()
total_speed_in_kmps = 0
i = 0 # iteration

while (now_time < start_time + timedelta(minutes=MAX_DURATION_IN_MINS)):
    if( i >= MAX_ITERATIONS ):
        break # exit while

    logger.info(f"iteration {i} started")
    take_picture(i)
    speed_in_kmps = calc_speed_from_pictures(i)
    logger.info(f"iteration {i} ended in {speed_in_kmps} km/s")

    if( speed_in_kmps >= 0 ):
        total_speed_in_kmps += speed_in_kmps

    i += 1
    sleep(SLEEP_TIMEOUT_IN_SECS)
    now_time = datetime.now()

if( i > 1 ): # we needed at least 2 iterations for a comparison
    avg_speed_in_kmps = total_speed_in_kmps / (i-1) # -1 to skip first iteration

estimate_kmps_formatted = "{:.5f}".format(avg_speed_in_kmps)
result_file = "result.txt"
with open(result_file, 'w') as file:
    file.write(estimate_kmps_formatted)

logger.info(f"result written to {result_file}")

logger.info("ended")
