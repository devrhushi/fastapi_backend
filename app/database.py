#holds db connection 
from sqlalchemy import create_engine #establish connection with pg
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}'
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)

SessionLocal = sessionmaker(autocommit = False,autoflush=False, bind = engine)

Base = declarative_base()
# yeild is genrator will pause till my api interacts with database or perfroms db opns ince response back to user it closesd the conn
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# import psycopg2
# from psycopg2.extras import RealDictCursor

# while True:
#     try:
#         conn = psycopg2.connect(
#             host="localhost",
#             database="fastapi",
#             user="postgres",
#             password="postgres123",
#         )
#         cursor = conn.cursor(cursor_factory=RealDictCursor)
#         print("database conn successfull")
#         break

#     except Exception as error:
        # time.sleep(2)
#         print("connecting to database failed")
#         print("Error", error)