from PySide6.QtWidgets import QApplication
from control.controller import ProjetoController
from view.tela_principal import TelaPrincipal
from model.Model import engine
import qdarkstyle
# Aplicação Principal que integra o MVC inteiro

if __name__ == "__main__":
    # Inicializa a aplicação do Qt
    app = QApplication([])
    # Aplicar o tema dark
    app.setStyleSheet(qdarkstyle.load_stylesheet())

    # Cria uma instância do controlador de projetos
    projeto_controller = ProjetoController(engine)

    # Cria a tela principal e passa o controlador como argumento
    lista_projetos_view = TelaPrincipal(projeto_controller)

    # Exibe a tela principal
    lista_projetos_view.show()

    # Executa o loop de eventos da aplicação
    app.exec()
