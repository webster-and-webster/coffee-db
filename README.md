# Coffee DB <a href="http://coffee-db.herokuapp.com/"><img src="docs/logo.png" align="right" height="138" /></a>

Coffee DB is a web app to track purchases of bags of coffee. The app is built with a Streamlit frontend, which allows you to add new coffees and visualise the coffee database. The backend uses a postgres SQL database to store the coffees. Both the app and the databse are hosted using Heroku. The app can be accessed at the following url: https://coffee-db.herokuapp.com/

## Running Locally

In order to run the app locally, it requires you to have [postgresql](https://www.postgresql.org/) installed on your machine. Once postgresql is installed, run the `helpers/db_init.sql` file to build the database that matches the production schemas. This will give you the correct tables for the app to run correctly.

In order to connect locally, add a settings.ini file in the root directory of the project. The file should look like the following:
```
[postgresql]
host=localhost
dbname=your_database
user=your_user
password=your_password
```

Install the requirements either through `Poetry` or through the `requirements.txt`.

```
pip install -r requirements.txt
```
or
```
poetry install
```

Then run the streamlit app from the root directory.

```
streamlit run app.py
```

## Package management with Poetry and requirements.txt
The project uses `poetry` for it's package management. However, the Python buildpack for Heroku requires a `requirements.txt` ([see docs](https://elements.heroku.com/buildpacks/heroku/heroku-buildpack-python)) file to be available. To generate the `requirements.txt` from the `poetry` environment, run the following command:
```
poetry export --without-hashes --format=requirements.txt > requirements.txt
```

## Formatting with Make
There is a simple github action to test formatting and linting using black and flake8 respectively. To run these checks locally prior to pushing your changes, use the following command:
```
make lint
```

## Testing with pytest
The project uses pytest for testing. Testing is split into unit-tests and integration tests. The tests are checked as part of the CICD pipeline, but they can be run manually with the following make commands:
```
make unit-tests
make integration-tests
```
Note: In order for the tests to pass, you must have an available connection to a PSQL database.
Note: Integration tests use TestContainers to run a fresh psql database in an isolated container. 


## Heroku Commands

### Deploying to Heroku

The repository is set to automatically deploy when pushing to `main`, dependant on the CI pipelines passing. You can manually deploy the app using the following command:
```
git push heroku main
```


### Heroku PSQL CLI

Use the following command to interact with the deployed psql database:

```
heroku pg:psql
```
