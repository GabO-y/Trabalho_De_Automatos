"""
Módulo para criação de autômatos a partir de entrada do usuário

Este módulo centraliza a criação e validação de todos os tipos de autômatos.
Facilita a adição de novos tipos e a reutilização do código.
"""

from typing import Set, Dict, Tuple, Optional, List
from afd import AFD
from afn import AFN
from apd import APD


class CriadorAutomatos:
    """Factory para criar autômatos a partir de strings de entrada"""

    @staticmethod
    def criar_afd(estados_str: str, alfabeto_str: str, estado_inicial_str: str,
                  estados_finais_str: str, transicoes_str: str) -> AFD:
        """
        Cria um AFD a partir de strings de entrada

        Args:
            estados_str: "q0,q1,q2"
            alfabeto_str: "0,1"
            estado_inicial_str: "q0"
            estados_finais_str: "q2"
            transicoes_str: "q0,0,q1\nq0,1,q0\n..."

        Returns:
            AFD: Autômato criado

        Raises:
            ValueError: Se os dados forem inválidos
        """
        # Processar entrada
        estados = set(e.strip() for e in estados_str.split(',') if e.strip())
        alfabeto = set(s.strip() for s in alfabeto_str.split(',') if s.strip())
        estado_inicial = estado_inicial_str.strip()
        estados_finais = set(e.strip() for e in estados_finais_str.split(',') if e.strip())

        # Processar transições
        transicoes = {}
        linhas = transicoes_str.strip().split('\n')

        for i, linha in enumerate(linhas, 1):
            linha = linha.strip()
            if not linha or linha.startswith('#'):
                continue

            partes = [p.strip() for p in linha.split(',')]
            if len(partes) != 3:
                raise ValueError(f"Linha {i}: formato inválido. Use: estado,símbolo,destino")

            estado_origem, simbolo, estado_destino = partes

            if estado_origem not in estados:
                raise ValueError(f"Linha {i}: estado '{estado_origem}' não existe")
            if estado_destino not in estados:
                raise ValueError(f"Linha {i}: estado '{estado_destino}' não existe")
            if simbolo not in alfabeto:
                raise ValueError(f"Linha {i}: símbolo '{simbolo}' não está no alfabeto")

            chave = (estado_origem, simbolo)
            if chave in transicoes:
                raise ValueError(f"Linha {i}: transição duplicada δ({estado_origem}, {simbolo})")

            transicoes[chave] = estado_destino

        if not transicoes:
            raise ValueError("Nenhuma transição foi definida")

        return AFD(estados, alfabeto, transicoes, estado_inicial, estados_finais)

    @staticmethod
    def criar_afn(estados_str: str, alfabeto_str: str, estado_inicial_str: str,
                  estados_finais_str: str, transicoes_str: str) -> AFN:
        """
        Cria um AFN a partir de strings de entrada

        Formato de transição: estado_origem,símbolo,estado_destino1,estado_destino2,...
        Use vazio no símbolo para ε-transição: estado_origem,,estado_destino

        Args:
            estados_str: "q0,q1,q2"
            alfabeto_str: "a,b"
            estado_inicial_str: "q0"
            estados_finais_str: "q2"
            transicoes_str: "q0,a,q0,q1\nq0,,q1\n..."

        Returns:
            AFN: Autômato criado
        """
        # Processar entrada
        estados = set(e.strip() for e in estados_str.split(',') if e.strip())
        alfabeto = set(s.strip() for s in alfabeto_str.split(',') if s.strip())
        estado_inicial = estado_inicial_str.strip()
        estados_finais = set(e.strip() for e in estados_finais_str.split(',') if e.strip())

        # Processar transições
        transicoes: Dict[Tuple[str, Optional[str]], Set[str]] = {}
        linhas = transicoes_str.strip().split('\n')

        for i, linha in enumerate(linhas, 1):
            linha = linha.strip()
            if not linha or linha.startswith('#'):
                continue

            partes = [p.strip() for p in linha.split(',')]
            if len(partes) < 3:
                raise ValueError(f"Linha {i}: formato inválido. Use: estado_origem,símbolo,destino1,destino2,...")

            estado_origem = partes[0]
            simbolo = partes[1] if partes[1] else None  # None = ε
            destinos = set(partes[2:])

            if estado_origem not in estados:
                raise ValueError(f"Linha {i}: estado '{estado_origem}' não existe")

            for destino in destinos:
                if destino not in estados:
                    raise ValueError(f"Linha {i}: estado destino '{destino}' não existe")

            if simbolo is not None and simbolo not in alfabeto:
                raise ValueError(f"Linha {i}: símbolo '{simbolo}' não está no alfabeto")

            chave = (estado_origem, simbolo)
            if chave not in transicoes:
                transicoes[chave] = set()
            transicoes[chave] |= destinos

        if not transicoes:
            raise ValueError("Nenhuma transição foi definida")

        return AFN(estados, alfabeto, transicoes, estado_inicial, estados_finais)

    @staticmethod
    def criar_apd(estados_str: str, alfabeto_str: str, estado_inicial_str: str,
                  estados_finais_str: str, transicoes_str: str,
                  alfabeto_pilha_str: str = "Z,a,b") -> APD:
        """
        Cria um APD a partir de strings de entrada

        Formato de transição: estado,símbolo,topo_pilha,novo_estado,operacao_pilha
        Use vazio para ε-transição: estado,,topo_pilha,novo_estado,operacao_pilha

        Args:
            estados_str: "q0,q1,q2"
            alfabeto_str: "a,b"
            estado_inicial_str: "q0"
            estados_finais_str: "q2"
            transicoes_str: "q0,a,Z,q0,aZ\nq0,b,a,q1,\n..."
            alfabeto_pilha_str: "Z,a,b"

        Returns:
            APD: Autômato criado
        """
        # Processar entrada
        estados = set(e.strip() for e in estados_str.split(',') if e.strip())
        alfabeto = set(s.strip() for s in alfabeto_str.split(',') if s.strip())
        alfabeto_pilha = set(s.strip() for s in alfabeto_pilha_str.split(',') if s.strip())
        estado_inicial = estado_inicial_str.strip()
        estados_finais = set(e.strip() for e in estados_finais_str.split(',') if e.strip())

        # Processar transições
        transicoes: Dict[Tuple[str, Optional[str], Optional[str]], List[Tuple[str, List[str]]]] = {}
        linhas = transicoes_str.strip().split('\n')

        for i, linha in enumerate(linhas, 1):
            linha = linha.strip()
            if not linha or linha.startswith('#'):
                continue

            partes = [p.strip() for p in linha.split(',')]
            if len(partes) < 4:
                raise ValueError(f"Linha {i}: formato inválido. Use: estado,símbolo,topo_pilha,novo_estado,operacoes")

            estado_origem = partes[0]
            simbolo = partes[1] if partes[1] else None
            topo_pilha = partes[2]
            novo_estado = partes[3]
            operacoes = list(partes[4]) if len(partes) > 4 and partes[4] else []

            if estado_origem not in estados:
                raise ValueError(f"Linha {i}: estado '{estado_origem}' não existe")
            if novo_estado not in estados:
                raise ValueError(f"Linha {i}: novo estado '{novo_estado}' não existe")
            if topo_pilha not in alfabeto_pilha:
                raise ValueError(f"Linha {i}: símbolo de pilha '{topo_pilha}' não existe")
            if simbolo is not None and simbolo not in alfabeto:
                raise ValueError(f"Linha {i}: símbolo '{simbolo}' não está no alfabeto")

            chave = (estado_origem, simbolo, topo_pilha)
            if chave not in transicoes:
                transicoes[chave] = []
            transicoes[chave].append((novo_estado, operacoes))

        if not transicoes:
            raise ValueError("Nenhuma transição foi definida")

        return APD(estados, alfabeto, alfabeto_pilha, transicoes,
                   estado_inicial, estados_finais)