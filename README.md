Trabalho Final da Disciplina Desenvolvimento Desktop
# Criação de um Sistema de Gestão de Projetos, aonde é possível realizar o CRUD e colocar o status do projeto

# Exercício 1: Sistema de Gerenciamento de Tarefas
Requisitos Funcionais:
● Criar, visualizar, atualizar e excluir tarefas.
● Cada tarefa deve ter um título, descrição e status.
Cada tarefa pode ter vários comentários associados.
● Requisitos Não Funcionais:
Interface intuitiva e de fácil utilização.
● DER:
● Tabela "Tarefa" com os campos:
● ID (chave primária)
● Título
● Descrição
● Status
● ID_Comentário (chave estrangeira para a tabela "Comentário")
● Tabela "Comentário" com os campos:
● ID (chave primária)
● Texto
● ID_Tarefa (chave estrangeira para a tabela "Tarefa")
Telas:
● Tela de Lista de Tarefas: Mostra todas as tarefas existentes em forma de
lista, permitindo a visualização, edição e exclusão.
● Tela de Detalhes da Tarefa: Exibe os detalhes de uma tarefa selecionada,
permitindo a edição, exclusão e adição de comentários.
