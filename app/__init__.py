"""app package

initialize app
"""

import os
from flask import Flask
from flask.logging import create_logger
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

# init app
ABS_PATH = os.path.abspath("app/sites")
app = Flask(__name__, template_folder=ABS_PATH)

CORS(app) # TODO: research CORS
logger = create_logger(app)

# initialize driver. construct connection string between engine and database
engine = create_engine("sqlite:///data.db")

# create a session to conect to the database
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine))

# TODO: look into this
# defines the base class for all models
Base = declarative_base()
Base.query = db_session.query_property()


@app.teardown_appcontext
def shutdown_session(exception=None):
    """shutdown current session"""

    if exception:
        print(exception)

    db_session.remove()
