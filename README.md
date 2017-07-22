## Forte

A simple Python server that downloads music from various sites
(whatever Youtube-DL can handle), and uploads it to your Google
Music account. It uses a worker to enqueue tasks as requests come
into the system.

Comes with a chrome extension that allows you to download from the
site you are currently browsing from.

### Local Setup

(Assuming that you've cloned this repo somehow)

1. Install virtualenv and run it within the repo
```bash
$ cd path/to/forte
$ virtualenv env
```
2. Like other similar Python programs, the app uses `pip` for
downloading dependencies. With `pip` installed on your machine,
run the following to install everything that Forte needs to run
properly.
```bash
$ pip install -r requirements.txt
```
3. This project was made with Heroku in mind; download the Heroku-CLI. See their
[documentation](https://devcenter.heroku.com/articles/heroku-cli) for more
details.
4. Run the app using the following command:
```bash
$ heroku local
```
This will create a development-friendly server and host the
application on http://localhost:5000. It will set all environment variables from
the `.env` file and run the worker for you as well.
