import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json

from interface import *


class AFD:
    """
    Classe que representa um Autômato Finito Determinístico (AFD)

    Atributos:
        estados: conjunto de estados do autômato
        alfabeto: conjunto de símbolos de entrada
        transicoes: dicionário de transições {(estado, símbolo): próximo_estado}
        estado_inicial: estado onde a execução começa
        estados_finais: conjunto de estados de aceitação
    """

    def __init__(self, estados, alfabeto, transicoes, estado_inicial, estados_finais):
        self.estados = estados
        self.alfabeto = alfabeto
        self.transicoes = transicoes
        self.estado_inicial = estado_inicial
        self.estados_finais = estados_finais

    def processar_cadeia(self, cadeia):
        """
        Simula a execução do AFD para uma cadeia de entrada

        Args:
            cadeia: string a ser processada

        Returns:
            tupla (aceita, historico, erro) onde:
                - aceita: True se a cadeia foi aceita, False caso contrário
                - historico: lista de tuplas (estado_atual, simbolo, proximo_estado)
                - erro: mensagem de erro ou None
        """
        estado_atual = self.estado_inicial
        historico = [(estado_atual, '', estado_atual)]  # Estado inicial

        for simbolo in cadeia:
            # Verifica se o símbolo pertence ao alfabeto
            if simbolo not in self.alfabeto:
                return False, historico, f"Símbolo '{simbolo}' não pertence ao alfabeto"

            # Busca a transição
            chave = (estado_atual, simbolo)
            if chave not in self.transicoes:
                return False, historico, f"Transição não definida para ({estado_atual}, {simbolo})"

            proximo_estado = self.transicoes[chave]
            historico.append((estado_atual, simbolo, proximo_estado))
            estado_atual = proximo_estado

        # Verifica se o estado final é de aceitação
        aceita = estado_atual in self.estados_finais
        return aceita, historico, None



