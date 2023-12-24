from math import radians, cos, sin, asin, sqrt

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
