from db_config import Base
from sqlalchemy import Column, Integer, String, ForeignKey,JSON,Enum, DateTime,Boolean,Interval,Float
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"  # The name of the table in the database

    # id = Column(Integer, primary_key=True, index=True)
    username = Column(String, primary_key=True, index=True)
    password = Column(String,unique=False,index=True)
    email = Column(String, unique=True, index=True)
    position = Column(Enum("customer", "owner", "admin"), default="available")
    full_name = Column(String)
    bookings = relationship("Booking",back_populates="users")
        
      
class Booking(Base):
    __tablename__ = "booking"
    id = Column(Integer, primary_key=True, index=True)
    seat_number = Column(String, unique=False)
    # Need to add how if user has booked ticket for multiple user
    amount = Column(Integer,unique=False)
    booking_time = Column(DateTime)
    cancel_time = Column(DateTime)
    show_name = Column(String)
    show_id = Column(Integer, ForeignKey("show.id"))
    audi_name = Column(String)
    multiplex_name = Column(String)
    user_id = Column(Integer, ForeignKey("users.username"))

    users = relationship("User",back_populates = "bookings")
    shows = relationship("Shows",back_populates = "bookings")


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
    # show_timings = Column(JSON)
    startdate = Column(DateTime)
    enddate = Column(DateTime)
    difference = Column(Interval)
    pricing = Column(JSON)
    status  = Column(Boolean)



    auditorium_id = Column(Integer, ForeignKey("auditoriums.id"))
    multiplex_id = Column(Integer, ForeignKey("multiplexes.id"))

    auditorium = relationship("Auditorium", back_populates="shows")
    multiplex = relationship("Multiplex", back_populates="shows")
    bookings = relationship("Booking",back_populates = "shows")

# class Auditorium(Base):
#     __tablename__ = "auditorium"
#     id = Column(Integer, primary_key=True, index=True)
#     auditorium_name = Column(String)
#     seats_count = Column(Integer)
#     seats_arrangment = Column(JSON)
#     # Add a field to store the multiplex's ID
#     multiplex_id = Column(Integer, ForeignKey("multiplexes.id"))

#     # Define a relationship to the Multiplex model
#     multiplex = relationship("Multiplex", back_populates="auditoriums")
#     shows = relationship("Shows", back_populates="auditorium")



# class Multiplex(Base):
#     __tablename__ = "multiplexes"
#     id = Column(Integer, primary_key=True, index=True)
#     multiplex_name = Column(String)
#     audi_count = Column(Integer)
#     owner = Column(String)
#     owner_email = Column(String)

#     auditoriums = relationship("Auditorium", back_populates="multiplex")
#     shows = relationship("Shows", back_populates="multiplex")





# from db_config import Base, engine

# # # # Drop a specific table
# table_name = "show"  # Replace with the name of the table you want to drop

# # Ensure the table exists in the metadata
# if table_name in Base.metadata.tables:
#     # Drop the table
#     Base.metadata.tables[table_name].drop(engine)
#     print(f"Table '{table_name}' has been dropped.")
# else:
#     print(f"Table '{table_name}' does not exist in the database.")

# # Close the engine if needed
# engine.dispose()


