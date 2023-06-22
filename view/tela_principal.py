from datetime import date, datetime
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
    QDialogButtonBox, QWidget
)
from PySide6.QtWidgets import QInputDialog

from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QPushButton, QListView, QMessageBox
from PySide6.QtGui import QStandardItemModel
from PySide6.QtCore import Qt

# Criação de classe específica para os Calendários nas datas.
class CustomDateEdit(QDateEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCalendarPopup(True)

    # Criação de método específico para a requisição da data
    def setDate(self, date):
        qt_date = QDate()
        super().setDate(qt_date.currentDate())

    def date(self):
        qt_date = super().date()
        return qt_date.currentDate()


class StatusTableWidgetItem(QTableWidgetItem):
    def __init__(self, status):
        super().__init__(status)

    def __lt__(self, other):
        # Personaliza a ordenação para exibir corretamente o campo de "Status"
        return self.text() < other.text()


# Tela de Boas Vindas, Widget Inicial
# Alterações da Classe principal
class TelaBoasVindas(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Boas-vindas")
        self.setModal(True)

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)  # Align the main layout to the center

        label_titulo = QLabel("Bem-vindo(a) à aplicação de Projetos!")
        label_titulo.setObjectName("titulo")
        label_titulo.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(label_titulo)

        label_descricao = QLabel("Esta é uma aplicação para gerenciar projetos.")
        label_descricao.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(label_descricao)

        image_layout = QHBoxLayout()
        image_layout.setAlignment(Qt.AlignCenter)  # Align the image layout to the center

        imagem_label = QLabel()
        imagem_label.setFixedSize(250, 250)
        imagem_label.setScaledContents(True)

        frame = QFrame()
        frame.setFrameStyle(QFrame.Box | QFrame.Plain)
        frame.setLineWidth(1)
        frame.setMidLineWidth(0)
        frame.setObjectName("imageFrame")
        frame.setFixedSize(imagem_label.size())
        frame_layout = QVBoxLayout()
        frame_layout.addWidget(imagem_label)
        frame.setLayout(frame_layout)

        imagem = QPixmap("C:\\Users\\anderson.placido\\PycharmProjects\\projeto_final_desktop\\images\\teste.jpg")
        imagem_label.setPixmap(imagem)

        image_layout.addWidget(frame)

        main_layout.addLayout(image_layout)


        username_widget = QWidget()  # Widget for the username
        username_layout = QVBoxLayout()
        username_layout.setAlignment(Qt.AlignCenter)  # Align the username layout to the center

        username_label = QLabel("Usuário:")
        username_label.setAlignment(Qt.AlignCenter)  # Align the label text to the center
        username_layout.addWidget(username_label)

        self.username_field = QLineEdit()
        self.username_field.setAlignment(Qt.AlignCenter)  # Align the input text to the center
        username_layout.addWidget(self.username_field)

        username_widget.setLayout(username_layout)
        main_layout.addWidget(username_widget)

        # Password field
        password_label = QLabel("Senha:")
        password_label.setAlignment(Qt.AlignCenter)  # Align the label text to the center
        main_layout.addWidget(password_label)

        self.password_field = QLineEdit()
        self.password_field.setEchoMode(QLineEdit.Password)
        self.password_field.setAlignment(Qt.AlignCenter)  # Align the input text to the center
        main_layout.addWidget(self.password_field)

        button_conectar = QPushButton("conectar")
        button_conectar.clicked.connect(self.conectar)
        main_layout.addWidget(button_conectar)

        label_equipe = QLabel("Desenvolvedores: Anderson Demetrio, Lucas Coelho, Leonardo Spinosa")
        label_equipe.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(label_equipe)


        self.setLayout(main_layout)
        self.showFullScreen()

    def showEvent(self, event):
        super().showEvent(event)
        self.showFullScreen()

    def conectar(self):
        if self.username_field.text() == "admin" and self.password_field.text() == "admin":
            self.accept()
        else:
            # Add code here for handling incorrect credentials
            print("Incorrect username or password!")

class TelaPrincipal(QDialog):

    def __init__(self, projeto_controller):
        super().__init__()
        self.setWindowTitle("Projeto de Gerenciamento")
        self.setModal(True)

        self.setMinimumSize(850, 500)

        self.projeto_controller = projeto_controller

        self.layout = QVBoxLayout()

        # Botão de maximizar
        button_box = QDialogButtonBox(self)
        button_box.addButton("Maximizar", QDialogButtonBox.ActionRole)
        button_box.clicked.connect(self.maximizar_janela)
        self.layout.addWidget(button_box)

        self.label_titulo = QLabel("Lista de Projetos")
        self.label_titulo.setObjectName("titulo")
        self.layout.addWidget(self.label_titulo)

        self.setLayout(self.layout)

        self.exibir_tela_boas_vindas()

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
        # Carrega a lista de projetos
        self.listar_projetos()


        # Tarefas
        self.table_widget_tarefas = QTableWidget()
        self.table_widget_tarefas.setColumnCount(4)
        self.table_widget_tarefas.setHorizontalHeaderLabels(["ID", "Título", "Descrição", "Status"])

        self.table_widget_tarefas.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget_tarefas.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.layout.addWidget(self.table_widget_tarefas)

        self.button_adicionar_tarefa = QPushButton("Adicionar Tarefa")
        self.layout.addWidget(self.button_adicionar_tarefa)
        self.button_adicionar_tarefa.clicked.connect(self.adicionar_tarefa)

        self.button_editar_tarefa = QPushButton("Editar Tarefa")
        self.layout.addWidget(self.button_editar_tarefa)
        self.button_editar_tarefa.clicked.connect(self.editar_tarefa)

        self.button_excluir_tarefa = QPushButton("Excluir Tarefa")
        self.layout.addWidget(self.button_excluir_tarefa)
        self.button_excluir_tarefa.clicked.connect(self.excluir_tarefa)

        self.button_exibir_tarefas = QPushButton("Exibir Tarefas")
        self.layout_buttons.addWidget(self.button_exibir_tarefas)
        self.button_exibir_tarefas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.button_exibir_tarefas.clicked.connect(self.exibir_tarefas)

        self.list_view_tarefas = QListView()
        # Configurar o modelo da lista de tarefas
        self.modelo_tarefas = QStandardItemModel()
        self.list_view_tarefas.setModel(self.modelo_tarefas)

        self.id_projeto_selecionado = None  # Inicialize o atributo id_projeto_selecionado


    def selecionar_projeto(self, projeto_id):
        self.id_projeto_selecionado = projeto_id
        self.listar_tarefas(self.id_projeto_selecionado)  # Chama a função listar_tarefas com o ID do projeto

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

        data_atual = QDate()

        label_data_inicio = QLabel("Data de Início:")
        date_edit_inicio = CustomDateEdit()
        date_edit_inicio.setDate(data_atual.currentDate())
        form_layout.addRow(label_data_inicio, date_edit_inicio)

        label_data_conclusao = QLabel("Data de Conclusão:")
        date_edit_conclusao = CustomDateEdit()
        date_edit_conclusao.setDate(data_atual.currentDate())
        form_layout.addRow(label_data_conclusao, date_edit_conclusao)

        label_status = QLabel("Status:")
        status_input = QComboBox()
        status_input.addItems(["Em andamento", "Concluído"])
        form_layout.addRow(label_status, status_input)

        layout.addLayout(form_layout)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(
            lambda: self.confirmar_adicionar_projeto(dialog, line_edit_nome.text(), line_edit_descricao.text(),
                                                     date_edit_inicio.date().toPython(),
                                                     date_edit_conclusao.date().toPython(),
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
                                                                              date_edit_inicio.date().toPython(),
                                                                              date_edit_conclusao.date().toPython(),
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

       #Ações Tarefa

    def exibir_tarefas(self):
        selected_rows = self.table_widget.selectionModel().selectedRows()

        if len(selected_rows) != 1:
            QMessageBox.warning(self, "Erro", "Selecione um projeto para exibir as tarefas.")
            return

        row = selected_rows[0].row()
        id_projeto = int(self.table_widget.item(row, 0).text())

        tarefas = self.projeto_controller.obter_tarefas_por_projeto(id_projeto)

        self.table_widget_tarefas.setRowCount(len(tarefas))
        self.table_widget_tarefas.setColumnCount(4)  # Definir o número de colunas como 4

        for row, tarefa in enumerate(tarefas):
            id_item = QTableWidgetItem(str(tarefa.id))
            titulo_item = QTableWidgetItem(tarefa.titulo)
            descricao_item = QTableWidgetItem(tarefa.descricao)  # Criar um QTableWidgetItem para o campo 'descricao'
            status_item = QTableWidgetItem(tarefa.status)  # Criar um QTableWidgetItem para o campo 'status'

            self.table_widget_tarefas.setItem(row, 0, id_item)
            self.table_widget_tarefas.setItem(row, 1, titulo_item)
            self.table_widget_tarefas.setItem(row, 2, descricao_item)  # Adicionar o item de 'descricao' na coluna 2
            self.table_widget_tarefas.setItem(row, 3, status_item)  # Adicionar o item de 'status' na coluna 3

        self.button_adicionar_tarefa.setEnabled(True)


    def adicionar_tarefa(self):
        selected_rows = self.table_widget.selectionModel().selectedRows()

        if len(selected_rows) != 1:
            QMessageBox.warning(self, "Erro", "Selecione um projeto para adicionar a tarefa.")
            return

        row = selected_rows[0].row()
        id_projeto = int(self.table_widget.item(row, 0).text())

        dialog = QDialog(self)
        dialog.setWindowTitle("Adicionar Tarefa")
        dialog.setModal(True)

        layout = QVBoxLayout(dialog)

        form_layout = QFormLayout()

        label_titulo = QLabel("Título:")
        line_edit_titulo = QLineEdit()
        form_layout.addRow(label_titulo, line_edit_titulo)

        label_projeto = QLabel("Descrição:")
        label_projeto_nome = QLabel(self.table_widget.item(row, 1).text())
        form_layout.addRow(label_projeto, label_projeto_nome)

        # Adicione uma nova linha para o campo 'Status'
        label_status = QLabel("Status:")
        combo_box_status = QComboBox()
        combo_box_status.addItem("Pendente")
        combo_box_status.addItem("Em andamento")
        combo_box_status.addItem("Concluído")
        form_layout.addRow(label_status, combo_box_status)

        layout.addLayout(form_layout)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(
            lambda: self.confirmar_adicionar_tarefa(dialog, id_projeto, line_edit_titulo.text(),
                                                    combo_box_status.currentText()))
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)

        dialog.exec()

    def confirmar_adicionar_tarefa(self, dialog, id_projeto, titulo, status):
        descricao, ok = QInputDialog.getText(self, "Descrição da Tarefa", "Digite a descrição da tarefa:")
        if ok:
            tarefa = self.projeto_controller.adicionar_tarefa(id_projeto, titulo, descricao, status)
            dialog.accept()
            if tarefa:
                QMessageBox.information(self, "Sucesso", "Tarefa adicionada com sucesso.")
                self.exibir_tarefas()
            else:
                QMessageBox.warning(self, "Erro", "Falha ao adicionar tarefa.")

    def editar_tarefa(self):
        selected_rows = self.table_widget_tarefas.selectionModel().selectedRows()

        if len(selected_rows) != 1:
            QMessageBox.warning(self, "Erro", "Selecione uma tarefa para editar.")
            return

        row = selected_rows[0].row()
        id_tarefa = int(self.table_widget_tarefas.item(row, 0).text())

        tarefa = self.projeto_controller.buscar_tarefa_por_id(id_tarefa)
        if tarefa:
            dialog = QDialog(self)
            dialog.setWindowTitle("Editar Tarefa")
            dialog.setModal(True)

            layout = QVBoxLayout(dialog)

            form_layout = QFormLayout()

            label_titulo = QLabel("Título:")
            line_edit_titulo = QLineEdit(tarefa.titulo)
            form_layout.addRow(label_titulo, line_edit_titulo)

            label_descricao = QLabel("Descrição:")
            line_edit_descricao = QLineEdit(tarefa.descricao)
            form_layout.addRow(label_descricao, line_edit_descricao)

            label_status = QLabel("Status:")
            status_input = QComboBox()
            status_input.addItems(["Em andamento", "Concluído"])
            status_input.setCurrentText(tarefa.status)
            form_layout.addRow(label_status, status_input)

            label_projeto_id = QLabel("ID do Projeto:")
            line_edit_projeto_id = QLineEdit(str(tarefa.projeto_id))
            form_layout.addRow(label_projeto_id, line_edit_projeto_id)

            layout.addLayout(form_layout)

            button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
            button_box.accepted.connect(lambda: self.confirmar_editar_tarefa(dialog, id_tarefa, line_edit_titulo.text(),
                                                                             line_edit_descricao.text(),
                                                                             status_input.currentText(),
                                                                             line_edit_projeto_id.text()))
            button_box.rejected.connect(dialog.reject)
            layout.addWidget(button_box)

            dialog.exec()

    def confirmar_editar_tarefa(self, dialog, id_tarefa, titulo, descricao, status, projeto_id):
        if self.projeto_controller.editar_tarefa(id_tarefa, titulo, descricao, status, projeto_id):
            dialog.accept()
            QMessageBox.information(self, "Sucesso", "Tarefa editada com sucesso.")
            self.exibir_tarefas()
        else:
            QMessageBox.warning(self, "Erro", "Falha ao editar tarefa.")

    def excluir_tarefa(self):
        selected_row = self.table_widget_tarefas.currentRow()
        if selected_row != -1:
            tarefa_id = int(self.table_widget_tarefas.item(selected_row, 0).text())
            tarefa = self.projeto_controller.get_tarefa(tarefa_id)

            if tarefa:
                confirm = QMessageBox.question(
                    self,
                    "Confirmação",
                    f"Tem certeza que deseja excluir a tarefa '{tarefa.titulo}'?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No,
                )

                if confirm == QMessageBox.Yes:
                    if self.projeto_controller.excluir_tarefa(tarefa_id):
                        self.exibir_tarefas()
                        QMessageBox.information(
                            self,
                            "Sucesso",
                            "Tarefa excluída com sucesso.",
                            QMessageBox.Ok,
                        )
                    else:
                        QMessageBox.warning(
                            self,
                            "Erro",
                            "Não foi possível excluir a tarefa.",
                            QMessageBox.Ok,
                        )
            else:
                QMessageBox.warning(
                    self,
                    "Erro",
                    "Tarefa não encontrada.",
                    QMessageBox.Ok,
                )
        else:
            QMessageBox.warning(
                self,
                "Erro",
                "Nenhuma tarefa selecionada.",
                QMessageBox.Ok,
            )

    def listar_tarefas(self, id_projeto):
        self.table_widget_tarefas.setRowCount(0)
        tarefas = self.projeto_controller.obter_tarefas_por_projeto(id_projeto)
        for tarefa in tarefas:
            row_position = self.table_widget_tarefas.rowCount()
            self.table_widget_tarefas.insertRow(row_position)
            self.table_widget_tarefas.setItem(row_position, 0, QTableWidgetItem(str(tarefa.id)))
            self.table_widget_tarefas.setItem(row_position, 1, QTableWidgetItem(tarefa.titulo))
            self.table_widget_tarefas.setItem(row_position, 2,
                                              QTableWidgetItem(tarefa.projeto.nome if tarefa.projeto else ""))

