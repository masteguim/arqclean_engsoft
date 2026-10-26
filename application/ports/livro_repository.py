from abc import ABC, abstractmethod
from model.livro import Livro

class LivroRepository(ABC):
    """Contrato para qualquer forma de armazenamento dos livros."""

    @abstractmethod
    def listar_livros(self) -> list[Livro]:
        pass

    @abstractmethod
    def obter_livro_por_id(self, id_livro: int) -> Livro | None:
        pass

    @abstractmethod
    def alternar_favorito(self, id_livro: int) -> bool:
        pass