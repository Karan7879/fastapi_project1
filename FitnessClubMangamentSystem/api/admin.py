from fastapi import APIRouter,Depends
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session
from db_config.sqlalchemy_connect import SessionFactory
from models.requests.signup import SignupReq
from models.data.sqlalchemy_models import Signup
from repository.sqlalchemy.signup import SignupRepository,LoginMemberRepository,MemberAttendanceRepository
from typing import List

router = APIRouter()

def sess_db():
    db = SessionFactory()
    try:
        yield db
    except:
        db.close


@router.post("/signup/add")
def add_signup(req:SignupReq,sess:Session = Depends(sess_db)):
    repo:SignupRepository = SignupRepository(sess)
    signup = Signup(password=req.password,
                    username = req.username,
                    id = req.id
                    )
    result = repo.insert_signup(signup)
    if result==True:
        return signup
    else:
        return JSONResponse(content={
            'message':'create signup problem encountere'
        }, status_code=500)
    
@router.get("signup/list",response_model=List[SignupReq])
def list_signup(sess:Session=Depends(sess_db)):
    repo:SignupRepository = SignupRepository(sess)
    result = repo.get_all_signup()
    return result

@router.patch("/signup/update")
def 





