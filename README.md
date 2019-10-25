# OPENALPR - HA API

This docker container is designed to read GB Number plates from a mpeg4 video stream. Please ensure your camera is either designed for number plate recognition or you have a suitably configured high specification camera. I can't offer any advice on the camera configuration as there are too many settings and too many cameras on the market.

It is specifically designed to call Home Assistant using the API and will execute a script called script.ANPR. Create this script in HA and put what ever automation you want in it.

When it recognises a number plate it will then enter a time out ensuring that the same number plate does not fire the script multiple times. It will just as easy call another api of your choice with a few little changes.


## Configure

### Environment Variables

You will need to run the container with the following variables;

HA_APIENDPOINT e.g. 'http://192.168.1.68:8123/api/services/script/turn_on'

HA_APIPASSWORD e.g. your HA API password

STREAM_SOURCE e.g. rtsp://192.168.0.60/mpeg4'

### Configure Number Plates

At present you need to configure the number plates you want recognising in the readstream.py.

### Build & Run

docker build -t openalpr .

docker run openalpr:latest
