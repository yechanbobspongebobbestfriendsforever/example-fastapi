from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database-name>'

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}!@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

# engine is what is responsible for sqlalchemy to connect postgres database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False,
    bind=engine
)

# All the models that we define to create tables in Postgres are going to be extending Base class
Base = declarative_base()

def get_db():
    ## session object is responsible for talking with the database
    ## this function will get a connection to our database or get session to our database
    ## everytime we get request, we are going to get a session
    ## term: database session represents an application's dialog with a relational database
    
    db = SessionLocal() 
    try:
        yield db
    finally:
        db.close()
        
        
        
######################## DEPRECIATED #############################
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time

# while True:
#     try:
#         conn = psycopg2.connect(  
#             host="localhost", 
#             database="fastapi",
#             user="postgres",
#             port=----,
#             password=
#             cursor_factory=RealDictCursor,
#         ) 
#         cursor = conn.cursor()
#         print('Database connection was succesfull!')
#         break
        
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error: ", error)
#         time.sleep(2)
