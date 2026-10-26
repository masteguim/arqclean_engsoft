import csv
from pathlib import Path
from application.ports.livro_repository import LivroRepository
from model.livro import Livro


class RepositorioLivrosTxt(LivroRepository):
    """Implementa o repositório usando um arquivo TXT separado por ponto e vírgula."""

    def __init__(self, caminho_arquivo=None):
        if caminho_arquivo is None:
            pasta_projeto = Path(__file__).resolve().parents[2]
            pasta_dados = pasta_projeto / "data"
            caminho_arquivo = pasta_dados / "livros.txt"

        self.caminho_arquivo = Path(caminho_arquivo)
        self.caminho_arquivo.parent.mkdir(parents=True, exist_ok=True)

        if not self.caminho_arquivo.exists() or self.caminho_arquivo.stat().st_size == 0:
            self._salvar_livros(self._catalogo_inicial())

    def listar_livros(self):
        livros = []

        try:
            with self.caminho_arquivo.open(
                "r",
                encoding="utf-8",
                newline="",
            ) as arquivo:
                leitor = csv.reader(arquivo, delimiter=";")

                for linha in leitor:
                    if len(linha) != 7:
                        continue

                    livros.append(
                        Livro(
                            id=int(linha[0]),
                            titulo=linha[1],
                            autor=linha[2],
                            genero=linha[3],
                            preco=float(linha[4]),
                            estoque=int(linha[5]),
                            favorito=linha[6] == "1",
                        )
                    )

        except (OSError, ValueError):
            return []

        return livros

    def obter_livro_por_id(self, id_livro):
        for livro in self.listar_livros():
            if livro.id == id_livro:
                return livro
        return None

    def alternar_favorito(self, id_livro):
        livros = self.listar_livros()

        for livro in livros:
            if livro.id == id_livro:
                livro.favorito = not livro.favorito
                self._salvar_livros(livros)
                return livro.favorito

        raise ValueError("Livro não encontrado.")

    def _salvar_livros(self, livros):
        with self.caminho_arquivo.open(
            "w",
            encoding="utf-8",
            newline="",
        ) as arquivo:
            escritor = csv.writer(arquivo, delimiter=";")

            for livro in livros:
                escritor.writerow(
                    [
                        livro.id,
                        livro.titulo,
                        livro.autor,
                        livro.genero,
                        f"{livro.preco:.2f}",
                        livro.estoque,
                        "1" if livro.favorito else "0",
                    ]
                )

    @staticmethod
    def _catalogo_inicial():
        return [
            Livro(1, "Dom Casmurro", "Machado de Assis", "Romance", 34.90, 8),
            Livro(2, "O Hobbit", "J. R. R. Tolkien", "Fantasia", 49.90, 5),
            Livro(3, "1984", "George Orwell", "Ficção", 39.90, 7),
            Livro(4, "Orgulho e Preconceito", "Jane Austen", "Romance", 42.50, 4),
            Livro(5, "A Revolução dos Bichos", "George Orwell", "Ficção", 29.90, 9),
            Livro(6, "O Pequeno Príncipe", "Antoine de Saint-Exupéry", "Infantil", 24.90, 6),
        ]