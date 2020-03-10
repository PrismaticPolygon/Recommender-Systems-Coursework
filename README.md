# Recommender Systems Coursework

Develop a context-aware recommender system (CARS) music application. This project re-uses the web app developed for
Web Technology. It uses the [MusicMicro](http://www.cp.jku.at/datasets/musicmicro/index.html) dataset, and a physical 
context comprising three factors: country, whether or not it is a weekend, and the season.

## Structure

* `load.py`: downloads, processes, and saves the MusicMicro dataset for use in the DB and SVD.
* `recommender.py`: generates recommendations. Uses SVD followed by `SciPy` optimisation to compute a context-weight
matrix (CAMF-C style). Saves two files to `weights`: the context parameters themselves, and the DataFrame of 
predictions.
* `benchmark.py`: calculates benchmarks for use in report.
* `config.py`: contains config settings for the DB and geolocation.
* `location.py`: contains a simple function to retrieve the user's country from their IP address, 
using [ipinfo.io](https://ipinfo.io/developers).
* `web.py`: entry point for Flask application, found in `app`.

## Running

The system has been tested with Python 3.6. To run locally:
* Create a virtual environment using `python -m venv venv`
* Activate the virtual environment by:
    * `cd venv/Scripts`
    * `activate`
    * `cd ../..`
* Install the required packages using `pip install -r requirements.txt`.
* Download data using `python load.py`.
* Calculate context weights and predictions using `python recommender.py`. This may take some time!
* Initialise the database using `flask db upgrade`.
* Fill the database using `python import.py`. This may take some time!
* Run using `flask run`.
* Navigate to `127.0.0.1/5000`. This page is simply a list of all tracks.
* Navigate to `127.0.0.1/5000/user/<user-id>` to see user-specific recommendations.
