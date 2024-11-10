FROM ubuntu:latest
RUN apt-get update && apt-get install -y python3-venv build-essential cmake imagemagick

COPY wa2refont/requirements.txt /tmp/requirements.txt
RUN python3 -m venv /wa2translate/python/venv
RUN /wa2translate/python/venv/bin/pip install -r /tmp/requirements.txt

COPY wa2repack /wa2translate/wa2repack/
RUN mkdir /wa2translate/wa2repack/build
WORKDIR /wa2translate/wa2repack/build
RUN /usr/bin/cmake ..
RUN make

COPY wa2refont /wa2translate/wa2refont/

COPY translate.sh /wa2translate/
WORKDIR /wa2translate
CMD ["bash", "/wa2translate/translate.sh"]

# docker build -t wa2translate .
# docker run -v %cd%:/wa2translate/myVolume wa2translate
# docker run -v ${pwd}:/wa2translate/myVolume wa2translate
