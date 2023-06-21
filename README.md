Trabalho Final da Disciplina Desenvolvimento Desktop
Criação de um Sistema de Gestão de Projetos
O objetivo deste trabalho é desenvolver um sistema de gestão de projetos que permita a realização das operações CRUD (Create, Read, Update, Delete) e a definição do status de cada projeto.

Exercício 5: Sistema de Gerenciamento de Projetos
Requisitos Funcionais:
Criar, visualizar, atualizar e excluir projetos.
Cada projeto deve ter um nome, descrição, data de início e data de conclusão.
Cada projeto pode ter várias tarefas associadas.
Requisitos Não Funcionais:
Organização dos projetos por status (em andamento, concluído, etc.).
DER (Diagrama Entidade-Relacionamento):
Tabela "Projeto" com os campos:

ID (chave primária)
Nome
Descrição
Data de início
Data de conclusão
Status
Tabela "Tarefa" com os campos:

ID (chave primária)
Título
Descrição
Status
ID_Projeto (chave estrangeira para a tabela "Projeto")
Telas:
Tela de Lista de Projetos:

Exibe a lista de todos os projetos.
Permite a visualização, edição e exclusão de projetos.
Tela de Detalhes do Projeto:

Mostra as informações detalhadas de um projeto selecionado.
Permite a edição, exclusão e gerenciamento das tarefas associadas ao projeto.
