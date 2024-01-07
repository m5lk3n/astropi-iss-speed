# Astro Pi Mission Space Lab 2023/24

The goal of this project is to determine the ISS' travel speed around the earth in km/s using data retrieved from the [Astro Pi Sensors](https://astro-pi.org/about/the-sensors/) and/or including the Astro Pi's camera.

For more details, please see [this page](https://astro-pi.org/mission-space-lab).

*The purpose of this repo is to provide a framework that allows to focus on the actual problem solving - **implementing `main.py`'s `calc_*` functions appropriately**!*

## Mission Space Lab Links

- [Mission Space Lab Resources](https://astro-pi.org/mission-space-lab/resources)
- Examples:
  - [Calculate the speed of the ISS using photos](https://projects.raspberrypi.org/en/projects/astropi-iss-speed/)
  - [Calculate the speed of the ISS using the magnetometer](https://esamultimedia.esa.int/docs/edu/ap_2020/VidhyasCode_report.pdf)
- Sample data:
  - [Sensor data](https://docs.google.com/spreadsheets/d/1RjPEp2IHVB6For65wuUQdWntsg1H5sHWpYUtLzK9LCM/edit#gid=671905630)
  - [Photos](https://www.flickr.com/photos/raspberrypi/collections/72157722152451877/)

## Prerequisites

### IDE

1. Install [Thonny](https://thonny.org/)
2. Install Packages:
In Thonny, Tools -> Manage packages -> Search and Install
- exif
- logzero
- black
- [astro-pi-replay](https://projects.raspberrypi.org/en/projects/mission-space-lab-creator-guide/2)
3. Install Plugins:
In Thonny, Tools -> Manage plug-ins -> Search and Install
- [thonny-black-format](https://pypi.org/project/thonny-black-formatter/)
- [thonny-astro-pi-replay](https://projects.raspberrypi.org/en/projects/mission-space-lab-creator-guide/2)

## Quickstart

- `git clone` this repo
- Open `main.py` in Thonny
- Optional: `Tools` -> `Format with Black`
- `Run` -> `Astro-Pi-Replay` and check `result.txt`: The latter file must carry the current timestamp and must contain a single line saying `7.34641`.

## Constraints

- Consider max. amount of images (42), image sizes and available max. storage size (*"You are allowed to produce up to 250MB of data."*)!

## To do

- Test with Python 3.9.2 (ideally on a Pi)
- Deploy (mode)
- Add exception handling 
- [Testing](https://projects.raspberrypi.org/en/projects/mission-space-lab-creator-guide/5)
- [Improve accuracy](https://projects.raspberrypi.org/en/projects/mission-space-lab-creator-guide/4)
- [Document](https://projects.raspberrypi.org/en/projects/documenting-your-code/)
- Zip

## Other Bookmarks

- [Python Naming Conventions](https://gist.github.com/etigui/7600441926e73c3385057718c2fdef8e)
- [Haversine formula in Python (bearing and distance between two GPS points)](https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points)
- [Python: get GPS latitude and longitude coordinates from JPEG EXIF using exifread](https://gist.github.com/snakeye/fdc372dbf11370fe29eb)
- [Translate Exif DMS to DD Geolocation with Python](https://stackoverflow.com/questions/6460381/translate-exif-dms-to-dd-geolocation-with-python)