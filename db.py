# create requirements.txt
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Establish db connection
username = 'admin'
password = 'vistavol_asset'
host = 'vistavol.c7ai0uaw6krx.ap-southeast-2.rds.amazonaws.com'
database_name = 'vistavol'
database_url = f'mysql+pymysql://{username}:{password}@{host}/{database_name}'

# access db on the cmd
# cd C:\Program Files\MySQL\MySQL Server 8.0
# mysql -u admin -h vistavol.c7ai0uaw6krx.ap-southeast-2.rds.amazonaws.com vistavol -p

engine = create_engine(database_url, pool_pre_ping=True, echo=True)  
print(engine)
Base = declarative_base()

# Create session local class for session maker
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False) 

def get_session():
  session = SessionLocal()
  try:
      yield session
  finally:
      session.close()
