from dataclasses import dataclass

@dataclass
class Livro:
    id: int
    titulo: str
    autor: str
    genero: str
    preco: float
    estoque: int
    favorito: bool = False