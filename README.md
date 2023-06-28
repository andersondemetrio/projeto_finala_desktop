# Trabalho Final da Disciplina Desenvolvimento Desktop
# Criação de um Sistema de Gestão de Projetos
# Equipe de Desenvolvedores
# Anderson Demetrio, Lucas Coelho, Leonardo Spinosa
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


# Para realizar a instalação configure os passoas abaixo e siga os requisitos

Tenha o docker, dbeaver em sua estação.

Comando Docker
Link download Docker
https://docs.docker.com/get-docker/
docker run --name mi_mysql -e MYSQL_ROOT_PASSWORD=Senac2021 -p 3306:3306 -d mysql

Link Download Dbeavear
https://dbeaver.io/download/

Python 3.10 ou Superior
https://www.python.org/downloads/

Recomendados Usar Ambiente Virtual, por padrão o Pycharm (IDE Python, já realiza essas configurações de criação de ambiente virtual) 
Faça a instalação das dependências do projeto com o comando 
pip install -r requirements.txt

Se preferir usuar outra IDE, Faça a criação de um ambiente virtual
python -m venv venv
ou clone o repositório usando o comando git clone link_repositório

pip install -r requirements.txt


# DER
# Diagrama Entidade-Relacionamento

## Tabelas

### Projeto

- ID (chave primária)
- Nome
- Descrição
- Data Início
- Data Conclusão
- Status

### Tarefa

- ID (chave primária)
- Título
- Descrição
- Status
- Projeto_ID (chave estrangeira, referenciando Projeto.ID)



