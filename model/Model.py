from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
import sqlalchemy.exc
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

# Criar a database (se não existir)
try:
    cursor.execute(f"CREATE DATABASE {database}")
    print(f"A database '{database}' foi criada com sucesso!")
except mysql.connector.Error as err:
    print(f"Erro ao criar a database: {err}")

# Fechar o cursor e a conexão temporariamente
cursor.close()
connection.close()

# Criar a conexão com o banco de dados
engine = create_engine(f'mysql://{user}:{password}@{host}/{database}')

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

    id_projeto = Column(Integer, ForeignKey('projeto.id'))
    projeto = relationship('Projeto', back_populates='tarefas')

# Criar o banco de dados (se não existir)
try:
    Base.metadata.create_all(engine)
    print("As tabelas foram criadas com sucesso!")
except sqlalchemy.exc.SQLAlchemyError as err:
    print(f"Erro ao criar as tabelas: {err}")

# Restante do código...
