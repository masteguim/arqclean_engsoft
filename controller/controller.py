class BookstoreController:
    """Conecta a View aos casos de uso."""

    def __init__(self, casos_de_uso, view):
        self.casos_de_uso = casos_de_uso
        self.view = view
        self.apenas_favoritos = False

        self.view.definir_acoes(
            pesquisar=self.pesquisar_livros,
            adicionar=self.adicionar_a_sacola,
            reservar=self.reservar_livro,
            favorito=self.alternar_favorito,
            filtrar_favoritos=self.alternar_filtro_favoritos,
        )

        self.pesquisar_livros("")
        self.atualizar_resumo_sacola()

    def pesquisar_livros(self, consulta):
        livros = self.casos_de_uso.buscar_livros(
            consulta,
            self.apenas_favoritos,
        )
        self.view.mostrar_livros(livros)

    def alternar_filtro_favoritos(self, apenas_favoritos):
        self.apenas_favoritos = apenas_favoritos
        self.pesquisar_livros(self.view.obter_texto_pesquisa())

    def alternar_favorito(self, id_livro):
        try:
            self.casos_de_uso.alternar_favorito(id_livro)
            self.pesquisar_livros(self.view.obter_texto_pesquisa())
        except ValueError as erro:
            self.view.mostrar_erro(str(erro))

    def adicionar_a_sacola(self, id_livro):
        try:
            livro = self.casos_de_uso.adicionar_a_sacola(id_livro)
            self.atualizar_resumo_sacola()
            self.view.mostrar_informacao(
                f"{livro.titulo} foi adicionado à sacola."
            )
        except ValueError as erro:
            self.view.mostrar_erro(str(erro))

    def reservar_livro(self, id_livro, nome_cliente):
        try:
            mensagem = self.casos_de_uso.reservar_para_retirada(
                nome_cliente,
                id_livro,
            )
            self.view.mostrar_informacao(mensagem)
        except ValueError as erro:
            self.view.mostrar_erro(str(erro))

    def atualizar_resumo_sacola(self):
        quantidade, total = self.casos_de_uso.obter_resumo_sacola()
        self.view.mostrar_resumo_sacola(quantidade, total)