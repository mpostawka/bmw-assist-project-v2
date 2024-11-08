FROM python:3.10

COPY ./requirements.txt .

RUN apt-get update -y \
&& apt-get install -y portaudio19-dev

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt
