from datetime import date
from PySide6.QtCore import Qt, QDate
from PySide6.QtWidgets import (
    QDialog,
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
    QMessageBox,
    QDateEdit,
    QDialogButtonBox,
)
from PySide6.QtWidgets import QSizePolicy


class CustomDateEdit(QDateEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCalendarPopup(True)

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


class TelaPrincipal(QDialog):
    def __init__(self, projeto_controller):
        super().__init__()
        self.setMinimumSize(500, 900)

        self.projeto_controller = projeto_controller

        self.setWindowTitle("Lista de Projetos")
        self.setModal(True)

        self.layout = QVBoxLayout()

        self.label_titulo = QLabel("Lista de Projetos")
        self.label_titulo.setObjectName("titulo")
        self.layout.addWidget(self.label_titulo)

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


    def carregar_projetos(self):
        self.setMinimumSize(1000, 1000)
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

    def confirmar_editar_projeto(self, dialog, id_projeto, nome, descricao, data_inicio, data_conclusao, status):
        if self.projeto_controller.editar_projeto(id_projeto, nome, descricao, data_inicio, data_conclusao, status):
            dialog.accept()
            QMessageBox.information(self, "Sucesso", "Projeto editado com sucesso.")
            self.carregar_projetos()
        else:
            QMessageBox.warning(self, "Erro", "Falha ao editar projeto.")

    def excluir_projeto(self):
        selected_rows = self.table_widget.selectionModel().selectedRows()

        if len(selected_rows) != 1:
            QMessageBox.warning(self, "Erro", "Selecione um projeto para excluir.")
            return

        confirm = QMessageBox.question(
            self, "Confirmação", "Tem certeza que deseja excluir o projeto selecionado?", QMessageBox.Yes | QMessageBox.No
        )

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
