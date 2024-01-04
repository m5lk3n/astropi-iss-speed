from datetime import datetime, timedelta
from time import sleep
from math import radians, cos, sin, asin, sqrt
from exif import Image
from logzero import logger
from picamera import PiCamera
from orbit import ISS


# https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
def haversine(lon1, lat1, lon2, lat2):  # TODO: swap order lon <-> lat
    """
    Calculate the great circle distance in kilometers between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Earth's mean radius in kilometers. Determines return value unit as km.
    # - https://sci.esa.int/web/solar-system/-/35649-earth
    r += 420  # ISS orbits earth at ~420km altitude as per ESA ISS tracker info
    # - https://www.esa.int/Science_Exploration/Human_and_Robotic_Exploration/International_Space_Station/Where_is_the_International_Space_Station
    # - https://www.esa.int/Science_Exploration/Human_and_Robotic_Exploration/Lessons_online/Life_in_Space#:~:text=The%20ISS%20is%20orbiting%20400,be%20taken%20there%20from%20Earth.
    return c * r


def convert_to_degress(value):
    degrees = value[0]
    minutes = value[1]
    seconds = value[2]

    return degrees + (minutes / 60.0) + (seconds / 3600.0)


# "CONSTANTS"
IMAGE_PATH = "tests/"  # for testing, use "" for deployment
MAX_DURATION_IN_MINS = 1  # for testing, use 9 for deployment
MAX_ITERATIONS = 3  # for testing, use 42 for deployment
SLEEP_TIMEOUT_IN_SECS = 5  # for testing, TODO for deployment


# returns image time in seconds since Epoch time (1/1/1970)
def get_time_in_seconds_since_epoch(image):
    time_str = image.get("datetime_original")
    # TODO: if time_str, else value? handling?
    time = datetime.strptime(time_str, "%Y:%m:%d %H:%M:%S")
    # https://pynative.com/python-datetime-to-seconds/
    epoch_time = datetime(1970, 1, 1)
    delta = time - epoch_time

    return delta.total_seconds()


def get_location_as_lat_lon(image):
    lat_ref_str = image.get("gps_latitude_ref")
    lat_str = image.get("gps_latitude")  # tuple of degrees, minutes, and seconds
    lon_ref_str = image.get("gps_longitude_ref")
    lon_str = image.get("gps_longitude")  # tuple of degrees, minutes, and seconds

    if (
        lat_ref_str and lat_str and lon_ref_str and lon_str
    ):  # TODO: else value? handling?
        lat = convert_to_degress(lat_str)
        if lat_ref_str != "N":
            lat = 0 - lat

        lon = convert_to_degress(lon_str)
        if lon_ref_str != "E":
            lon = 0 - lon

    return lat, lon


def get_image_meta_data(iteration):
    with open(f"{IMAGE_PATH}{iteration}.jpg", "rb") as image_file:  # open read, binary
        image = Image(image_file)
        time_in_seconds = get_time_in_seconds_since_epoch(image)
        lat, lon = get_location_as_lat_lon(image)
    image_file.close()

    return time_in_seconds, lat, lon


# source: https://projects.raspberrypi.org/en/projects/mission-space-lab-creator-guide/2
def convert(angle):
    # Convert a `skyfield` Angle to an Exif-appropriate
    # representation (positive rationals)
    # e.g. 98° 34' 58.7 to "98/1,34/1,587/10"

    # Return a tuple containing a Boolean and the converted angle,
    # with the Boolean indicating if the angle is negative

    sign, degrees, minutes, seconds = angle.signed_dms()
    exif_angle = f"{degrees:.0f}/1,{minutes:.0f}/1,{seconds*10:.0f}/10"
    return sign < 0, exif_angle


# source: https://projects.raspberrypi.org/en/projects/mission-space-lab-creator-guide/2
def take_picture(iss, camera, iteration):
    if IMAGE_PATH == "tests/":
        return

    # Use `camera` to capture an `image` file with lat/long Exif data
    point = iss.coordinates()

    # Convert the latitude and longitude to Exif-appropriate
    # representations
    south, exif_latitude = convert(point.latitude)
    west, exif_longitude = convert(point.longitude)

    # Set the Exif tags specifying the current location
    camera.exif_tags["GPS.GPSLatitude"] = exif_latitude
    camera.exif_tags["GPS.GPSLatitudeRef"] = "S" if south else "N"
    camera.exif_tags["GPS.GPSLongitude"] = exif_longitude
    camera.exif_tags["GPS.GPSLongitudeRef"] = "W" if west else "E"

    logger.info(f"taking picture {IMAGE_PATH}{iteration}.jpg")

    # Capture the image
    camera.capture(f"{IMAGE_PATH}{iteration}.jpg")


def calc_speed_from_pictures(iteration):
    if iteration <= 0:
        logger.info("nothing to compare")
        return (
            -1
        )  # we define a negative speed as an "invalid" value to indicate that we couldn't calculate

    logger.info(f"comparing pictures {iteration}.jpg and {iteration - 1}.jpg")

    time_in_seconds_cur, lat_cur, lon_cur = get_image_meta_data(iteration)
    logger.info(f"current: {time_in_seconds_cur}, {lat_cur}, {lon_cur}")

    time_in_seconds_prev, lat_prev, lon_prev = get_image_meta_data(iteration - 1)
    logger.info(f"prev: {time_in_seconds_prev}, {lat_prev}, {lon_prev}")

    time_in_seconds = time_in_seconds_cur - time_in_seconds_prev
    distance_in_km = haversine(lon_cur, lat_cur, lon_prev, lat_prev)
    logger.info(f"distance between images in km: {distance_in_km}")
    logger.info(f"time between images in s: {time_in_seconds}")

    speed = distance_in_km / time_in_seconds
    logger.info(f"speed in km/s: {speed}")

    return abs(speed)  # absolute value just in case


## https://projects.raspberrypi.org/en/projects/mission-space-lab-creator-guide/3

logger.info("started")

# init.
start_time = datetime.now()
now_time = datetime.now()
total_speed_in_kmps = 0
i = 0  # iteration
cam = PiCamera()
cam.resolution = (4056, 3040)

while now_time < start_time + timedelta(minutes=MAX_DURATION_IN_MINS):
    if i >= MAX_ITERATIONS:
        break  # exit while

    logger.info(f"iteration {i} started")
    take_picture(ISS(), cam, i)
    speed_in_kmps = calc_speed_from_pictures(i)
    logger.info(f"iteration {i} ended in {speed_in_kmps} km/s")

    if speed_in_kmps >= 0:
        total_speed_in_kmps += speed_in_kmps

    i += 1
    sleep(SLEEP_TIMEOUT_IN_SECS)
    now_time = datetime.now()

cam.close()

# we define a negative speed as an "invalid" value to indicate that we couldn't calculate
avg_speed_in_kmps = -1.0
if i > 1:  # we needed at least 2 iterations for a comparison
    avg_speed_in_kmps = total_speed_in_kmps / (i - 1)  # -1 to skip first iteration

avg_speed_in_kmps_formatted = "{:.5f}".format(avg_speed_in_kmps)
result_file = "result.txt"
with open(result_file, "w", encoding="utf-8") as file:
    file.write(avg_speed_in_kmps_formatted)
file.close()

logger.info(f"result written to {result_file}")

logger.info(f"calculated travel speed of the ISS: {avg_speed_in_kmps_formatted} km/s")
# https://projects.raspberrypi.org/en/projects/astropi-iss-speed/7
logger.info("actual travel speed of the ISS: 7.66 km/s")


logger.info("ended")
