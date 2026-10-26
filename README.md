# Livraria Aurora — Clean Architecture

Aplicação de livraria desenvolvida em Python com interface gráfica Tkinter. O projeto foi refatorado da arquitetura multicamadas para Clean Architecture.

## Funcionalidades

- Pesquisar livros por título, autor ou gênero.
- Adicionar livros à sacola e consultar o total.
- Reservar livros para retirada na loja.
- Favoritar e desfavoritar livros.
- Filtrar o catálogo para exibir apenas os favoritos.
- Salvar o catálogo e o estado dos favoritos em um arquivo TXT.

## Arquitetura

```text
application/
├── ports/
│   └── livro_repository.py
└── use_cases/
    └── bookstore_use_cases.py

model/
└── livro.py

infrastructure/
└── persistence/
    └── repositorio_livros_txt.py

controller/
└── controller.py

view/
└── view.py

main.py
