"""
Máquina de Turing - Interface Gráfica Completa
Simulador de Máquinas de Turing com fita infinita, cabeça móvel e função de transição

Definição Formal:
M = (Q, Σ, Γ, δ, q₀, ▢, F)

Onde:
- Q: conjunto finito de estados internos
- Σ: conjunto finito chamado de alfabeto de entrada
- Γ: conjunto finito de símbolos da fita
- δ: Q × Γ → Q × Γ × {L, R} é a função de transição
- q₀: estado inicial
- ▢: símbolo branco (blank)
- F: conjunto de estados finais (aceitação)
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from typing import Optional, Dict, Set, Tuple, List


class MaquinaTuring:
    """
    Implementação de uma Máquina de Turing
    M = (Q, Σ, Γ, δ, q₀, ▢, F)
    """

    def __init__(self, Q: Set[str], Sigma: Set[str], Gamma: Set[str],
                 delta: Dict, q0: str, blank: str, F: Set[str]):
        """
        Inicializa a Máquina de Turing

        Args:
            Q: conjunto de estados internos
            Sigma: alfabeto de entrada
            Gamma: alfabeto da fita
            delta: função de transição
            q0: estado inicial
            blank: símbolo branco
            F: conjunto de estados finais de aceitação
        """
        self.Q = Q
        self.Sigma = Sigma
        self.Gamma = Gamma
        self.delta = delta
        self.q0 = q0
        self.blank = blank
        self.F = F

        self.posicao = 0
        self.fita = {}
        self.estado_atual = q0

    def simular(self, cadeia: str, max_passos: int = 10000) -> Tuple[bool, List[str]]:
        """
        Simula a execução da Máquina de Turing

        Args:
            cadeia: cadeia de entrada
            max_passos: máximo de passos para evitar loops infinitos

        Returns:
            Tupla (aceita, histórico)
        """
        self.fita = {}
        self.posicao = 0
        self.estado_atual = self.q0

        for i, simbolo in enumerate(cadeia):
            self.fita[i] = simbolo

        historico = []
        historico.append("SIMULACAO DE MAQUINA DE TURING")
        historico.append("M = (Q, Sigma, Gamma, delta, q0, blank, F)")
        historico.append("")

        historico.append("DEFINICAO FORMAL:")
        historico.append(f"  Q = {{{', '.join(sorted(self.Q))}}}")
        historico.append(f"  Sigma = {{{', '.join(sorted(self.Sigma)) if self.Sigma else 'vazio'}}}")
        historico.append(f"  Gamma = {{{', '.join(sorted(self.Gamma))}}}")
        historico.append(f"  q0 = {self.q0}")
        historico.append(f"  blank = '{self.blank}'")
        historico.append(f"  F = {{{', '.join(sorted(self.F)) if self.F else 'vazio'}}}")
        historico.append("")

        if cadeia == "":
            historico.append("ENTRADA: vazia")
            historico.append("")
        else:
            historico.append(f"ENTRADA: '{cadeia}'")
            historico.append("")

        historico.append(f"Estado inicial: {self.q0}")
        historico.append(f"Posicao inicial: 0")
        historico.append("")
        historico.append("-" * 70)

        passo = 0
        while passo < max_passos:
            simbolo_lido = self.fita.get(self.posicao, self.blank)

            fita_visual = self._gerar_visualizacao_fita()
            historico.append(f"\nPASSO {passo}:")
            historico.append(f"  Fita: {fita_visual}")
            historico.append(f"  Estado: {self.estado_atual} | Posicao: {self.posicao} | Lido: '{simbolo_lido}'")

            if self.estado_atual in self.F:
                historico.append("")
                historico.append("CADEIA ACEITA")
                historico.append(f"Estado de aceitacao atingido: {self.estado_atual}")
                return True, historico

            chave_transicao = (self.estado_atual, simbolo_lido)
            if chave_transicao not in self.delta:
                historico.append("")
                historico.append("CADEIA REJEITADA")
                historico.append(f"Nenhuma transicao definida para delta({self.estado_atual}, '{simbolo_lido}')")
                return False, historico

            novo_estado, novo_simbolo, direcao = self.delta[chave_transicao]

            if direcao not in ["L", "R"]:
                raise ValueError(f"Direcao invalida: {direcao}. Use 'L' ou 'R'")

            self.fita[self.posicao] = novo_simbolo
            dir_nome = "Esquerda" if direcao == "L" else "Direita"
            historico.append(f"  Acao: delta({self.estado_atual}, '{simbolo_lido}') = ({novo_estado}, '{novo_simbolo}', {direcao})")
            historico.append(f"        Escrever '{novo_simbolo}', Mover {dir_nome}, Novo estado: {novo_estado}")

            if direcao == "R":
                self.posicao += 1
            elif direcao == "L":
                self.posicao -= 1

            self.estado_atual = novo_estado
            passo += 1

        historico.append("")
        historico.append("CADEIA REJEITADA")
        historico.append("LOOPING INFINITO DETECTADO")
        historico.append(f"Excedeu o maximo de {max_passos} passos")
        return False, historico

    def _gerar_visualizacao_fita(self, intervalo: int = 10) -> str:
        """Gera visualização da fita ao redor da posição atual"""
        inicio = max(self.posicao - intervalo, min(self.fita.keys()) if self.fita else 0)
        fim = self.posicao + intervalo + 1

        fita_visual = "["
        for i in range(inicio, fim):
            simbolo = self.fita.get(i, self.blank)
            if i == self.posicao:
                fita_visual += f"[{simbolo}]"
            else:
                fita_visual += f" {simbolo} "
        fita_visual += "]"

        return fita_visual


class CriadorMaquinaTuring:
    """Cria instâncias de Máquinas de Turing a partir de entradas do usuário"""

    def criar_mt(self, Q_str: str, Sigma_str: str, Gamma_str: str,
                 q0_str: str, F_str: str, delta_str: str, blank: str = "_") -> MaquinaTuring:
        """
        Cria uma Máquina de Turing a partir de strings de entrada
        """
        Q = set(e.strip() for e in Q_str.split(",") if e.strip())
        Sigma = set(s.strip() for s in Sigma_str.split(",") if s.strip() and s.strip() != "epsilon")
        Gamma = set(s.strip() for s in Gamma_str.split(",") if s.strip())

        q0 = q0_str.strip()
        F = set(e.strip() for e in F_str.split(",") if e.strip())

        if q0 not in Q:
            raise ValueError(f"Estado inicial '{q0}' nao esta em Q")
        if not F.issubset(Q):
            raise ValueError(f"F (estados finais) deve estar contido em Q")

        delta = {}
        for linha in delta_str.strip().split("\n"):
            if linha.strip():
                partes = [p.strip() for p in linha.split(",")]
                if len(partes) >= 5:
                    estado = partes[0]
                    simbolo = partes[1] if partes[1] != "epsilon" else ""
                    novo_estado = partes[2]
                    novo_simbolo = partes[3] if partes[3] != "epsilon" else ""
                    direcao = partes[4].upper()

                    if direcao not in ["L", "R"]:
                        raise ValueError(f"Direcao invalida: {direcao}. Use 'L' ou 'R'")

                    delta[(estado, simbolo)] = (novo_estado, novo_simbolo, direcao)

        return MaquinaTuring(Q, Sigma, Gamma, delta, q0, blank, F)


class SimuladorMaquinaTuring:
    """Interface gráfica para simulação de Máquina de Turing"""

    def __init__(self, root):
        """Inicializa a interface gráfica"""
        self.root = root
        self.root.title("Simulador de Maquina de Turing")
        self.root.geometry("1200x850")

        self.maquina: Optional[MaquinaTuring] = None
        self.criador = CriadorMaquinaTuring()

        self.criar_interface()

    def criar_interface(self):
        """Cria os componentes da interface gráfica"""

        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        titulo = ttk.Label(main_frame, text="Simulador de Maquina de Turing",
                          font=("Arial", 16, "bold"))
        titulo.grid(row=0, column=0, columnspan=2, pady=10)

        self.criar_frame_entrada(main_frame)
        self.criar_frame_simulacao(main_frame)
        self.criar_frame_resultado(main_frame)

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)

        self.root.bind('<Escape>', lambda e: self.root.destroy())

    def criar_frame_entrada(self, parent):
        """Frame para entrada da definição da Máquina de Turing"""
        frame = ttk.LabelFrame(parent, text="Definicao Formal: M = (Q, Sigma, Gamma, delta, q0, blank, F)", padding="10")
        frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(frame, text="Q - Estados (separados por virgula):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entrada_Q = ttk.Entry(frame, width=60)
        self.entrada_Q.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        self.entrada_Q.insert(0, "q0,q1,q2")

        ttk.Label(frame, text="Sigma - Alfabeto de Entrada (separado por virgula):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entrada_Sigma = ttk.Entry(frame, width=60)
        self.entrada_Sigma.grid(row=1, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        self.entrada_Sigma.insert(0, "a,b")

        ttk.Label(frame, text="Gamma - Alfabeto da Fita (separado por virgula):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.entrada_Gamma = ttk.Entry(frame, width=60)
        self.entrada_Gamma.grid(row=2, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        self.entrada_Gamma.insert(0, "a,b,_")

        ttk.Label(frame, text="q0 - Estado Inicial:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.entrada_q0 = ttk.Entry(frame, width=60)
        self.entrada_q0.grid(row=3, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        self.entrada_q0.insert(0, "q0")

        ttk.Label(frame, text="F - Estados Finais de Aceitacao (separados por virgula):").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.entrada_F = ttk.Entry(frame, width=60)
        self.entrada_F.grid(row=4, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        self.entrada_F.insert(0, "q2")

        ttk.Label(frame, text="delta - Funcao de Transicao: delta: Q x Gamma -> Q x Gamma x {L, R}").grid(row=5, column=0, sticky=tk.NW, pady=5)
        ttk.Label(frame, text="(formato: estado,simbolo,novo_estado,novo_simbolo,direcao)", font=("Arial", 8)).grid(row=5, column=1, sticky=tk.W, pady=2)

        self.entrada_delta = scrolledtext.ScrolledText(frame, height=7, width=70, wrap=tk.WORD)
        self.entrada_delta.grid(row=6, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        self.entrada_delta.insert(1.0,
            "q0,a,q0,a,R\nq0,b,q1,b,R\nq0,_,q2,_,R\nq1,b,q1,b,R\nq1,_,q2,_,R")

        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=7, column=0, columnspan=2, pady=10)

        ttk.Button(btn_frame, text="Criar MT", command=self.criar_mt).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Exemplo 1 (a*b*)", command=self.carregar_exemplo1).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Exemplo 2 (0*)", command=self.carregar_exemplo2).pack(side=tk.LEFT, padx=5)

        frame.columnconfigure(1, weight=1)

    def criar_frame_simulacao(self, parent):
        """Frame para entrada e simulação"""
        frame = ttk.LabelFrame(parent, text="Simulacao", padding="10")
        frame.grid(row=1, column=2, sticky=(tk.W, tk.E), padx=5)

        ttk.Label(frame, text="Cadeia de Entrada:").pack(anchor=tk.W, pady=5)

        self.entrada_cadeia = ttk.Entry(frame, width=40, font=("Arial", 11))
        self.entrada_cadeia.pack(fill=tk.X, pady=5)
        self.entrada_cadeia.bind('<Return>', lambda e: self.simular())

        btn_simular = ttk.Button(frame, text="Simular", command=self.simular)
        btn_simular.pack(fill=tk.X, pady=5)

        btn_limpar = ttk.Button(frame, text="Limpar", command=self.limpar)
        btn_limpar.pack(fill=tk.X, pady=5)

    def criar_frame_resultado(self, parent):
        """Frame para exibir resultado da simulação"""
        frame = ttk.LabelFrame(parent, text="Resultado da Simulacao", padding="10")
        frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)

        self.resultado_text = scrolledtext.ScrolledText(frame, height=15, width=140, wrap=tk.WORD)
        self.resultado_text.pack(fill=(tk.BOTH), expand=True)

        self.resultado_text.tag_config("aceita", foreground="green", font=("Arial", 10, "bold"))
        self.resultado_text.tag_config("rejeita", foreground="red", font=("Arial", 10, "bold"))

    def criar_mt(self):
        """Cria a Máquina de Turing"""
        try:
            Q_str = self.entrada_Q.get()
            Sigma_str = self.entrada_Sigma.get()
            Gamma_str = self.entrada_Gamma.get()
            q0_str = self.entrada_q0.get()
            F_str = self.entrada_F.get()
            delta_str = self.entrada_delta.get(1.0, tk.END)

            self.maquina = self.criador.criar_mt(
                Q_str, Sigma_str, Gamma_str, q0_str, F_str, delta_str
            )

            messagebox.showinfo("Sucesso", "Maquina de Turing criada com sucesso!")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao criar MT:\n{str(e)}")

    def simular(self):
        """Executa a simulação da Máquina de Turing"""
        if self.maquina is None:
            messagebox.showwarning("Aviso", "Crie uma Maquina de Turing antes de simular!")
            return

        cadeia = self.entrada_cadeia.get()

        self.resultado_text.config(state=tk.NORMAL)
        self.resultado_text.delete(1.0, tk.END)

        aceita, historico = self.maquina.simular(cadeia)

        for linha in historico:
            if "ACEITA" in linha:
                self.resultado_text.insert(tk.END, linha + "\n", "aceita")
            elif "REJEITADA" in linha or "LOOPING" in linha:
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
        """Carrega exemplo 1: reconhece a*b*"""
        self.entrada_Q.delete(0, tk.END)
        self.entrada_Q.insert(0, "q0,q1,q2")
        self.entrada_Sigma.delete(0, tk.END)
        self.entrada_Sigma.insert(0, "a,b")
        self.entrada_Gamma.delete(0, tk.END)
        self.entrada_Gamma.insert(0, "a,b,_")
        self.entrada_q0.delete(0, tk.END)
        self.entrada_q0.insert(0, "q0")
        self.entrada_F.delete(0, tk.END)
        self.entrada_F.insert(0, "q2")
        self.entrada_delta.delete(1.0, tk.END)
        self.entrada_delta.insert(1.0,
            "q0,a,q0,a,R\nq0,b,q1,b,R\nq0,_,q2,_,R\nq1,b,q1,b,R\nq1,_,q2,_,R")

    def carregar_exemplo2(self):
        """Carrega exemplo 2: reconhece 0*"""
        self.entrada_Q.delete(0, tk.END)
        self.entrada_Q.insert(0, "q0,q1")
        self.entrada_Sigma.delete(0, tk.END)
        self.entrada_Sigma.insert(0, "0")
        self.entrada_Gamma.delete(0, tk.END)
        self.entrada_Gamma.insert(0, "0,_")
        self.entrada_q0.delete(0, tk.END)
        self.entrada_q0.insert(0, "q0")
        self.entrada_F.delete(0, tk.END)
        self.entrada_F.insert(0, "q1")
        self.entrada_delta.delete(1.0, tk.END)
        self.entrada_delta.insert(1.0, "q0,0,q0,0,R\nq0,_,q1,_,R")


if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorMaquinaTuring(root)
    root.mainloop()