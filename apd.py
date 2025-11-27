# ============== apd.py ==============
"""
Módulo para Autômato a Pilha (APD)

O APD reconhece linguagens livres de contexto (LLC).
Combina máquina de estados finitos com uma pilha infinita.
"""

from typing import Dict, Tuple, Set, Optional, List
from automato_base import AutomatoBase


class APD(AutomatoBase):
    """
    Autômato a Pilha (Não-Determinístico)

    Características:
        - Máquina de estados finitos com uma pilha
        - Reconhece linguagens livres de contexto
        - Transições dependem do estado, símbolo de entrada e topo da pilha
        - Pode realizar operações: push (empilhar) e pop (desempilhar)

    Atributos:
        alfabeto_pilha (Set[str]): Símbolos que podem estar na pilha
        transicoes (Dict): Mapeamento (estado, símbolo, topo_pilha) -> [(novo_estado, operacoes_pilha)]
        simbolo_pilha_inicial (str): Símbolo inicial da pilha
    """

    def __init__(self, estados: Set[str], alfabeto: Set[str],
                 alfabeto_pilha: Set[str],
                 transicoes: Dict[Tuple[str, Optional[str], Optional[str]],
                 List[Tuple[str, List[str]]]],
                 estado_inicial: str, estados_finais: Set[str],
                 simbolo_pilha_inicial: str = 'Z'):
        """
        Inicializa um APD

        Args:
            estados: Conjunto de estados
            alfabeto: Alfabeto de entrada
            alfabeto_pilha: Alfabeto da pilha
            transicoes: Dicionário com transições δ(q, a, X) = [(q', γ)]
                       onde γ é a sequência a ser empilhada
            estado_inicial: Estado inicial
            estados_finais: Conjunto de estados finais
            simbolo_pilha_inicial: Símbolo inicial na pilha (padrão 'Z')
        """
        super().__init__(estados, alfabeto, estado_inicial, estados_finais)
        self.alfabeto_pilha = alfabeto_pilha
        self.transicoes = transicoes
        self.simbolo_pilha_inicial = simbolo_pilha_inicial

    def simular(self, cadeia: str) -> Tuple[bool, List[str]]:
        """
        Simula a execução do APD com a cadeia fornecida

        A simulação segue um caminho não-determinístico através dos estados.
        Em cada passo:
        1. Lê um símbolo de entrada (ou ε)
        2. Observa o topo da pilha
        3. Transiciona para novo estado
        4. Modifica a pilha (pop e eventualmente push)

        Args:
            cadeia (str): Cadeia a ser reconhecida

        Returns:
            Tuple[bool, List[str]]: (cadeia_aceita, historico)
        """
        self.reset_historico()
        pilha = [self.simbolo_pilha_inicial]
        estado_atual = self.estado_inicial
        posicao = 0

        # Registrar estado inicial
        self.historico.append(f"Estado inicial: {estado_atual}")
        self.historico.append(f"Pilha inicial: {pilha}")
        self.historico.append(f"Símbolo na pilha: {self.simbolo_pilha_inicial}\n")

        # Processar cadeia
        while posicao <= len(cadeia):
            # Símbolo atual (None = fim da cadeia = ε)
            simbolo_entrada = cadeia[posicao] if posicao < len(cadeia) else None

            # Topo da pilha
            simbolo_pilha = pilha[-1] if pilha else None

            # Procurar transição
            chave = (estado_atual, simbolo_entrada, simbolo_pilha)

            if chave not in self.transicoes:
                self.historico.append(f"\nPasso {posicao}: Sem transição definida")
                self.historico.append(f"  Estado: {estado_atual}")
                self.historico.append(f"  Entrada: '{simbolo_entrada if simbolo_entrada else 'ε'}'")
                self.historico.append(f"  Topo pilha: {simbolo_pilha}")
                self.historico.append("❌ Cadeia REJEITADA")
                return False, self.historico

            # Executar primeira transição possível (não-determinismo)
            transicoes_possiveis = self.transicoes[chave]

            for proximo_estado, operacoes_pilha in transicoes_possiveis:
                # Copiar pilha e executar operações
                pilha_copia = pilha.copy()

                # Pop: remover topo
                if pilha_copia:
                    pilha_copia.pop()

                # Push: adicionar novos símbolos
                pilha_copia.extend(operacoes_pilha)

                # Registrar passo
                self.historico.append(f"Passo {posicao}:")
                self.historico.append(f"  Entrada: '{simbolo_entrada if simbolo_entrada else 'ε'}'")
                self.historico.append(f"  Topo pilha: {simbolo_pilha}")
                self.historico.append(f"  Próximo estado: {proximo_estado}")
                self.historico.append(f"  Operação pilha: pop {simbolo_pilha}, push {operacoes_pilha}")
                self.historico.append(f"  Pilha após: {pilha_copia}")

                # Atualizar estado e pilha
                estado_atual = proximo_estado
                pilha = pilha_copia
                posicao += 1
                break

        # Verificar aceitação
        self.historico.append(f"\nEstado final: {estado_atual}")
        self.historico.append(f"Pilha final: {pilha}")

        # Aceitação por estado final ou pilha vazia
        aceita = (estado_atual in self.estados_finais) or (len(pilha) == 0)

        if aceita:
            self.historico.append("✓ Resultado: CADEIA ACEITA")
        else:
            self.historico.append("✗ Resultado: CADEIA REJEITADA")

        return aceita, self.historico

    def __str__(self) -> str:
        """Representação em string do APD"""
        return (f"APD - Autômato a Pilha\n"
                f"Estados: {self.estados}\n"
                f"Alfabeto: {self.alfabeto}\n"
                f"Alfabeto pilha: {self.alfabeto_pilha}\n"
                f"Estado inicial: {self.estado_inicial}\n"
                f"Estados finais: {self.estados_finais}\n"
                f"Símbolo pilha inicial: {self.simbolo_pilha_inicial}\n"
                f"Número de transições: {len(self.transicoes)}")