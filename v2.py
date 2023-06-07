import sys
from datetime import datetime
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QDateEdit, QCalendarWidget
from PySide6.QtWidgets import (
    QApplication,
    QSizePolicy,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView,
    QFormLayout,
    QDialog,
    QMessageBox, QFrame,

)
import qdarkstyle
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import qdarkstyle

# Criar a conexão com o banco de dados
engine = create_engine('mysql://root:Senac2021@localhost/projeto')

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

class ProjetoController:
    def __init__(self):
        self.projetos = []

    def carregar_projetos(self):
        self.projetos = session.query(Projeto).all()

    def listar_projetos(self):
        return session.query(Projeto).all()

    def adicionar_projeto(self, nome, descricao, data_inicio, data_conclusao, status):
        projeto = Projeto(
            nome=nome,
            descricao=descricao,
            data_inicio=data_inicio,
            data_conclusao=data_conclusao,
            status=status
        )
        session.add(projeto)
        session.commit()

    def editar_projeto(self, projeto_id, nome, descricao, data_inicio, data_conclusao, status):
        projeto = session.query(Projeto).get(projeto_id)
        if projeto:
            projeto.nome = nome
            projeto.descricao = descricao
            projeto.data_inicio = data_inicio
            projeto.data_conclusao = data_conclusao
            projeto.status = status
            session.commit()

    def excluir_projeto(self, projeto_id):
        projeto = session.query(Projeto).get(projeto_id)
        if projeto:
            session.delete(projeto)
            session.commit()

