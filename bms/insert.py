from sqlalchemy import create_engine, Column, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Define the database URL (replace with your actual database URL)
DATABASE_URL = "sqlite:///testing.db"

# Create an SQLAlchemy engine and session
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

# Define the Multiplex model
class Multiplex(Base):
    __tablename__ = "multiplexes"
    id = Column(Integer, primary_key=True, index=True)
    multiplex_name = Column(String)
    audi_count = Column(Integer)
    owner = Column(String)
    owner_email = Column(String)
    
    # Define relationships to other models
    auditoriums = relationship("Auditorium", back_populates="multiplex")
    shows = relationship("Shows", back_populates="multiplex")

# # Define the Auditorium model
class Auditorium(Base):
    __tablename__ = "auditoriums"
    id = Column(Integer, primary_key=True, index=True)
    auditorium_name = Column(String)
    seats_count = Column(Integer)
    seats_arrangement = Column(JSON)
    
#     # Add a field to store the multiplex's ID
    multiplex_id = Column(Integer, ForeignKey("multiplexes.id"))

    # Define relationships to other models
    multiplex = relationship("Multiplex", back_populates="auditoriums")
    shows = relationship("Shows", back_populates="auditorium")

# # Define the Shows model
class Shows(Base):
    __tablename__ = "show"
    id = Column(Integer, primary_key=True, index=True)
    show_name = Column(String, unique=False)
    show_timings = Column(JSON)

    auditorium_id = Column(Integer, ForeignKey("auditoriums.id"))
    multiplex_id = Column(Integer, ForeignKey("multiplexes.id"))

    auditorium = relationship("Auditorium", back_populates="shows")
    multiplex = relationship("Multiplex", back_populates="shows")
    
    

# Create the database tables if they don't exist
Base.metadata.create_all(bind=engine)

# Insert data into the Multiplex model
multiplex1 = Multiplex(multiplex_name="CinePlex", audi_count=5, owner="John Doe", owner_email="john@example.com")
multiplex2 = Multiplex(multiplex_name="MegaCinema", audi_count=3, owner="Alice Smith", owner_email="alice@example.com")

session.add(multiplex1)
session.add(multiplex2)
session.commit()

# # Insert data into the Auditorium model
auditorium1 = Auditorium(auditorium_name="Audi 1", seats_count=100, seats_arrangement={})
auditorium2 = Auditorium(auditorium_name="Audi 2", seats_count=150, seats_arrangement={})

auditorium1.multiplex = multiplex1
auditorium2.multiplex = multiplex1

session.add(auditorium1)
session.add(auditorium2)
session.commit()



# # Insert data into the Shows model
show1 = Shows(show_name="Movie 1", show_timings=["10:00 AM", "3:00 PM"])
show2 = Shows(show_name="Movie 2", show_timings=["1:00 PM", "6:00 PM"])

show1.auditorium = auditorium1
show2.auditorium = auditorium2
show1.multiplex = multiplex1  # Assign the multiplex to the show
show2.multiplex = multiplex1 

session.add(show1)
session.add(show2)
session.commit()

# Close the session
session.close()
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from models import Base, Multiplex, Auditorium, Shows

# # Replace 'DATABASE_URL' with your actual database URL
# DATABASE_URL = "sqlite:///testing.db"
# engine = create_engine(DATABASE_URL)

# # Create the tables if they don't exist
# Base.metadata.create_all(bind=engine)

# # Create a session
# Session = sessionmaker(bind=engine)
# session = Session()

# # Insert data into the Multiplex model
# multiplex1 = Multiplex(multiplex_name="CinePlex", audi_count=5, owner="John Doe", owner_email="john@example.com")
# multiplex2 = Multiplex(multiplex_name="MegaCinema", audi_count=3, owner="Alice Smith", owner_email="alice@example.com")

# # Add and commit the multiplex data to the database
# session.add(multiplex1)
# session.add(multiplex2)
# session.commit()

# # # Insert data into the Auditorium model
# # auditorium1 = Auditorium(auditorium_name="Audi 1", seats_count=100, seats_arrangment={})
# # auditorium2 = Auditorium(auditorium_name="Audi 2", seats_count=150, seats_arrangment={})

# # # Assign the multiplex to the auditorium
# # auditorium1.multiplex = multiplex1
# # auditorium2.multiplex = multiplex1

# # # Add and commit the auditorium data to the database
# # session.add(auditorium1)
# # session.add(auditorium2)
# # session.commit()

# # # Insert data into the Shows model
# # show1 = Shows(show_name="Movie 1", show_timings=["10:00 AM", "3:00 PM"])
# # show2 = Shows(show_name="Movie 2", show_timings=["1:00 PM", "6:00 PM"])

# # # Assign the auditorium to the show
# # show1.auditorium = auditorium1
# # show2.auditorium = auditorium2

# # # Add and commit the show data to the database
# # session.add(show1)
# # session.add(show2)
# # session.commit()

# # Close the session
# session.close()
