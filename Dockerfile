FROM python:2.7-slim
WORKDIR /app
ADD . /app
RUN echo deb http://ftp.debian.org/debian jessie-backports main >> /etc/apt/sources.list
RUN apt-get update
RUN apt-get -y install ffmpeg
RUN pip install -r requirements.txt
CMD ["python", "-u", "server/consumer.py"]
