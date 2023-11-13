from request_body import ShowCreate
from fastapi import APIRouter, Depends, HTTPException
from db_config import get_db
from db_config import sessionmaker,engine
Session = sessionmaker(bind=engine)
from models import Multiplex,Auditorium,Shows

showsroute = APIRouter()

@showsroute.post("/addshows")
async def create_shows(show:ShowCreate, db: Session=Depends(get_db)):
    if show.auditorium_id !=None and show.multiplex_id!=None:
        multiplex = db.query(Multiplex).filter(Multiplex.id==show.multiplex_id).first()
        db.close()
        auditorium = db.query(Auditorium).filter(Auditorium.id==show.auditorium_id).first()
        db.close()
        if not multiplex or not auditorium:
            raise HTTPException(status_code=404,detail="Multiplex or Audi not found")
    new_shows = Shows(**show.dict())
    new_shows.difference = new_shows.enddate-new_shows.startdate
    new_shows.status = True
    db.add(new_shows)
    db.commit()
    db.refresh(new_shows)
    db.close()
    return new_shows

@showsroute.get("/get_shows_details")
async def getshowdetails(showID,db:Session=Depends(get_db)):
    searchshow = db.query(Shows).get(showID)
    db.close()
    # if searchshow:
    print(searchshow.id)

    searchaudi = db.query(Auditorium).get(searchshow.auditorium_id)
    db.close()
    # searchshow.Auditorium
    getMultiplex = db.query(Multiplex).get(searchshow.multiplex_id)
    db.close()
    
    print(searchaudi.seats_arrangement)

    return {"show_name":searchshow.show_name,
            "pricing":searchshow.pricing,
            "show_id":showID,
            "show_timings":searchshow.startdate,
            "auditorium_name":searchaudi.auditorium_name,
            "seats_arrangement":searchaudi.seats_arrangement,
            "multiplex_name":getMultiplex.multiplex_name}



