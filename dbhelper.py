from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from todosAndTags import Base

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
# Base.metadata.create_all(engine)


def create_db_connection(app):
    # Create an engine that stores data in the local directory's todosAndTags.db
    app['engine'] = create_engine('sqlite:///todosAndTags.db')
    app['session'] = sessionmaker(bind=app['engine'])

