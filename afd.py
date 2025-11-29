# ============== afd.py ==============
"""
Módulo para Autômato Finito Determinístico (AFD)

O AFD é um autômato que reconhece linguagens regulares.
Para cada estado e símbolo, há exatamente uma transição.
"""

from typing import Dict, Tuple, Set, List
from automato_base import AutomatoBase


class AFD(AutomatoBase):
    """
    Autômato Finito Determinístico

    Características:
        - Para cada (estado, símbolo), há apenas uma transição
        - Sem ε-transições (transições vazias)
        - Função de transição total ou parcial

    Atributos:
        transicoes (Dict): Mapeamento (estado, símbolo) -> próximo_estado
    """

    def __init__(self, estados: Set[str], alfabeto: Set[str],
                 transicoes: Dict[Tuple[str, str], str],
                 estado_inicial: str, estados_finais: Set[str]):
        """
        Inicializa um AFD

        Args:
            estados: Conjunto de estados
            alfabeto: Alfabeto de entrada
            transicoes: Dicionário com transições δ(q, a) = q'
            estado_inicial: Estado inicial
            estados_finais: Conjunto de estados finais

        Raises:
            ValueError: Se a configuração for inválida
        """
        super().__init__(estados, alfabeto, estado_inicial, estados_finais)
        self.transicoes = transicoes
        self._validar()

    def _validar(self):
        """Valida a configuração do AFD"""
        if self.estado_inicial not in self.estados:
            raise ValueError(f"Estado inicial '{self.estado_inicial}' não existe")

        for estado_final in self.estados_finais:
            if estado_final not in self.estados:
                raise ValueError(f"Estado final '{estado_final}' não existe")

        for (estado, simbolo), destino in self.transicoes.items():
            if estado not in self.estados:
                raise ValueError(f"Estado '{estado}' na transição não existe")
            if simbolo not in self.alfabeto:
                raise ValueError(f"Símbolo '{simbolo}' na transição não está no alfabeto")
            if destino not in self.estados:
                raise ValueError(f"Estado destino '{destino}' não existe")

    def simular(self, cadeia: str) -> Tuple[bool, List[str]]:
        """
        Simula a execução do AFD com a cadeia fornecida

        A simulação segue determinísticamente um único caminho através dos estados.
        Se em algum ponto não houver transição definida, a cadeia é rejeitada.

        Args:
            cadeia (str): Cadeia a ser reconhecida

        Returns:
            Tuple[bool, List[str]]: (cadeia_aceita, historico)

        Exemplo:
            >>> afd = AFD(...)
            >>> aceita, historico = afd.simular("0101")
            >>> if aceita:
            ...     print("Cadeia aceita!")
        """
        self.reset_historico()
        estado_atual = self.estado_inicial

        # Registrar estado inicial
        self.historico.append(f"Estado inicial: {estado_atual}")

        # Processar cada símbolo da cadeia
        for i, simbolo in enumerate(cadeia):
            # Validar se o símbolo está no alfabeto
            if simbolo not in self.alfabeto:
                self.historico.append(f"\n Erro: Símbolo '{simbolo}' não está no alfabeto")
                self.historico.append(f"Alfabeto válido: {self.alfabeto}")
                return False, self.historico

            # Procurar a transição
            chave = (estado_atual, simbolo)
            if chave not in self.transicoes:
                self.historico.append(f"\nPasso {i + 1}: δ({estado_atual}, '{simbolo}') = indefinida")
                self.historico.append(f" Cadeia REJEITADA - Transição não definida para '{simbolo}'")
                return False, self.historico

            # Executar transição
            proximo_estado = self.transicoes[chave]
            self.historico.append(f"Passo {i + 1}: δ({estado_atual}, '{simbolo}') = {proximo_estado}")
            estado_atual = proximo_estado

        # Verificar se terminou em estado final
        self.historico.append(f"\nEstado final alcançado: {estado_atual}")
        aceita = estado_atual in self.estados_finais

        if aceita:
            self.historico.append("Resultado: CADEIA ACEITA")
        else:
            self.historico.append("Resultado: CADEIA REJEITADA")

        return aceita, self.historico

    def __str__(self) -> str:
        """Representação em string do AFD"""
        return (f"AFD - Autômato Finito Determinístico\n"
                f"Estados: {self.estados}\n"
                f"Alfabeto: {self.alfabeto}\n"
                f"Estado inicial: {self.estado_inicial}\n"
                f"Estados finais: {self.estados_finais}\n"
                f"Número de transições: {len(self.transicoes)}")