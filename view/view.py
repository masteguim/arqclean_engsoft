import tkinter as tk
from tkinter import messagebox, simpledialog, ttk


class BookstoreView:
    """Interface gráfica da livraria."""

    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Livraria Aurora")
        self.janela.geometry("950x700")
        self.janela.minsize(700, 500)
        self.janela.configure(bg="#faf8f4")

        self.acao_pesquisar = None
        self.acao_adicionar = None
        self.acao_reservar = None
        self.acao_favorito = None
        self.acao_filtrar_favoritos = None
        self.apenas_favoritos = False

        self._montar_layout()

    def _montar_layout(self):
        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure("TFrame", background="#faf8f4")
        estilo.configure("Card.TFrame", background="#ffffff")
        estilo.configure(
            "Title.TLabel",
            background="#f0e8dd",
            foreground="#302923",
            font=("Georgia", 23, "bold"),
        )
        estilo.configure(
            "Body.TLabel",
            background="#faf8f4",
            foreground="#45443f",
            font=("Arial", 10),
        )
        estilo.configure(
            "CardTitle.TLabel",
            background="#ffffff",
            foreground="#292923",
            font=("Georgia", 14, "bold"),
        )
        estilo.configure(
            "CardText.TLabel",
            background="#ffffff",
            foreground="#555555",
            font=("Arial", 10),
        )

        cabecalho = ttk.Frame(self.janela, padding=(22, 16))
        cabecalho.pack(fill="x")

        ttk.Label(
            cabecalho,
            text="AURORA · LIVRARIA",
            background="#faf8f4",
            foreground="#a94332",
            font=("Georgia", 16, "bold"),
        ).pack(side="left")

        ttk.Label(
            cabecalho,
            text="Seu próximo livro está aqui.",
            style="Body.TLabel",
        ).pack(side="right")

        destaque = tk.Frame(
            self.janela,
            bg="#f0e8dd",
            padx=24,
            pady=18,
        )
        destaque.pack(fill="x")

        ttk.Label(
            destaque,
            text="Histórias para descobrir.",
            style="Title.TLabel",
        ).pack(anchor="w")

        tk.Label(
            destaque,
            text="Pesquise o catálogo, favorite livros ou adicione-os à sacola.",
            bg="#f0e8dd",
            fg="#5f5d57",
            font=("Arial", 10),
        ).pack(anchor="w", pady=(6, 0))

        area_pesquisa = ttk.Frame(self.janela, padding=(22, 14, 22, 8))
        area_pesquisa.pack(fill="x")

        ttk.Label(
            area_pesquisa,
            text="Buscar por título, autor ou gênero:",
            style="Body.TLabel",
        ).pack(side="left", padx=(0, 8))

        self.campo_pesquisa = ttk.Entry(area_pesquisa, font=("Arial", 11))
        self.campo_pesquisa.pack(side="left", fill="x", expand=True)
        self.campo_pesquisa.bind("<KeyRelease>", self._ao_pesquisar)

        self.botao_favoritos = ttk.Button(
            area_pesquisa,
            text="Mostrar favoritos",
            command=self._alternar_filtro_favoritos,
        )
        self.botao_favoritos.pack(side="left", padx=(8, 0))

        area_lista = ttk.Frame(self.janela)
        area_lista.pack(
            fill="both",
            expand=True,
            padx=(22, 10),
            pady=5,
        )

        self.canvas = tk.Canvas(
            area_lista,
            bg="#faf8f4",
            highlightthickness=0,
        )
        barra_rolagem = ttk.Scrollbar(
            area_lista,
            orient="vertical",
            command=self.canvas.yview,
        )

        self.area_livros = ttk.Frame(self.canvas)
        self.janela_livros = self.canvas.create_window(
            (0, 0),
            window=self.area_livros,
            anchor="nw",
        )

        self.area_livros.bind(
            "<Configure>",
            lambda _evento: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            ),
        )
        self.canvas.bind("<Configure>", self._redimensionar_livros)
        self.canvas.configure(yscrollcommand=barra_rolagem.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        barra_rolagem.pack(side="right", fill="y")

        rodape = ttk.Frame(self.janela, padding=(22, 10, 22, 16))
        rodape.pack(fill="x")

        self.rotulo_sacola = ttk.Label(
            rodape,
            text="Sacola: 0 itens",
            style="Body.TLabel",
        )
        self.rotulo_sacola.pack(side="left")

        ttk.Label(
            rodape,
            text="Livraria Aurora · Clean Architecture",
            style="Body.TLabel",
        ).pack(side="right")

    def definir_acoes(
        self,
        pesquisar,
        adicionar,
        reservar,
        favorito,
        filtrar_favoritos,
    ):
        self.acao_pesquisar = pesquisar
        self.acao_adicionar = adicionar
        self.acao_reservar = reservar
        self.acao_favorito = favorito
        self.acao_filtrar_favoritos = filtrar_favoritos

    def _ao_pesquisar(self, _evento=None):
        if self.acao_pesquisar:
            self.acao_pesquisar(self.campo_pesquisa.get())

    def _alternar_filtro_favoritos(self):
        self.apenas_favoritos = not self.apenas_favoritos

        if self.apenas_favoritos:
            self.botao_favoritos.configure(text="Mostrar todos")
        else:
            self.botao_favoritos.configure(text="Mostrar favoritos")

        if self.acao_filtrar_favoritos:
            self.acao_filtrar_favoritos(self.apenas_favoritos)

    def _redimensionar_livros(self, evento):
        self.canvas.itemconfigure(self.janela_livros, width=evento.width)

    def obter_texto_pesquisa(self):
        return self.campo_pesquisa.get()

    def mostrar_livros(self, livros):
        for filho in self.area_livros.winfo_children():
            filho.destroy()

        if not livros:
            ttk.Label(
                self.area_livros,
                text="Nenhum livro encontrado.",
                style="Body.TLabel",
                padding=20,
            ).grid(row=0, column=0, sticky="w")
            return

        for indice, livro in enumerate(livros):
            linha = indice // 2
            coluna = indice % 2

            cartao = ttk.Frame(
                self.area_livros,
                style="Card.TFrame",
                padding=14,
            )
            cartao.grid(
                row=linha,
                column=coluna,
                sticky="nsew",
                padx=6,
                pady=6,
            )

            ttk.Label(
                cartao,
                text=livro.titulo,
                style="CardTitle.TLabel",
                wraplength=300,
            ).pack(anchor="w")

            ttk.Label(
                cartao,
                text=f"Autor: {livro.autor}",
                style="CardText.TLabel",
            ).pack(anchor="w", pady=(6, 0))

            ttk.Label(
                cartao,
                text=f"Gênero: {livro.genero}",
                style="CardText.TLabel",
            ).pack(anchor="w", pady=(3, 0))

            ttk.Label(
                cartao,
                text=f"Preço: R$ {livro.preco:.2f} · Estoque: {livro.estoque}",
                style="CardText.TLabel",
            ).pack(anchor="w", pady=(3, 8))

            botoes = ttk.Frame(cartao, style="Card.TFrame")
            botoes.pack(anchor="w")

            texto_favorito = "★ Remover favorito" if livro.favorito else "☆ Favoritar"

            ttk.Button(
                botoes,
                text=texto_favorito,
                command=lambda id_livro=livro.id: self.acao_favorito(id_livro),
            ).pack(side="left", padx=(0, 5))

            ttk.Button(
                botoes,
                text="Adicionar à sacola",
                command=lambda id_livro=livro.id: self.acao_adicionar(id_livro),
            ).pack(side="left", padx=5)

            ttk.Button(
                botoes,
                text="Reservar",
                command=lambda id_livro=livro.id: self._pedir_nome_reserva(id_livro),
            ).pack(side="left", padx=5)

        self.area_livros.columnconfigure(0, weight=1)
        self.area_livros.columnconfigure(1, weight=1)

    def _pedir_nome_reserva(self, id_livro):
        nome_cliente = simpledialog.askstring(
            "Reserva para retirada",
            "Digite seu nome:",
            parent=self.janela,
        )

        if nome_cliente is not None and self.acao_reservar:
            self.acao_reservar(id_livro, nome_cliente)

    def mostrar_resumo_sacola(self, quantidade, total):
        self.rotulo_sacola.configure(
            text=f"Sacola: {quantidade} itens · Total: R$ {total:.2f}"
        )

    def mostrar_informacao(self, mensagem):
        messagebox.showinfo(
            "Livraria Aurora",
            mensagem,
            parent=self.janela,
        )

    def mostrar_erro(self, mensagem):
        messagebox.showerror(
            "Livraria Aurora",
            mensagem,
            parent=self.janela,
        )