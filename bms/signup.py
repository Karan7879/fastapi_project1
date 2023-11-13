from models import User
from fastapi import APIRouter,HTTPException,status,Depends
from request_body import UserCreate
from db_config import Base,engine
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext
import jwt
from datetime import datetime,timedelta
from jose import JWTError

# from jose import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

SECRET_KEY = "4da73e5e37d0b92abfbf31be54a38319"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

Session = sessionmaker(bind=engine)

signups = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_jwt_token(user_id):
    payload = {
        "sub": user_id,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}


def decode_jwt_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )





@signups.post("/signup")
async def signup(user_data:UserCreate):
    db = Session()
    user = User(**user_data.dict())
    user.password = pwd_context.hash(user_data.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user



@signups.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    with Session() as session:
        user = session.query(User).filter(User.username == form_data.username).first()
        if user is None or not pwd_context.verify(form_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
    token = create_jwt_token(user.username)
    return token

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_jwt_token(token)
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    with Session() as session:
        user = session.query(User).filter(User.id == user_id).first()
        if user is None:
            raise credentials_exception

    return user

    # @signups.get("/users/me", response_model=User)
    # async def read_users_me(current_user: User = Depends(get_current_user)):
    #     return current_user

@signups.post("/expenses/")
async def create_expense(current_user: str = Depends(oauth2_scheme)):
    decoded_token = jwt.decode(current_user, SECRET_KEY, algorithms=[ALGORITHM])
    # username = decoded_token.get("sub")
    # user_data = users_collection.find_one({"username": username})
    # if not user_data:
    #     raise HTTPException(status_code=400, detail="User not found")
    # expense_data = {
    #     "user_id": user_data["_id"],
    #     "description": expense.description,
    #     "amount": expense.amount,
    #     "expensetime":current_datetime
    # }
    # expense_id = expenses_collection.insert_one(expense_data).inserted_id
    return decoded_token
#{**expense.dict(), "_id": str(expense_id)}


