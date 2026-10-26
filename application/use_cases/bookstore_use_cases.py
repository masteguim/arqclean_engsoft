from application.ports.livro_repository import LivroRepository

class BookstoreUseCases:
    """Regras e casos de uso da livraria."""

    def __init__(self, repositorio: LivroRepository):
        self.repositorio = repositorio
        self.sacola = {}

    def buscar_livros(self, consulta="", apenas_favoritos=False):
        livros = self.repositorio.listar_livros()
        consulta = consulta.strip().casefold()

        if consulta:
            livros = [
                livro
                for livro in livros
                if consulta in livro.titulo.casefold()
                or consulta in livro.autor.casefold()
                or consulta in livro.genero.casefold()
            ]

        if apenas_favoritos:
            livros = [livro for livro in livros if livro.favorito]

        return livros

    def alternar_favorito(self, id_livro):
        livro = self.repositorio.obter_livro_por_id(id_livro)

        if livro is None:
            raise ValueError("Livro não encontrado.")

        return self.repositorio.alternar_favorito(id_livro)

    def adicionar_a_sacola(self, id_livro):
        livro = self.repositorio.obter_livro_por_id(id_livro)

        if livro is None:
            raise ValueError("Livro não encontrado.")

        quantidade_atual = self.sacola.get(id_livro, 0)

        if quantidade_atual >= livro.estoque:
            raise ValueError("Não há mais unidades disponíveis desse livro.")

        self.sacola[id_livro] = quantidade_atual + 1
        return livro

    def obter_resumo_sacola(self):
        quantidade = sum(self.sacola.values())
        total = 0.0

        for id_livro, quantidade_livros in self.sacola.items():
            livro = self.repositorio.obter_livro_por_id(id_livro)

            if livro is not None:
                total += livro.preco * quantidade_livros

        return quantidade, total

    def reservar_para_retirada(self, nome_cliente, id_livro):
        nome_cliente = nome_cliente.strip()
        livro = self.repositorio.obter_livro_por_id(id_livro)

        if not nome_cliente:
            raise ValueError("Digite o nome do cliente.")

        if livro is None:
            raise ValueError("Livro não encontrado.")

        if livro.estoque <= 0:
            raise ValueError("Este livro está sem estoque.")

        return (
            f"Reserva feita para {nome_cliente}: {livro.titulo}. "
            "Aguarde a confirmação da livraria."
        )