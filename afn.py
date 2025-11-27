# ============== afn.py ==============
"""
Módulo para Autômato Finito Não-Determinístico (AFN)

O AFN é um autômato que reconhece linguagens regulares.
Para um mesmo (estado, símbolo), pode haver múltiplas transições.
Também suporta ε-transições (transições vazias).
"""

from typing import Dict, Tuple, Set, Optional, List
from automato_base import AutomatoBase


class AFN(AutomatoBase):
    """
    Autômato Finito Não-Determinístico

    Características:
        - Para um mesmo (estado, símbolo), pode haver múltiplas transições
        - Suporta ε-transições (representadas como None)
        - Reconhece a mesma classe de linguagens que AFD (linguagens regulares)

    Atributos:
        transicoes (Dict): Mapeamento (estado, símbolo) -> conjunto de estados
    """

    def __init__(self, estados: Set[str], alfabeto: Set[str],
                 transicoes: Dict[Tuple[str, Optional[str]], Set[str]],
                 estado_inicial: str, estados_finais: Set[str]):
        """
        Inicializa um AFN

        Args:
            estados: Conjunto de estados
            alfabeto: Alfabeto de entrada
            transicoes: Dicionário com transições δ(q, a) = {q1, q2, ...}
                       Use None como símbolo para representar ε-transições
            estado_inicial: Estado inicial
            estados_finais: Conjunto de estados finais
        """
        super().__init__(estados, alfabeto, estado_inicial, estados_finais)
        self.transicoes = transicoes

    def _epsilon_fecho(self, estado_atual: str) -> Set[str]:
        """
        Calcula o ε-fecho de um estado

        O ε-fecho de um estado é o conjunto de todos os estados
        alcançáveis a partir dele seguindo apenas ε-transições.

        Args:
            estado_atual: Estado inicial

        Returns:
            Set[str]: Conjunto de estados no ε-fecho
        """
        fecho = {estado_atual}
        pilha = [estado_atual]

        while pilha:
            estado = pilha.pop()
            chave = (estado, None)  # None representa ε

            if chave in self.transicoes:
                for proximo in self.transicoes[chave]:
                    if proximo not in fecho:
                        fecho.add(proximo)
                        pilha.append(proximo)

        return fecho

    def _epsilon_fecho_conjunto(self, estados: Set[str]) -> Set[str]:
        """
        Calcula o ε-fecho de um conjunto de estados

        Args:
            estados: Conjunto de estados

        Returns:
            Set[str]: ε-fecho do conjunto
        """
        fecho = set()
        for estado in estados:
            fecho |= self._epsilon_fecho(estado)
        return fecho

    def simular(self, cadeia: str) -> Tuple[bool, List[str]]:
        """
        Simula a execução do AFN com a cadeia fornecida

        O AFN explora todos os caminhos possíveis através dos estados.
        A cadeia é aceita se existe pelo menos um caminho que termina
        em um estado final.

        Args:
            cadeia (str): Cadeia a ser reconhecida

        Returns:
            Tuple[bool, List[str]]: (cadeia_aceita, historico)

        Exemplo:
            >>> afn = AFN(...)
            >>> aceita, historico = afn.simular("aab")
            >>> if aceita:
            ...     print("Cadeia aceita por algum caminho!")
        """
        self.reset_historico()

        # Calcular estados iniciais considerando ε-transições
        estados_atuais = self._epsilon_fecho(self.estado_inicial)
        self.historico.append(f"Estados iniciais (com ε-fecho): {estados_atuais}")

        # Processar cada símbolo da cadeia
        for i, simbolo in enumerate(cadeia):
            # Validar se o símbolo está no alfabeto
            if simbolo not in self.alfabeto:
                self.historico.append(f"\n❌ Erro: Símbolo '{simbolo}' não está no alfabeto")
                return False, self.historico

            # Encontrar todos os próximos estados possíveis
            proximos_estados = set()
            for estado in estados_atuais:
                chave = (estado, simbolo)
                if chave in self.transicoes:
                    proximos_estados |= self.transicoes[chave]

            # Se não há próximos estados, rejeita
            if not proximos_estados:
                self.historico.append(
                    f"\nPasso {i + 1}: Nenhuma transição para '{simbolo}' a partir de {estados_atuais}")
                self.historico.append("❌ Cadeia REJEITADA")
                return False, self.historico

            # Aplicar ε-fecho ao conjunto de próximos estados
            estados_atuais = self._epsilon_fecho_conjunto(proximos_estados)
            self.historico.append(f"Passo {i + 1}: '{simbolo}' → {estados_atuais}")

        # Verificar se algum estado atual é final
        estados_finais_alcancados = estados_atuais & self.estados_finais
        self.historico.append(f"\nEstados finais alcançados: {estados_finais_alcancados}")

        aceita = bool(estados_finais_alcancados)

        if aceita:
            self.historico.append("✓ Resultado: CADEIA ACEITA")
        else:
            self.historico.append("✗ Resultado: CADEIA REJEITADA")

        return aceita, self.historico

    def __str__(self) -> str:
        """Representação em string do AFN"""
        return (f"AFN - Autômato Finito Não-Determinístico\n"
                f"Estados: {self.estados}\n"
                f"Alfabeto: {self.alfabeto}\n"
                f"Estado inicial: {self.estado_inicial}\n"
                f"Estados finais: {self.estados_finais}\n"
                f"Número de transições: {len(self.transicoes)}")