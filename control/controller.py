from sqlalchemy.orm import sessionmaker
from model.Model import Projeto, Tarefa
from sqlalchemy.orm import joinedload

#Aqui estão definidos os métods de Commit, Update e Delete do SQL-ALCHMEY

class ProjetoController:
    def __init__(self, engine):
        self.engine = engine
        self.Session = sessionmaker(bind=self.engine)

        self.projetos = []
        self.tarefas = []

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

    def adicionar_tarefa(self, projeto_id, titulo, descricao, status):
        session = self.Session()
        projeto = session.query(Projeto).get(projeto_id)
        if projeto:
            tarefa = Tarefa(titulo=titulo, descricao=descricao, status=status)
            projeto.tarefas.append(tarefa)
            self.tarefas.append(tarefa)  # Adicionar a tarefa à lista do controlador
            session.commit()
            session.close()
            return tarefa
        else:
            session.close()
            return None

    def obter_tarefas_por_projeto(self, id_projeto):
        session = self.Session()
        projeto = session.query(Projeto).get(id_projeto)

        if projeto is None:
            session.close()
            return []

        tarefas = session.query(Tarefa).filter(Tarefa.projeto_id == id_projeto).options(
            joinedload(Tarefa.projeto)).all()
        session.close()

        return tarefas

    def editar_tarefa(self, tarefa_id, titulo, descricao, status, projeto_id):
        session = self.Session()
        tarefa = session.query(Tarefa).get(tarefa_id)

        if tarefa:
            tarefa.titulo = titulo
            tarefa.descricao = descricao
            tarefa.status = status  # Atualizar o campo status da tarefa

            projeto = session.query(Projeto).get(projeto_id)
            if projeto:
                tarefa.projeto = projeto
            else:
                tarefa.projeto = None

            session.commit()
            session.close()
            return True
        else:
            session.close()
            return False
    def excluir_tarefa(self, id):
        session = self.Session()
        tarefa = session.query(Tarefa).get(id)
        if tarefa:
            session.delete(tarefa)

            session.commit()
        session.close()

        return tarefa

    def get_tarefa(self, tarefa_id):
        session = self.Session()
        tarefa = session.query(Tarefa).get(tarefa_id)
        session.close()
        return tarefa

    def buscar_tarefa_por_id(self, id_tarefa):
        session = self.Session()
        tarefa = session.query(Tarefa).get(id_tarefa)
        session.close()
        return tarefa





