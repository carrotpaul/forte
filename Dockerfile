# Use an official Python runtime as a parent image
FROM python:2.7-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Define environment variable
ENV AUTH_SECRET ""
ENV AUTH_PASSWORD ""
ENV KAFKA_CONSUMER_TOPIC "forte-download"
# If you're using Docker for Mac, replace localhost with your machine's en0
ENV KAFKA_CONSUMER_BROKERS "localhost:9092"

# Run app.py when the container launches
CMD ["python", "server/consumer.py"]
