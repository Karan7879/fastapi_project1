from fastapi import FastAPI
from db_config import Base,engine
import signup
import multiplexes
import audi
import shows
import booking
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(signup.signups)
app.include_router(multiplexes.addingmultiplexe)
app.include_router(audi.audirouter)
app.include_router(shows.showsroute)
app.include_router(booking.boookingroutes)

