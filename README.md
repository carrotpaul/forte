## Forte

A simple Python server that downloads music from various sites
(whatever Youtube-DL can handle), and uploads it to your Google
Music account. It uses a worker to enqueue tasks as requests come
into the system.

Comes with a chrome extension that allows you to download from the
site you are currently browsing from.

### Local Setup

(Assuming that you've cloned this repo somehow)

1. This project was made with Docker in mind. You can download Docker via their [official site](https://www.docker.com/get-docker).

2. For the application to work, you will need to set an authorization token. The app itself authenticates using a salt & pepper hashing algorithm.

    Generate a random pepper, and figure out the encrypted value of your password using the in-app salt. Place the encrypted password, along with the pepper in `server/auth/auth_certificate` with the encrypted password on the first line, and the pepper on the following line.

    **Note:** If your pepper is very long, feel free to splice it into multiple lines. However, this will append the `\n` character for each line, and therefore to the final pepper string itself. This will affect the encryption of your secret.

    ```bash
    $ touch server/auth/auth_certificate
    $ echo $encryptedPassword >> server/auth/auth_certificate
    $ echo $generatedPepper >> server/auth/auth_certificate
    ```

3. Before you can run `docker-compose`, you will be required to build the image for the source code. You may tag the build as you wish (as long as the name is still `forte`).
    ```bash
    $ docker build -t forte .
    $ docker-compose up -d
    ```
4. Check to make sure that all the containers are up and running as expected using `docker-compose ps`.
    ```bash
    Name                 Command                          State   Ports
    ========================================================================================================
    forte_kafka-rest_1   /etc/confluent/docker/run        Up      0.0.0.0:8082->8082/tcp
    forte_kafka_1        /etc/confluent/docker/run        Up      0.0.0.0:9092->9092/tcp
    forte_web_1          python -u server/consumer.py     Up
    forte_zookeeper_1    /docker-entrypoint.sh zkSe ...   Up      0.0.0.0:2181->2181/tcp, 2888/tcp, 3888/tcp
    ```
    Use `docker logs <container_name>` to dig into anything that broke.
