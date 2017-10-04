from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

# declare a mapping
global Base
Base = declarative_base()

# backref
#TodoTags = Table(
#    'TodoTags', Base.metadata,
#    Column('todo_id', Integer, ForeignKey('Todo.id')),
#    Column('tag_id', Integer, ForeignKey('Tag.id'))
#)


# define mapped classes
class Todo(Base):
    __tablename__ = 'todo'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    placeNumber = Column(Integer)
    completed = Column(Integer)
    #tags = relationship(
    #    "Tag",
    #    secondary=TodoTags,
    #    backref="todos"
    #)

    def to_dictionary(self):
        return {
            "id": self.id,
            "title": self.title,
            "placeNumber": self.placeNumber,
            "completed": self.completed
        }


#class Tag(Base):
#    __tablename__ = 'tag'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
#    id = Column(Integer, primary_key=True)
#    name = Column(String(250))

#    def to_dictionary(self):
#        return {
#            "id": self.id,
#            "name": self.name,
#            "todo": self.todos
#        }

