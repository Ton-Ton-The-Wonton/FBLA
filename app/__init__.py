"""app package

initialize app
"""

from flask import Flask
from flask.logging import create_logger
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
from configs.__init__ import Config

# init app
app = Flask(__name__)
logger = create_logger(app)
logger.setLevel(Config.LOG_LEVEL)

# init db
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


@app.teardown_appcontext
def shutdown_session(exception=None):
    """shutdown current session"""

    if exception:
        logger.warning(exception)

    db_session.remove()
