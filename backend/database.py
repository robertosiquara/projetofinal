
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from  sqlalchemy.ext.declarative import declarative_base

#URL de conexão
database_url = 'mysql+pymysql://root:@localhost/Wayne_security1'

#prepara a conexão
engine = create_engine(database_url)

#cria fabrica de sessão para interagir com o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Usada para criar as tabelas através das classes
Base = declarative_base()

#Função para criar uma nova sessão
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()