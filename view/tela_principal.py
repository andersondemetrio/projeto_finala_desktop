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
        self.table_widget.setColumnCount(6)  # Alterado para 6 colunas
        self.table_widget.setHorizontalHeaderLabels(
            ["ID", "Nome", "Descrição", "Data de Início", "Data de Conclusão", "Status"]  # Adicionado "Status"
        )
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.layout.addWidget(self.table_widget)

        self.button_adicionar = QPushButton("Adicionar Projeto")
        self.button_editar = QPushButton("Editar Projeto")
        self.button_excluir = QPushButton("Excluir Projeto")
        self.button_listar = QPushButton("Listar Projetos")
        self.layout_buttons = QHBoxLayout()
        self.layout_buttons.addWidget(self.button_adicionar)
        self.layout_buttons.addWidget(self.button_editar)
        self.layout_buttons.addWidget(self.button_excluir)
        self.layout_buttons.addWidget(self.button_listar)
        self.layout.addLayout(self.layout_buttons)

        self.setLayout(self.layout)

        self.button_adicionar.clicked.connect(self.adicionar_projeto)
        self.button_editar.clicked.connect(self.editar_projeto)
        self.button_excluir.clicked.connect(self.excluir_projeto)
        self.button_listar.clicked.connect(self.listar_projetos)

    def carregar_projetos(self):
        self.table_widget.clearContents()
        self.table_widget.setRowCount(0)

        projetos = self.projeto_controller.listar_projetos()

        for projeto in projetos:
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)

            id_item = QTableWidgetItem(str(projeto.id))
            nome_item = QTableWidgetItem(projeto.nome)
            descricao_item = QTableWidgetItem(projeto.descricao)
            data_inicio_item = QTableWidgetItem(projeto.data_inicio.strftime("%d/%m/%Y"))
            data_conclusao_item = QTableWidgetItem(
                projeto.data_conclusao.strftime("%d/%m/%Y") if projeto.data_conclusao else ""
            )
            status_item = QTableWidgetItem(projeto.status)  # Adicionado o item para o campo de status

            self.table_widget.setItem(row_position, 0, id_item)
            self.table_widget.setItem(row_position, 1, nome_item)
            self.table_widget.setItem(row_position, 2, descricao_item)
            self.table_widget.setItem(row_position, 3, data_inicio_item)
            self.table_widget.setItem(row_position, 4, data_conclusao_item)
            self.table_widget.setItem(row_position, 5, status_item)  # Adicionado o item para o campo de status

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

        label_status = QLabel("Status:")  # Adicionado o label para o campo de status
        status_input = QComboBox()  # Criado o combo box para o campo de status
        status_input.addItems(["Em andamento", "Concluído"])  # Adicionado os itens ao combo box
        form_layout.addRow(label_status, status_input)  # Adicionado o label e o combo box ao formulário

        layout.addLayout(form_layout)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)

        if dialog.exec() == QDialog.Accepted:
            nome = line_edit_nome.text()
            descricao = line_edit_descricao.text()
            data_inicio = date_edit_inicio.date()
            data_conclusao = date_edit_conclusao.date() if date_edit_conclusao.date() else None
            status = status_input.currentText()  # Obtém o valor selecionado no combo box

            projeto = self.projeto_controller.adicionar_projeto(nome, descricao, data_inicio, data_conclusao)

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
            button_box.accepted.connect(dialog.accept)
            button_box.rejected.connect(dialog.reject)
            layout.addWidget(button_box)

            if dialog.exec() == QDialog.Accepted:
                nome = line_edit_nome.text()
                descricao = line_edit_descricao.text()
                data_inicio = date_edit_inicio.date()
                data_conclusao = date_edit_conclusao.date() if date_edit_conclusao.date() else None
                status = status_input.currentText()

                if self.projeto_controller.editar_projeto(id_projeto, nome, descricao, data_inicio, data_conclusao):

                    QMessageBox.information(self, "Sucesso", "Projeto editado com sucesso.")
                    self.carregar_projetos()
                else:
                    QMessageBox.warning(self, "Erro", "Falha ao editar projeto.")
        else:
            QMessageBox.warning(self, "Erro", "Projeto não encontrado.")

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
