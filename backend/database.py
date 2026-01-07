from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


#crio o caminho da conexao
database_url = 'mysql+pymysql://root:@localhost/Wayne_security1'

#sistema para conexão
engine = create_engine(database_url)

#cria as sessões para interagir com o banco de dados
#Session é uma classe do SQLAlchemy que representa uma conexão ativa com o banco de dados.(SELECT, INSERT, UPDATE...)
#Não confirma alterações automaticamente (autocommit=False)
#Não sincroniza dados automaticamente antes de cada consulta (autoflush=False)
#Está conectada ao banco definido pelo engine (bind=engine).
SessionLocal = sessionmaker(autocommit= False, autoflush= False, bind= engine)

#Usado para criar as tabelas através das classes
class Base (DeclarativeBase):
     pass

#função para conectar com o banco de dados e depois fechar qdo termiar
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
