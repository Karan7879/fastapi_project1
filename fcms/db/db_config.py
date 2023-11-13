# from sqlalchemy import create_engine,text

# engine = create_engine("sqlite:///fcms.db")
# with engine.connect() as connection:
#     result = connection.execute(text('select "Testing"'))
#     print(result)


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_URL = "sqlite:///fcms.db"  # Use SQLite database file "fcms.db" in the current directory

engine = create_engine(DB_URL)
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
