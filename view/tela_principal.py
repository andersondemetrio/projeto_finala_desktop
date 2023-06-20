from datetime import date
from PySide6.QtCore import QDate
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel, QFrame, QVBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QPushButton
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLineEdit,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView,
    QFormLayout,
    QMessageBox,
    QDateEdit,
    QDialogButtonBox,
)


# Criação de classe específica para os Calendários nas datas.
class CustomDateEdit(QDateEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCalendarPopup(True)

    # Criação de método específico para a requisição da data
    def setDate(self, date):
        qt_date = QDate(date.year, date.month, date.day)
        super().setDate(qt_date)

    def date(self):
        qt_date = super().date()
        return date(qt_date.year(), qt_date.month(), qt_date.day())


class StatusTableWidgetItem(QTableWidgetItem):
    def __init__(self, status):
        super().__init__(status)

    def __lt__(self, other):
        # Personaliza a ordenação para exibir corretamente o campo de "Status"
        return self.text() < other.text()


# Tela de Boas Vindas, Widget Inicial

class TelaBoasVindas(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Boas-vindas")
        self.setModal(True)

        layout = QVBoxLayout()

        label_titulo = QLabel("Bem-vindo(a) à aplicação de Projetos!")
        label_titulo.setObjectName("titulo")
        label_titulo.setAlignment(Qt.AlignCenter)  # Alinha ao centro horizontalmente
        layout.addWidget(label_titulo)

        label_descricao = QLabel("Esta é uma aplicação para gerenciar projetos.")
        label_descricao.setAlignment(Qt.AlignCenter)  # Alinha ao centro horizontalmente
        layout.addWidget(label_descricao)

        # Adicionar imagem centralizada
        imagem_label = QLabel()
        imagem_label.setFixedSize(250, )
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

        imagem = QPixmap(
            "C:\\Users\\leonardo.spinosa\\OneDrive - SENAC-SC\\3° Fase\\projeto_finala_desktop\\images\\teste.jpg")
        imagem_label.setPixmap(imagem)

        layout.addWidget(frame, alignment=Qt.AlignCenter)

        label_equipe = QLabel("Desenvolvedores: Anderson Demetrio, Lucas Coelho, Leonardo Spinosa")
        label_equipe.setAlignment(Qt.AlignCenter)
        layout.addWidget(label_equipe)

        button_fechar = QPushButton("Fechar")
        button_fechar.clicked.connect(self.fechar_tela)
        layout.addWidget(button_fechar)

        self.setLayout(layout)

        # Método Para expandir a tela Inteira, fica em fullscreen
        self.showFullScreen()

    # Método Para expandir a tela Inteira
    def showEvent(self, event):
        super().showEvent(event)
        self.showFullScreen()

    # método para fechar a tela de boas vindas
    def fechar_tela(self):
        self.accept()


class TelaPrincipal(QDialog):

    def __init__(self, projeto_controller):
        super().__init__()
        self.setWindowTitle("Projeto de Gerenciamento")
        self.setModal(True)

        self.setMinimumSize(850, 500)

        self.projeto_controller = projeto_controller

        self.layout = QVBoxLayout()

        self.label_titulo = QLabel("Lista de Projetos")
        self.label_titulo.setObjectName("titulo")
        self.layout.addWidget(self.label_titulo)

        self.setLayout(self.layout)

        self.exibir_tela_boas_vindas()

        # Botão de maximizar
        button_box = QDialogButtonBox(self)
        button_box.addButton("Maximizar", QDialogButtonBox.ActionRole)
        button_box.clicked.connect(self.maximizar_janela)
        self.layout.addWidget(button_box)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(6)
        self.table_widget.setHorizontalHeaderLabels(
            ["ID", "Nome", "Descrição", "Data de Início", "Data de Conclusão", "Status"])

        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.layout.addWidget(self.table_widget)

        self.button_adicionar = QPushButton("Adicionar Projeto")
        self.button_editar = QPushButton("Editar Projeto")
        self.button_excluir = QPushButton("Excluir Projeto")
        self.button_listar = QPushButton("Listar Projetos")
        self.layout_buttons = QHBoxLayout()
        self.layout_buttons.addWidget(self.button_adicionar)
        self.button_adicionar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.layout_buttons.addWidget(self.button_editar)
        self.button_editar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.layout_buttons.addWidget(self.button_excluir)
        self.button_excluir.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.layout_buttons.addWidget(self.button_listar)
        self.button_listar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.layout.addLayout(self.layout_buttons)

        self.setLayout(self.layout)

        self.button_adicionar.clicked.connect(self.adicionar_projeto)
        self.button_editar.clicked.connect(self.editar_projeto)
        self.button_excluir.clicked.connect(self.excluir_projeto)
        self.button_listar.clicked.connect(self.listar_projetos)

    def maximizar_janela(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def carregar_projetos(self):
        self.setMinimumSize(250, 250)
        projetos = self.projeto_controller.listar_projetos()

        self.table_widget.setRowCount(len(projetos))

        for row, projeto in enumerate(projetos):
            id_item = QTableWidgetItem(str(projeto.id))
            nome_item = QTableWidgetItem(projeto.nome)
            descricao_item = QTableWidgetItem(projeto.descricao)
            data_inicio_item = QTableWidgetItem(projeto.data_inicio.strftime("%d/%m/%Y") if projeto.data_inicio else "")
            data_conclusao_item = QTableWidgetItem(
                projeto.data_conclusao.strftime("%d/%m/%Y") if projeto.data_conclusao else "")
            status_item = QTableWidgetItem(projeto.status)

            self.table_widget.setItem(row, 0, id_item)
            self.table_widget.setItem(row, 1, nome_item)
            self.table_widget.setItem(row, 2, descricao_item)
            self.table_widget.setItem(row, 3, data_inicio_item)
            self.table_widget.setItem(row, 4, data_conclusao_item)
            self.table_widget.setItem(row, 5, status_item)

    def adicionar_projeto(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Adicionar Projeto")
        dialog.setModal(True)

        layout = QVBoxLayout(dialog)

        form_layout = QFormLayout()

        label_nome = QLabel("Nome:")
        line_edit_nome = QLineEdit()
        form_layout.addRow(label_nome, line_edit_nome)

        label_descricao = QLabel("Descrição:")
        line_edit_descricao = QLineEdit()
        form_layout.addRow(label_descricao, line_edit_descricao)

        label_data_inicio = QLabel("Data de Início:")
        date_edit_inicio = CustomDateEdit()
        form_layout.addRow(label_data_inicio, date_edit_inicio)

        label_data_conclusao = QLabel("Data de Conclusão:")
        date_edit_conclusao = CustomDateEdit()
        form_layout.addRow(label_data_conclusao, date_edit_conclusao)

        label_status = QLabel("Status:")
        status_input = QComboBox()
        status_input.addItems(["Em andamento", "Concluído"])
        form_layout.addRow(label_status, status_input)

        layout.addLayout(form_layout)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(
            lambda: self.confirmar_adicionar_projeto(dialog, line_edit_nome.text(), line_edit_descricao.text(),
                                                     date_edit_inicio.date(), date_edit_conclusao.date(),
                                                     status_input.currentText()))
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)

        dialog.exec()

    # Confirmação de integração de projeto
    def confirmar_adicionar_projeto(self, dialog, nome, descricao, data_inicio, data_conclusao, status):
        projeto = self.projeto_controller.adicionar_projeto(nome, descricao, data_inicio, data_conclusao, status)
        dialog.accept()
        if projeto:
            QMessageBox.information(self, "Sucesso", "Projeto adicionado com sucesso.")
            self.carregar_projetos()
        else:
            QMessageBox.warning(self, "Erro", "Falha ao adicionar projeto.")

    def editar_projeto(self):
        selected_rows = self.table_widget.selectionModel().selectedRows()

        # Tratamento de exceção caso não seja selecionado um projeto.
        if len(selected_rows) != 1:
            QMessageBox.warning(self, "Erro", "Selecione um projeto para editar.")
            return

        row = selected_rows[0].row()
        id_projeto = int(self.table_widget.item(row, 0).text())

        projeto = self.projeto_controller.buscar_projeto_por_id(id_projeto)
        if projeto:
            dialog = QDialog(self)
            dialog.setWindowTitle("Editar Projeto")
            dialog.setModal(True)

            layout = QVBoxLayout(dialog)

            form_layout = QFormLayout()

            label_nome = QLabel("Nome:")
            line_edit_nome = QLineEdit(projeto.nome)
            form_layout.addRow(label_nome, line_edit_nome)

            label_descricao = QLabel("Descrição:")
            line_edit_descricao = QLineEdit(projeto.descricao)
            form_layout.addRow(label_descricao, line_edit_descricao)

            label_data_inicio = QLabel("Data de Início:")
            date_edit_inicio = CustomDateEdit()
            date_edit_inicio.setDate(projeto.data_inicio)
            form_layout.addRow(label_data_inicio, date_edit_inicio)

            label_data_conclusao = QLabel("Data de Conclusão:")
            date_edit_conclusao = CustomDateEdit()
            date_edit_conclusao.setDate(projeto.data_conclusao)
            form_layout.addRow(label_data_conclusao, date_edit_conclusao)

            label_status = QLabel("Status:")
            status_input = QComboBox()
            status_input.addItems(["Em andamento", "Concluído"])
            form_layout.addRow(label_status, status_input)

            layout.addLayout(form_layout)

            button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
            button_box.accepted.connect(lambda: self.confirmar_editar_projeto(dialog, id_projeto, line_edit_nome.text(),
                                                                              line_edit_descricao.text(),
                                                                              date_edit_inicio.date(),
                                                                              date_edit_conclusao.date(),
                                                                              status_input.currentText()))
            button_box.rejected.connect(dialog.reject)
            layout.addWidget(button_box)

            dialog.exec()

    # Confirmação de atualização de projetos
    def confirmar_editar_projeto(self, dialog, id_projeto, nome, descricao, data_inicio, data_conclusao, status):
        if self.projeto_controller.editar_projeto(id_projeto, nome, descricao, data_inicio, data_conclusao, status):
            dialog.accept()
            QMessageBox.information(self, "Sucesso", "Projeto editado com sucesso.")
            self.carregar_projetos()
        else:
            QMessageBox.warning(self, "Erro", "Falha ao editar projeto.")

    def excluir_projeto(self):
        selected_rows = self.table_widget.selectionModel().selectedRows()

        # Tratamento de exceção, caso não seja selecionado um projeto
        if len(selected_rows) != 1:
            QMessageBox.warning(self, "Erro", "Selecione um projeto para excluir.")
            return

        # Alteração do idioma de confirmação para exclusão de projetos.
        msg = QMessageBox()
        msg.setWindowTitle('Remover projeto')
        msg.setText(f'Este projeto será removido')
        msg.setInformativeText(f'Você deseja remover o projeto ?')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.button(QMessageBox.Yes).setText('Sim')
        msg.button(QMessageBox.No).setText('Não')
        confirm = msg.exec()

        # Validação para exclusão de projetos
        if confirm == QMessageBox.Yes:
            row = selected_rows[0].row()
            id_projeto = int(self.table_widget.item(row, 0).text())

            if self.projeto_controller.excluir_projeto(id_projeto):
                QMessageBox.information(self, "Sucesso", "Projeto excluído com sucesso.")
                self.carregar_projetos()
            else:
                QMessageBox.warning(self, "Erro", "Falha ao excluir projeto.")

    def listar_projetos(self):
        self.carregar_projetos()

    def exibir_tela_boas_vindas(self):
        self.tela_boas_vindas = TelaBoasVindas()
        self.tela_boas_vindas.exec()
