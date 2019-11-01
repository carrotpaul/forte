# Python 3.7 Slim (the bare minimum to keep the image small)
FROM python:3.7-slim

# Set working directory
WORKDIR /app
ADD . /app

# Install GCC and all required dependencies
RUN apt-get update \
    && apt-get install -y build-essential
# Update source file to include Debian backport and install FFMPEG
RUN echo deb http://ftp.debian.org/debian jessie-backports main \
    >> /etc/apt/sources.list \
    && apt-get update \
    && apt-get install -y ffmpeg

# Install python app dependencies
RUN pip install -r requirements.txt

# Start the app
CMD ["python", "-u", "server/main.py"]
