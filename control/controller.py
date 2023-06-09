from sqlalchemy.orm import sessionmaker
from model.Model import Projeto
#Aqui estão definidos os métods de Commit, Update e Delete do SQL-ALCHMEY



class ProjetoController:
    def __init__(self, engine):
        self.engine = engine
        self.Session = sessionmaker(bind=self.engine)

    def adicionar_projeto(self, nome, descricao, data_inicio, data_conclusao, status):
        session = self.Session()
        projeto = Projeto(nome=nome, descricao=descricao, data_inicio=data_inicio, data_conclusao=data_conclusao,
                          status=status)
        session.add(projeto)
        session.commit()
        session.close()
        return projeto

    def listar_projetos(self):
        session = self.Session()
        projetos = session.query(Projeto).all()
        session.close()
        return projetos

    def criar_projeto(self, nome, descricao):
        session = self.Session()
        projeto = Projeto(nome=nome, descricao=descricao)
        session.add(projeto)
        session.commit()
        session.close()

    def atualizar_projeto(self, projeto_id, nome, descricao):
        session = self.Session()
        projeto = session.query(Projeto).get(projeto_id)
        if projeto:
            projeto.nome = nome
            projeto.descricao = descricao
            session.commit()
        session.close()

    def excluir_projeto(self, projeto_id):
        session = self.Session()
        projeto = session.query(Projeto).get(projeto_id)
        if projeto:
            session.delete(projeto)
            session.commit()
        session.close()
        return projeto

    def buscar_projeto_por_id(self, projeto_id):
        session = self.Session()
        projeto = session.query(Projeto).get(projeto_id)
        session.close()
        return projeto

    def editar_projeto(self, projeto_id, nome, descricao, data_inicio, data_conclusao, status):
        session = self.Session()
        projeto = session.query(Projeto).get(projeto_id)
        if projeto:
            projeto.nome = nome
            projeto.descricao = descricao
            projeto.data_inicio = data_inicio
            projeto.data_conclusao = data_conclusao
            projeto.status = status
            session.commit()
            session.close()
            return True
        else:
            session.close()
            return False
