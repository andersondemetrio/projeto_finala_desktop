from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
import mysql.connector

# Parâmetros de conexão com o banco de dados
host = 'localhost'
user = 'root'
password = 'Senac2021'
database = 'cliente'

# Criar a conexão com o servidor MySQL
connection = mysql.connector.connect(
    host=host,
    user=user,
    password=password
)

# Criar o cursor para executar comandos SQL
cursor = connection.cursor()

# Criar o banco de dados (se não existir)
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
print(f"A database '{database}' foi criada com sucesso!")

# Fechar o cursor e a conexão temporariamente
cursor.close()
connection.close()

# Configurar o engine para incluir o nome do banco de dados
engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{database}')

# Criar uma sessão
Session = sessionmaker(bind=engine)
session = Session()

# Declarar a base
Base = declarative_base()

# Definir a classe Projeto
class Projeto(Base):
    __tablename__ = 'projeto'

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(String(200))
    data_inicio = Column(DateTime, default=datetime.now)
    data_conclusao = Column(DateTime)
    status = Column(String(20))

    tarefas = relationship('Tarefa', back_populates='projeto')

# Definir a classe Tarefa
class Tarefa(Base):
    __tablename__ = 'tarefa'

    id = Column(Integer, primary_key=True)
    titulo = Column(String(100), nullable=False)
    descricao = Column(String(200))
    status = Column(String(20))

    projeto_id = Column(Integer, ForeignKey('projeto.id'))
    projeto = relationship('Projeto', back_populates='tarefas')

# Criar o banco de dados (se não existir)
Base.metadata.create_all(engine, checkfirst=True)