from fastapi import APIRouter
from db_config import Base,engine,get_db
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException,Depends
from models import Auditorium,Multiplex
from fastapi import APIRouter
from request_body import AuditoriumCreate
Session = sessionmaker(bind=engine)


audirouter = APIRouter()

@audirouter.post("/addaudi")
async def create_auditorium(auditorium: AuditoriumCreate, db: Session = Depends(get_db)):
    # Check if the multiplex with the specified multiplex_id exists
    multiplex = db.query(Multiplex).filter(Multiplex.id == auditorium.multiplex_id).first()
    if not multiplex:
        raise HTTPException(status_code=404, detail="Multiplex not found")

    # Create the auditorium and associate it with the multiplex
    new_auditorium = Auditorium(**auditorium.dict())
    db.add(new_auditorium)
    db.commit()
    db.refresh(new_auditorium)
    db.close()
    return new_auditorium

# def map_index_to_name(row, col):
#     # Convert the row index to a letter using ASCII values (A=65, B=66, and so on)
#     name = chr(ord('A') + row)
#     # Add 1 to the column index to match your example
#     number = col + 1
#     return f'({name},{number})'

# # Example usage
# row = 10
# col = 10
# for i in range(0,10):
#     for j in range(0,10):

#         result = map_index_to_name(i, j)
#         print(result)  # Output: (A,1)