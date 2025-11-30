"""
Interface grafica para o Simulador de Automatos

Permite criar e simular diferentes tipos de automatos (AFD, AFN, APD).
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from typing import Optional

from criador_automatos import CriadorAutomatos
from automato_base import AutomatoBase


class SimuladorAutomatos:
    """Interface grafica para simulacao de automatos"""

    def __init__(self, root):
        """
        Inicializa a interface grafica

        Args:
            root: Janela raiz do Tkinter
        """
        self.root = root
        self.root.title("Simulador de Automatos - Linguagens Formais")
        self.root.geometry("1200x750")

        self.automato_sel = tk.StringVar(value="AFD")
        self.automato: Optional[AutomatoBase] = None
        self.criador = CriadorAutomatos()

        self.criar_interface()

    def criar_interface(self):
        """Cria os componentes da interface grafica"""

        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        titulo = ttk.Label(main_frame, text="Simulador de Automatos",
                           font=("Arial", 16, "bold"))
        titulo.grid(row=0, column=0, columnspan=2, pady=10)

        # Selecao do tipo de automato
        self.criar_frame_selecao(main_frame)

        # Frame de entrada
        self.criar_frame_entrada(main_frame)

        # Frame de simulacao
        self.criar_frame_simulacao(main_frame)

        # Frame de resultado
        self.criar_frame_resultado(main_frame)

        # Configurar redimensionamento
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)

        self.root.bind('<Escape>', lambda e: self.root.destroy())

    def criar_frame_selecao(self, parent):
        """Frame para selecao do tipo de automato"""
        frame = ttk.LabelFrame(parent, text="Tipo de Automato", padding="10")
        frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        ttk.Radiobutton(frame, text="AFD", variable=self.automato_sel,
                        value="AFD", command=self.atualizar_entrada).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(frame, text="AFN", variable=self.automato_sel,
                        value="AFN", command=self.atualizar_entrada).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(frame, text="APD", variable=self.automato_sel,
                        value="APD", command=self.atualizar_entrada).pack(side=tk.LEFT, padx=10)

    def criar_frame_entrada(self, parent):
        """Frame para entrada da definicao do automato"""
        frame = ttk.LabelFrame(parent, text="Definicao do Automato", padding="10")
        frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        # Estados
        ttk.Label(frame, text="Estados (separados por virgula):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entrada_estados = ttk.Entry(frame, width=60)
        self.entrada_estados.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        self.entrada_estados.insert(0, "q0,q1,q2")

        # Alfabeto
        ttk.Label(frame, text="Alfabeto (separado por virgula):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entrada_alfabeto = ttk.Entry(frame, width=60)
        self.entrada_alfabeto.grid(row=1, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        self.entrada_alfabeto.insert(0, "0,1")

        # Estado inicial
        ttk.Label(frame, text="Estado Inicial:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.entrada_estado_inicial = ttk.Entry(frame, width=60)
        self.entrada_estado_inicial.grid(row=2, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        self.entrada_estado_inicial.insert(0, "q0")

        # Estados finais
        ttk.Label(frame, text="Estados Finais (separados por virgula):").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.entrada_estados_finais = ttk.Entry(frame, width=60)
        self.entrada_estados_finais.grid(row=3, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        self.entrada_estados_finais.insert(0, "q2")

        # Transicoes
        ttk.Label(frame, text="Transicoes (formato: estado,simbolo,destino):").grid(row=4, column=0, sticky=tk.NW,
                                                                                    pady=5)
        self.entrada_transicoes = scrolledtext.ScrolledText(frame, height=6, width=70, wrap=tk.WORD)
        self.entrada_transicoes.grid(row=4, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        self.entrada_transicoes.insert(1.0, "q0,0,q1\nq0,1,q0\nq1,0,q1\nq1,1,q2\nq2,0,q1\nq2,1,q0")

        # Botoes
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)

        ttk.Button(btn_frame, text="Criar Automato", command=self.criar_automato).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Exemplo 1 (termina em 01)", command=self.carregar_exemplo1).pack(side=tk.LEFT,
                                                                                                     padx=5)
        ttk.Button(btn_frame, text="Exemplo 2 (numero par de 0s)", command=self.carregar_exemplo2).pack(side=tk.LEFT,
                                                                                                        padx=5)

        frame.columnconfigure(1, weight=1)

    def criar_frame_simulacao(self, parent):
        """Frame para entrada e simulacao"""
        frame = ttk.LabelFrame(parent, text="Simulacao", padding="10")
        frame.grid(row=2, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)

        ttk.Label(frame, text="Cadeia:").pack(anchor=tk.W, pady=5)

        self.entrada_cadeia = ttk.Entry(frame, width=40, font=("Arial", 11))
        self.entrada_cadeia.pack(fill=tk.X, pady=5)
        self.entrada_cadeia.bind('<Return>', lambda e: self.simular())

        btn_simular = ttk.Button(frame, text="Simular", command=self.simular)
        btn_simular.pack(fill=tk.X, pady=5)

        btn_limpar = ttk.Button(frame, text="Limpar", command=self.limpar)
        btn_limpar.pack(fill=tk.X, pady=5)

    def criar_frame_resultado(self, parent):
        """Frame para exibir resultado da simulacao"""
        frame = ttk.LabelFrame(parent, text="Resultado da Simulacao", padding="10")
        frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)

        self.resultado_text = scrolledtext.ScrolledText(frame, height=12, width=100, wrap=tk.WORD)
        self.resultado_text.pack(fill=(tk.BOTH), expand=True)

        self.resultado_text.tag_config("aceita", foreground="green", font=("Arial", 10, "bold"))
        self.resultado_text.tag_config("rejeita", foreground="red", font=("Arial", 10, "bold"))

    def atualizar_entrada(self):
        """Atualiza o exemplo conforme o tipo de automato selecionado e limpa a interface"""
        tipo = self.automato_sel.get()

        # Limpar campos de entrada
        self.entrada_estados.delete(0, tk.END)
        self.entrada_alfabeto.delete(0, tk.END)
        self.entrada_estado_inicial.delete(0, tk.END)
        self.entrada_estados_finais.delete(0, tk.END)
        self.entrada_transicoes.delete(1.0, tk.END)
        self.entrada_cadeia.delete(0, tk.END)

        # Limpar resultado
        self.resultado_text.config(state=tk.NORMAL)
        self.resultado_text.delete(1.0, tk.END)
        self.resultado_text.config(state=tk.DISABLED)

        # Resetar automato
        self.automato = None

        # Carregar exemplo conforme tipo
        if tipo == "AFD":
            self.entrada_estados.insert(0, "q0,q1,q2")
            self.entrada_alfabeto.insert(0, "0,1")
            self.entrada_estado_inicial.insert(0, "q0")
            self.entrada_estados_finais.insert(0, "q2")
            self.entrada_transicoes.insert(1.0, "q0,0,q1\nq0,1,q0\nq1,0,q1\nq1,1,q2\nq2,0,q1\nq2,1,q0")

        elif tipo == "AFN":
            self.entrada_estados.insert(0, "q0,q1,q2")
            self.entrada_alfabeto.insert(0, "a,b,c")
            self.entrada_estado_inicial.insert(0, "q0")
            self.entrada_estados_finais.insert(0, "q2")
            self.entrada_transicoes.insert(1.0, "q0,a,q0,q1\nq0,,q1\nq1,b,q1\nq1,,q2\nq2,c,q2")

        elif tipo == "APD":
            self.entrada_estados.insert(0, "q0,q1,q2")
            self.entrada_alfabeto.insert(0, "a,b")
            self.entrada_estado_inicial.insert(0, "q0")
            self.entrada_estados_finais.insert(0, "q2")
            self.entrada_transicoes.insert(1.0, "q0,a,Z,q0,Za\nq0,a,a,q0,aa,\nq0,b,a,q1,\nq1,b,a,q1,\nq1,,Z,q2,Z")

    def criar_automato(self):
        """Cria o automato selecionado"""
        tipo = self.automato_sel.get()

        try:
            estados_str = self.entrada_estados.get()
            alfabeto_str = self.entrada_alfabeto.get()
            estado_inicial_str = self.entrada_estado_inicial.get()
            estados_finais_str = self.entrada_estados_finais.get()
            transicoes_str = self.entrada_transicoes.get(1.0, tk.END)

            if tipo == "AFD":
                self.automato = self.criador.criar_afd(
                    estados_str, alfabeto_str, estado_inicial_str,
                    estados_finais_str, transicoes_str
                )
            elif tipo == "AFN":
                self.automato = self.criador.criar_afn(
                    estados_str, alfabeto_str, estado_inicial_str,
                    estados_finais_str, transicoes_str
                )
            elif tipo == "APD":
                self.automato = self.criador.criar_apd(
                    estados_str, alfabeto_str, estado_inicial_str,
                    estados_finais_str, transicoes_str
                )

            messagebox.showinfo("Sucesso", f"{tipo} criado com sucesso!")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao criar {tipo}:\n{str(e)}")

    def simular(self):
        """Executa a simulacao do automato"""
        if self.automato is None:
            messagebox.showwarning("Aviso", "Crie um automato antes de simular!")
            return

        cadeia = self.entrada_cadeia.get()
        tipo = self.automato_sel.get()

        self.resultado_text.config(state=tk.NORMAL)
        self.resultado_text.delete(1.0, tk.END)

        aceita, historico = self.automato.simular(cadeia)

        self.resultado_text.insert(tk.END, f"Simulacao de {tipo}\n\n")

        if cadeia == "":
            self.resultado_text.insert(tk.END, "Cadeia: vazia\n\n")
        else:
            self.resultado_text.insert(tk.END, f"Cadeia: '{cadeia}'\n\n")

        for linha in historico:
            if "ACEITA" in linha:
                self.resultado_text.insert(tk.END, linha + "\n", "aceita")
            elif "REJEITADA" in linha:
                self.resultado_text.insert(tk.END, linha + "\n", "rejeita")
            else:
                self.resultado_text.insert(tk.END, linha + "\n")

        self.resultado_text.config(state=tk.DISABLED)

    def limpar(self):
        """Limpa os campos"""
        self.entrada_cadeia.delete(0, tk.END)
        self.resultado_text.config(state=tk.NORMAL)
        self.resultado_text.delete(1.0, tk.END)
        self.resultado_text.config(state=tk.DISABLED)

    def carregar_exemplo1(self):
        """Carrega primeiro exemplo"""
        self.entrada_estados.delete(0, tk.END)
        self.entrada_estados.insert(0, "q0,q1,q2")
        self.entrada_alfabeto.delete(0, tk.END)
        self.entrada_alfabeto.insert(0, "0,1")
        self.entrada_estado_inicial.delete(0, tk.END)
        self.entrada_estado_inicial.insert(0, "q0")
        self.entrada_estados_finais.delete(0, tk.END)
        self.entrada_estados_finais.insert(0, "q2")

    def carregar_exemplo2(self):
        """Carrega segundo exemplo"""
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


if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorAutomatos(root)
    root.mainloop()