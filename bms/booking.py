from fastapi import APIRouter
from db_config import Base,engine,get_db
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException,Depends
from models import Auditorium,Multiplex,Shows,Booking
from fastapi import APIRouter
from request_body import AuditoriumCreate,Bookings
Session = sessionmaker(bind=engine)
from signup import oauth2_scheme,SECRET_KEY,ALGORITHM
import jwt

boookingroutes = APIRouter()

@boookingroutes.post("/book")
async def book_show(booking_data: Bookings, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        search_seat = db.query(Shows).filter(Shows.id == booking_data.show_id).first()
        select_seat = db.query(Auditorium).filter(Auditorium.id == search_seat.auditorium_id).first()

        if select_seat.seats_arrangement[booking_data.seat_number[0]][int(booking_data.seat_number[1])-1] == 0:
            select_seat.seats_arrangement[booking_data.seat_number[0]][int(booking_data.seat_number[1])-1] = 1
            db.commit()

            new_shows = Booking(**booking_data.dict())
            new_shows.amount = search_seat.pricing[booking_data.seat_number[0]]

            opuser = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            new_shows.user_id = opuser["sub"]

            db.add(new_shows)
            db.commit()
            db.refresh(new_shows)

            return "Booked"
        else:
            return "Seat already booked"
    finally:
        db.close()
# In this modified version, I've used a try/finally block to ensure that the db.close() statement is executed even if an exception occurs. This way, the database session will be closed, and any changes will be committed before closing the session.










# @boookingroutes.post("/book")
# async def book_show(booking_data:Bookings,db: Session=Depends(get_db),token: str =Depends(oauth2_scheme)):
#     print(booking_data.seat_number[1])
#     search_seat = db.query(Shows).filter(Shows.id==booking_data.show_id).first()
#     print(search_seat)
#     # db.close()
#     select_seat = db.query(Auditorium).filter(Auditorium.id==search_seat.auditorium_id).first()
#     print(select_seat)
#     # db.close()
    

#     if select_seat.seats_arrangement[booking_data.seat_number[0]][int(booking_data.seat_number[1])-1] == 0:
#         select_seat.seats_arrangement[booking_data.seat_number[0]][int(booking_data.seat_number[1])-1] = 1
#         # db.add(select_seat)
#         db.commit()
#         db.close()
#         new_shows = Booking(**booking_data.dict())
#         new_shows.amount=search_seat.pricing[booking_data.seat_number[0]]
#         opuser = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         new_shows.user_id = opuser["sub"]

#         db.add(new_shows)
#         db.commit()
#         db.refresh(new_shows)
#         db.close()
        
        
#         return "Booked"
    
#     else:
#         return "Seat already booked"


    # db.close()

    # new_shows = Booking(**booking_data.dict())
    # new_shows.show_id = str(booking_data.seat_number_i) + str(booking_data.seat_number_j)
    # db.add(new_shows)
    # db.commit()
    # db.refresh(new_shows)
    # db.close()
    return new_shows

  
@boookingroutes.get("/bookings")
async def gets_shows(userID, db: Session=Depends(get_db)):
    user_bookings = db.query(Booking).filter(Booking.user_id == userID).all()
    db.close()
    # print(user_bookings)
    for u in user_bookings:
        show_details = db.query(Shows).filter(Shows.id == u.show_id).first()
    
    db.close()
    return show_details

   

    # joined_data = (
    #     db.query(Multiplex, Booking, Shows)
    #     .join(Shows, Booking.id == Shows.id)
    #     .join(Multiplex, Multiplex.id == Shows.id)
    #     .all()
    # )
    # db.close()
    
    # return joined_data










  # results = db.query(Booking, Shows).join(Booking).first()
    # filter(booking_data.show_id == Shows.id).all()
    # result = engine.execute("SELECT booking.show_id, booking.name, your_table.name FROM my_table LEFT JOIN your_table ON my_table.name = your_table.name")

# Print the fetched rows
    # for row in result.fetchall():
    #     print(row)


    # if booking_data.auditorium_id !=None and booking_data.multiplex_id!=None:
    #     multiplex = db.query(Multiplex).filter(Multiplex.id==booking_data.multiplex_id).first()
    #     db.close()
    #     auditorium = db.query(Auditorium).filter(Auditorium.id==booking_data.auditorium_id).first()
    #     db.close()
    #     if not multiplex or not auditorium:
    #         raise HTTPException(status_code=404,detail="Multiplex or Audi not found")


