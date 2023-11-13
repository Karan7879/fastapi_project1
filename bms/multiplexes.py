from request_body import AddMultiplex
from models import Multiplex,User
from fastapi import APIRouter,Depends
from request_body import UserCreate
from db_config import Base,engine
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
from signup import oauth2_scheme,SECRET_KEY,ALGORITHM
import jwt
from db_config import get_db


addingmultiplexe = APIRouter()

@addingmultiplexe.post("/addmultiplex")
async def addmultiplex(mult_data:AddMultiplex,token: str =Depends(oauth2_scheme),db:Session=Depends(get_db)):
    print(jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]))
    opuser = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user = db.query(User).filter(User.username == opuser['sub']).first()
    db.close()
    if user.position!="admin":
        return "Access Denied"
    db = Session()
    mult = Multiplex(**mult_data.dict())
    db.add(mult)
    db.commit()
    db.refresh(mult)
    db.close()
    return mult




