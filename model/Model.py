from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

# Criar a conexão com o banco de dados
engine = create_engine('mysql://root:Senac2021@localhost/cliente')

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
Base.metadata.create_all(engine)



