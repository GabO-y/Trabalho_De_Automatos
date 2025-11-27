# ============== automato_base.py ==============
"""
Módulo de classe base para todos os autômatos
Define a interface comum que todos os autômatos devem implementar
"""

from abc import ABC, abstractmethod
from typing import Set, List, Tuple


class AutomatoBase(ABC):
    """
    Classe abstrata que define a interface para todos os autômatos

    Atributos:
        estados (Set[str]): Conjunto de estados do autômato
        alfabeto (Set[str]): Alfabeto de entrada
        estado_inicial (str): Estado inicial
        estados_finais (Set[str]): Conjunto de estados finais/aceitação
        historico (List[str]): Histórico de execução da simulação
    """

    def __init__(self, estados: Set[str], alfabeto: Set[str],
                 estado_inicial: str, estados_finais: Set[str]):
        """
        Inicializa o autômato com os parâmetros básicos

        Args:
            estados: Conjunto de estados
            alfabeto: Alfabeto de entrada
            estado_inicial: Estado inicial
            estados_finais: Conjunto de estados finais
        """
        self.estados = estados
        self.alfabeto = alfabeto
        self.estado_inicial = estado_inicial
        self.estados_finais = estados_finais
        self.historico = []

    @abstractmethod
    def simular(self, cadeia: str) -> Tuple[bool, List[str]]:
        """
        Simula a execução do autômato com a cadeia fornecida

        Args:
            cadeia (str): Cadeia a ser testada

        Returns:
            Tuple[bool, List[str]]: (cadeia_aceita, historico_passos)
        """
        pass

    def reset_historico(self):
        """Limpa o histórico de execução"""
        self.historico = []

    def __str__(self) -> str:
        """Representação em string do autômato"""
        return (f"{self.__class__.__name__}\n"
                f"Estados: {self.estados}\n"
                f"Alfabeto: {self.alfabeto}\n"
                f"Estado inicial: {self.estado_inicial}\n"
                f"Estados finais: {self.estados_finais}")