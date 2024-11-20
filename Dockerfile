FROM python:3.10

COPY ./requirements.txt .

RUN apt-get update -y \
&& apt-get install -y portaudio19-dev espeak-ng

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt


# sudo apt-get install python3-gi gir1.2-gst-1.0
# sudo apt-get install gstreamer1.0-tools gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly
# sudo apt-get install libcairo2-dev
# sudo apt-get install gobject-introspection libgirepository1.0-dev