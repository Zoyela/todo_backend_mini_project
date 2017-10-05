from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
# Base.metadata.create_all(engine)


def create_db_connection(app):
    # Create an engine that stores data in the local directory's todos_and_tags.db
    app['engine'] = create_engine('sqlite:///todos_and_tags.db')
    app['session'] = sessionmaker(bind=app['engine'])

