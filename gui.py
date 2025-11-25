import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from typing import Optional

from quest1_AFD import *
from automata_protocol import *

class SimuladorAFD:
    """Interface gráfica para simulação de AFD"""

    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Autômato Finito Determinístico (AFD)")
        self.root.geometry("1000x800")

        # Variável para armazenar o automato atual
        self.automata: Optional[Automata] = None

        self.criar_interface()

    def criar_interface(self):
        """Cria os componentes da interface gráfica"""

        # Frame principal
        main_frame = ttk.Frame(self.root, padding=(10))
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Título
        titulo = ttk.Label(main_frame, text="Simulador de AFD", font=("Arial", 16, "bold"))
        titulo.grid(row=0, column=0, columnspan=2, pady=10)

        # Frame de entrada do AFD
        self.criar_frame_entrada_afd(main_frame)

        # Frame de simulação
        self.criar_frame_simulacao(main_frame)

        # Frame de resultado
        self.criar_frame_resultado(main_frame)

        # Configurar redimensionamento
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        self.root.bind('<Escape>', lambda event: self.root.destroy())

    def criar_frame_entrada_afd(self, parent):
        """Cria o frame para entrada da definição do AFD"""
        frame = ttk.LabelFrame(parent, text="Definir AFD", padding="10")
        frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        # Estados
        ttk.Label(frame, text="Estados (separados por vírgula):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entrada_estados = ttk.Entry(frame, width=50)
        self.entrada_estados.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        self.entrada_estados.insert(0, "q0,q1,q2")

        # Alfabeto
        ttk.Label(frame, text="Alfabeto (separado por vírgula):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entrada_alfabeto = ttk.Entry(frame, width=50)
        self.entrada_alfabeto.grid(row=1, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        self.entrada_alfabeto.insert(0, "0,1")

        # Estado inicial
        ttk.Label(frame, text="Estado Inicial:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.entrada_estado_inicial = ttk.Entry(frame, width=50)
        self.entrada_estado_inicial.grid(row=2, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        self.entrada_estado_inicial.insert(0, "q0")

        # Estados finais
        ttk.Label(frame, text="Estados Finais (separados por vírgula):").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.entrada_estados_finais = ttk.Entry(frame, width=50)
        self.entrada_estados_finais.grid(row=3, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        self.entrada_estados_finais.insert(0, "q2")

        # Transições
        ttk.Label(frame, text="Transições (formato: estado,simbolo,destino):").grid(row=4, column=0, sticky=tk.W,
                                                                                    pady=5)
        self.entrada_transicoes = scrolledtext.ScrolledText(frame, height=6, width=50, wrap=tk.WORD)
        self.entrada_transicoes.grid(row=4, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        self.entrada_transicoes.insert(1.0, "q0,0,q1\nq0,1,q0\nq1,0,q1\nq1,1,q2\nq2,0,q1\nq2,1,q0")

        # Botões
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)

        ttk.Button(btn_frame, text="Criar AFD", command=self.criar_afd).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Exemplo 1 (termina em 01)", command=self.carregar_exemplo1).pack(side=tk.LEFT,
                                                                                                     padx=5)
        ttk.Button(btn_frame, text="Exemplo 2 (número par de 0s)", command=self.carregar_exemplo2).pack(side=tk.LEFT,
                                                                                                        padx=5)

        frame.columnconfigure(1, weight=1)

    def criar_frame_simulacao(self, parent):
        """Cria o frame para entrada e simulação"""
        frame = ttk.LabelFrame(parent, text="Simulação", padding="10")
        frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        # Label e entrada de cadeia
        ttk.Label(frame, text="Digite a cadeia:").grid(row=0, column=0, sticky=tk.W, pady=5)

        self.entrada_cadeia = ttk.Entry(frame, width=40, font=("Arial", 12))
        self.entrada_cadeia.grid(row=0, column=1, padx=5, pady=5)
        self.entrada_cadeia.bind('<Return>', lambda e: self.simular())

        # Botão simular
        btn_simular = ttk.Button(frame, text="Simular", command=self.simular)
        btn_simular.grid(row=0, column=2, padx=5, pady=5)

        # Botão limpar
        btn_limpar = ttk.Button(frame, text="Limpar", command=self.limpar)
        btn_limpar.grid(row=0, column=3, padx=5, pady=5)

    def criar_frame_resultado(self, parent):
        """Cria o frame para exibir o resultado da simulação"""
        frame = ttk.LabelFrame(parent, text="Resultado da Simulação", padding="10")
        frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)

        # Área de texto para histórico
        self.resultado_text = scrolledtext.ScrolledText(frame, height=8, width=80, wrap=tk.WORD)
        self.resultado_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Tags para colorir o texto
        self.resultado_text.tag_config("aceita", foreground="green", font=("Arial", 12, "bold"))
        self.resultado_text.tag_config("rejeita", foreground="red", font=("Arial", 12, "bold"))
        self.resultado_text.tag_config("titulo", font=("Arial", 11, "bold"))
        self.resultado_text.tag_config("passo", foreground="blue")

        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

    def carregar_exemplo1(self):
        """Carrega exemplo de AFD que aceita cadeias terminadas em '01'"""
        self.entrada_estados.delete(0, tk.END)
        self.entrada_estados.insert(0, "q0,q1,q2")

        self.entrada_alfabeto.delete(0, tk.END)
        self.entrada_alfabeto.insert(0, "0,1")

        self.entrada_estado_inicial.delete(0, tk.END)
        self.entrada_estado_inicial.insert(0, "q0")

        self.entrada_estados_finais.delete(0, tk.END)
        self.entrada_estados_finais.insert(0, "q2")

        self.entrada_transicoes.delete(1.0, tk.END)
        self.entrada_transicoes.insert(1.0, "q0,0,q1\nq0,1,q0\nq1,0,q1\nq1,1,q2\nq2,0,q1\nq2,1,q0")

        messagebox.showinfo("Exemplo 1",
                            "AFD que aceita cadeias binárias terminadas em '01'\n\nExemplos:\nACEITA: 01, 101, 001, 1101\nREJEITA: 0, 1, 10, 11, 00")

    def carregar_exemplo2(self):
        """Carrega exemplo de AFD que aceita cadeias com número par de 0s"""
        self.entrada_estados.delete(0, tk.END)
        self.entrada_estados.insert(0, "q0,q1")

        self.entrada_alfabeto.delete(0, tk.END)
        self.entrada_alfabeto.insert(0, "0,1")

        self.entrada_estado_inicial.delete(0, tk.END)
        self.entrada_estado_inicial.insert(0, "q0")

        self.entrada_estados_finais.delete(0, tk.END)
        self.entrada_estados_finais.insert(0, "q0")

        self.entrada_transicoes.delete(1.0, tk.END)
        self.entrada_transicoes.insert(1.0, "q0,0,q1\nq0,1,q0\nq1,0,q0\nq1,1,q1")

        messagebox.showinfo("Exemplo 2",
                            "AFD que aceita cadeias binárias com número par de 0s\n\nExemplos:\nACEITA: ε (vazio), 11, 00, 0110, 1001\nREJEITA: 0, 000, 10, 0111")

    def criar_afd(self):
        """Cria o AFD a partir dos dados inseridos"""
        try:
            # Processa estados
            estados_str = self.entrada_estados.get().strip()
            if not estados_str:
                raise ValueError("Estados não podem estar vazios")
            estados = set(e.strip() for e in estados_str.split(','))

            # Processa alfabeto
            alfabeto_str = self.entrada_alfabeto.get().strip()
            if not alfabeto_str:
                raise ValueError("Alfabeto não pode estar vazio")
            alfabeto = set(s.strip() for s in alfabeto_str.split(','))

            # Estado inicial
            estado_inicial = self.entrada_estado_inicial.get().strip()
            if not estado_inicial:
                raise ValueError("Estado inicial não pode estar vazio")
            if estado_inicial not in estados:
                raise ValueError(f"Estado inicial '{estado_inicial}' não está no conjunto de estados")

            # Estados finais
            estados_finais_str = self.entrada_estados_finais.get().strip()
            if not estados_finais_str:
                raise ValueError("Estados finais não podem estar vazios")
            estados_finais = set(e.strip() for e in estados_finais_str.split(','))
            for ef in estados_finais:
                if ef not in estados:
                    raise ValueError(f"Estado final '{ef}' não está no conjunto de estados")

            # Processa transições
            transicoes_str = self.entrada_transicoes.get(1.0, tk.END).strip()
            if not transicoes_str:
                raise ValueError("Transições não podem estar vazias")

            transicoes = {}
            linhas = transicoes_str.split('\n')
            for i, linha in enumerate(linhas, 1):
                linha = linha.strip()
                if not linha:
                    continue

                partes = [p.strip() for p in linha.split(',')]
                if len(partes) != 3:
                    raise ValueError(f"Linha {i}: formato inválido. Use: estado,simbolo,destino")

                estado_origem, simbolo, estado_destino = partes

                if estado_origem not in estados:
                    raise ValueError(f"Linha {i}: estado '{estado_origem}' não existe")
                if estado_destino not in estados:
                    raise ValueError(f"Linha {i}: estado '{estado_destino}' não existe")
                if simbolo not in alfabeto:
                    raise ValueError(f"Linha {i}: símbolo '{simbolo}' não está no alfabeto")

                chave = (estado_origem, simbolo)
                if chave in transicoes:
                    raise ValueError(f"Transição duplicada: δ({estado_origem}, {simbolo})")

                transicoes[chave] = estado_destino

            # Cria o AFD
            self.automata = AFD(estados, alfabeto, transicoes, estado_inicial, estados_finais)

            messagebox.showinfo("Sucesso", "AFD criado com sucesso!")

        except ValueError as e:
            messagebox.showerror("Erro", str(e))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao criar AFD: {str(e)}")

    def simular(self):
        """Executa a simulação do AFD com a cadeia fornecida"""
        if self.automata is None:
            messagebox.showwarning("Aviso", "Crie um AFD antes de simular!")
            return

        cadeia = self.entrada_cadeia.get()

        # Limpa o resultado anterior
        self.resultado_text.config(state=tk.NORMAL)
        self.resultado_text.delete(1.0, tk.END)

        # Executa o AFD
        aceita, historico, erro = self.automata.run(cadeia)

        # Exibe o resultado
        if cadeia == "":
            self.resultado_text.insert(tk.END, "Cadeia: ε (cadeia vazia)\n", "titulo")
        else:
            self.resultado_text.insert(tk.END, f"Cadeia: '{cadeia}'\n", "titulo")
        self.resultado_text.insert(tk.END, f"Tamanho: {len(cadeia)}\n\n", "titulo")

        if erro:
            self.resultado_text.insert(tk.END, f"ERRO: {erro}\n", "rejeita")
        else:
            # Resultado final
            estado_final = historico[-1][2]

            if aceita:
                self.resultado_text.insert(tk.END,
                                           f"ACEITA\nEstado final: '{estado_final}'\n", "aceita")
            else:
                self.resultado_text.insert(tk.END,
                                           f"REJEITA\nEstado final: '{estado_final}'\n", "rejeita")

        self.resultado_text.config(state=tk.DISABLED)

    def limpar(self):
        """Limpa os campos de entrada e resultado"""
        self.entrada_cadeia.delete(0, tk.END)
        self.resultado_text.config(state=tk.NORMAL)
        self.resultado_text.delete(1.0, tk.END)
        self.resultado_text.config(state=tk.DISABLED)

