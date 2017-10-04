from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_declarative import Base, Todo, Tag

engine = create_engine('sqlite:///todosAndTags.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Insert a Todo in the todo table
session.add_all([
    Todo(title='build an API', placeNumber=1, completed=False),
    Todo(title='?????', placeNumber=2, completed=False),
    Todo(title='profit!', placeNumber=3, completed=False)
])
session.commit()