class CustomDateEdit(QDateEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setCalendarPopup(True)
        self.setCalendarWidget(QCalendarWidget())

    def setText(self, param):
        pass


class ListaProjetosView(QDialog):
    def __init__(self, projeto_controller):
        super().__init__()

        self.projeto_controller = projeto_controller
        self.setMinimumSize(900, 900)

        self.setWindowTitle("Lista de Projetos")

        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Nome", "Descrição", "Data de Início", "Data de Conclusão", "Status"]
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.cellDoubleClicked.connect(self.editar_projeto)

        layout.addWidget(self.table)

        btn_layout = QHBoxLayout()

        self.btn_editar = QPushButton("Editar")
        self.btn_editar.clicked.connect(self.editar_projeto)
        self.btn_excluir = QPushButton("Excluir")
        self.btn_excluir.clicked.connect(self.excluir_projeto)
        self.btn_fechar = QPushButton("Fechar")
        self.btn_fechar.clicked.connect(self.close)

        btn_layout.addWidget(self.btn_editar)
        btn_layout.addWidget(self.btn_excluir)
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_fechar)

        layout.addLayout(btn_layout)

        self.setLayout(layout)

        self.carregar_projetos()

    def carregar_projetos(self):
        projetos = self.projeto_controller.listar_projetos()

        self.table.setRowCount(len(projetos))

        for row, projeto in enumerate(projetos):
            self.table.setItem(row, 0, QTableWidgetItem(str(projeto.id)))
            self.table.setItem(row, 1, QTableWidgetItem(projeto.nome))
            self.table.setItem(row, 2, QTableWidgetItem(projeto.descricao))
            self.table.setItem(
                row,
                3,
                QTableWidgetItem(
                    projeto.data_inicio.strftime("%d/%m/%Y") if projeto.data_inicio else ""
                ),
            )
            self.table.setItem(
                row,
                4,
                QTableWidgetItem(
                    projeto.data_conclusao.strftime("%d/%m/%Y") if projeto.data_conclusao else ""
                ),
            )
            self.table.setItem(row, 5, QTableWidgetItem(projeto.status))


    def editar_projeto(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            projeto_id = int(self.table.item(selected_row, 0).text())
            self.close()
            self.editar_projeto_view = EditarProjetoView(
                self.projeto_controller, projeto_id, self
            )
            self.editar_projeto_view.show()

    def excluir_projeto(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            projeto_id = int(self.table.item(selected_row, 0).text())
            projeto_nome = self.table.item(selected_row, 1).text()

            reply = QMessageBox.question(
                self,
                "Excluir Projeto",
                f"Tem certeza de que deseja excluir o projeto '{projeto_nome}'?",
                QMessageBox.Yes | QMessageBox.No,
            )

            if reply == QMessageBox.Yes:
                self.projeto_controller.excluir_projeto(projeto_id)
                self.carregar_projetos()

class EditarProjetoView(QDialog):
    def __init__(self, projeto_controller, projeto_id=None, parent=None):
        super().__init__(parent)

        self.projeto_controller = projeto_controller
        self.projeto_id = projeto_id

        if self.projeto_id:
            self.setWindowTitle("Editar Projeto")
        else:
            self.setWindowTitle("Adicionar Projeto")

        layout = QVBoxLayout()

        form_layout = QFormLayout()

        self.nome_input = QLineEdit()
        self.descricao_input = QLineEdit()
        #self.data_inicio_input = QLineEdit()
       # self.data_inicio_input = QDateEdit()
        #self.data_inicio_input = QDateEdit()  # Substitui o QLineEdit pelo QDateEdit
        #self.data_conclusao_input = QDateEdit()
        # self.data_conclusao_input = QLineEdit()
        self.data_inicio_input = CustomDateEdit()
        self.data_conclusao_input = CustomDateEdit()

        self.status_input = QComboBox()
        self.status_input.addItems(["Em andamento", "Concluído"])

        form_layout.addRow(QLabel("Nome:"), self.nome_input)
        form_layout.addRow(QLabel("Descrição:"), self.descricao_input)
        form_layout.addRow(QLabel("Data de Início:"), self.data_inicio_input)
        form_layout.addRow(QLabel("Data de Conclusão:"), self.data_conclusao_input)
        form_layout.addRow(QLabel("Status:"), self.status_input)

        layout.addLayout(form_layout)

        btn_layout = QHBoxLayout()

        self.btn_salvar = QPushButton("Salvar")
        self.btn_salvar.clicked.connect(self.salvar_projeto)
        self.btn_salvar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.btn_cancelar = QPushButton("Cancelar")
        self.btn_cancelar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.btn_cancelar.clicked.connect(self.close)

        btn_layout.addWidget(self.btn_salvar)
        btn_layout.addWidget(self.btn_cancelar)

        layout.addLayout(btn_layout)

        self.setLayout(layout)

        if self.projeto_id:
            self.carregar_projeto()
        else:
            #self.data_inicio_input.setText(datetime.now().strftime("%d/%m/%Y"))
            self.data_inicio_input.setDate(datetime.now().date())

    def carregar_projeto(self):
        projeto = session.query(Projeto).get(self.projeto_id)
        if projeto:
            self.nome_input.setText(projeto.nome)
            self.descricao_input.setText(projeto.descricao)
            self.data_inicio_input.setText(
                projeto.data_inicio.strftime("%d/%m/%Y") if projeto.data_inicio else ""
            )
            self.data_conclusao_input.setText(
                projeto.data_conclusao.strftime("%d/%m/%Y") if projeto.data_conclusao else ""
            )
            self.status_input.setCurrentText(projeto.status)

    def salvar_projeto(self):
        nome = self.nome_input.text()
        descricao = self.descricao_input.text()
        data_inicio = datetime.strptime(self.data_inicio_input.text(), "%d/%m/%Y")
        data_conclusao = (
            datetime.strptime(self.data_conclusao_input.text(), "%d/%m/%Y")
            if self.data_conclusao_input.text()
            else None
        )
        status = self.status_input.currentText()

        if self.projeto_id:
            self.projeto_controller.editar_projeto(
                self.projeto_id, nome, descricao, data_inicio, data_conclusao, status
            )
        else:
            self.projeto_controller.adicionar_projeto(
                nome, descricao, data_inicio, data_conclusao, status
            )

        mensagem_box = QMessageBox()
        mensagem_box.setWindowTitle("Sucesso")
        mensagem_box.setText("Projeto salvo com sucesso.")
        mensagem_box.setIcon(QMessageBox.Information)
        mensagem_box.setStandardButtons(QMessageBox.Ok)
        mensagem_box.exec()


        self.close()


class MainWindow(QMainWindow):
    def __init__(self, projeto_controller):
        super().__init__()

        self.projeto_controller = projeto_controller
        self.setMinimumSize(500, 900)


        self.setWindowTitle("Gerenciador de Projetos")
        self.setCentralWidget(QWidget())

        layout = QVBoxLayout()

        self.btn_adicionar_projeto = QPushButton("Adicionar Projeto")
        self.btn_adicionar_projeto.clicked.connect(self.adicionar_projeto)
        self.btn_adicionar_projeto.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.btn_listar_projetos = QPushButton("Listar Projetos")
        self.btn_listar_projetos.clicked.connect(self.listar_projetos)
        self.btn_listar_projetos.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        layout.addWidget(self.btn_adicionar_projeto)
        layout.addWidget(self.btn_listar_projetos)
        layout.setAlignment(Qt.AlignCenter)

        self.centralWidget().setLayout(layout)

        # ...

        imagem_label = QLabel()
        imagem_label.setFixedSize(250, 450)
        imagem_label.setScaledContents(True)

        frame = QFrame()
        frame.setFrameStyle(QFrame.Box | QFrame.Plain)
        frame.setLineWidth(1)
        frame.setMidLineWidth(0)
        frame.setObjectName("imageFrame")  # Define um nome para o QFrame (opcional)
        frame.setFixedSize(imagem_label.size())  # Define o tamanho do QFrame com base no tamanho da imagem
        frame_layout = QVBoxLayout()
        frame_layout.addWidget(imagem_label)
        frame.setLayout(frame_layout)

        imagem = QPixmap("C:\\Users\\anderson.placido\\PycharmProjects\\projeto_final_desktop\\teste.jpg")
        imagem_label.setPixmap(imagem)

        layout.addWidget(frame, alignment=Qt.AlignCenter)

        self.centralWidget().setLayout(layout)




    def adicionar_projeto(self):

        self.adicionar_projeto_view = EditarProjetoView(self.projeto_controller)
        self.adicionar_projeto_view.show()

    def listar_projetos(self):
        self.listar_projetos_view = ListaProjetosView(self.projeto_controller)
        self.listar_projetos_view.show()

if __name__ == '__main__':
    Base.metadata.create_all(engine)

    projeto_controller = ProjetoController()

    app = QApplication(sys.argv)

    # Aplicar o tema dark
    app.setStyleSheet(qdarkstyle.load_stylesheet())

    window = MainWindow(projeto_controller)
    window.show()

    sys.exit(app.exec())
