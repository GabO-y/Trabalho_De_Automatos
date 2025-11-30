# Simulador de Autômatos e Máquina de Turing

Simuladores educacionais para Autômatos Finitos Determinísticos (AFD), Autômatos Finitos Não-Determinísticos (AFN), Autômatos a Pilha (APN) e Máquina de Turing (MT), desenvolvidos para a disciplina de Linguagens Formais e Autômatos.

## Descrição

Este projeto implementa simuladores completos com interface gráfica para diferentes modelos computacionais, permitindo a visualização passo a passo da execução e facilitando o entendimento dos conceitos de teoria da computação.

## Funcionalidades

### 1. Autômato Finito Determinístico (AFD)
- Reconhece linguagens regulares
- Simulação determinística com um único caminho
- Validação completa de transições
- Visualização de cada passo da execução

### 2. Autômato Finito Não-Determinístico (AFN)
- Reconhece linguagens regulares
- Suporte a não-determinismo
- Transições epsilon (lambda)
- Cálculo automático de epsilon-fecho
- Exploração de múltiplos caminhos

### 3. Autômato a Pilha (APN)
- Reconhece linguagens livres de contexto
- Estrutura de pilha com operações push/pop
- Transições baseadas em estado, entrada e topo da pilha
- Aceitação por estado final ou pilha vazia
- Visualização do estado da pilha em cada passo

### 4. Máquina de Turing (MT)
- Modelo computacional universal
- Fita infinita em ambas as direções
- Movimentação da cabeça de leitura/escrita (L/R)
- Função de transição completa
- Detecção de loops infinitos
- Visualização da fita em cada passo

## Requisitos

- Python 3.8 ou superior
- Tkinter (geralmente incluído com Python)

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/simulador-automatos.git
cd simulador-automatos
```

2. (Opcional) Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Execute os simuladores:
```bash
# Simulador de Autômatos (AFD, AFN, APN)
python gui_automatos.py

# Simulador de Máquina de Turing
python maquina_turing.py
```

## Estrutura do Projeto

```
simulador-automatos/
├── automato_base.py          # Classe base abstrata para autômatos
├── afd.py                     # Implementação do AFD
├── afn.py                     # Implementação do AFN
├── apd.py                     # Implementação do APN
├── criador_automatos.py      # Factory para criar autômatos
├── gui_automatos.py          # Interface gráfica para autômatos
├── maquina_turing.py         # Implementação completa da MT
├── README.md                  # Este arquivo
└── relatorio.md              # Relatório técnico completo
```

## Como Usar

### Simulador de Autômatos

1. Execute `python gui_automatos.py`
2. Selecione o tipo de autômato (AFD, AFN ou APN)
3. Preencha os campos:
   - Estados (separados por vírgula)
   - Alfabeto (separado por vírgula)
   - Estado inicial
   - Estados finais
   - Transições (uma por linha)
4. Clique em "Criar Automato"
5. Digite a cadeia de entrada
6. Clique em "Simular"

### Simulador de Máquina de Turing

1. Execute `python maquina_turing.py`
2. Preencha a definição formal:
   - Q (estados)
   - Sigma (alfabeto de entrada)
   - Gamma (alfabeto da fita)
   - q0 (estado inicial)
   - F (estados finais)
   - delta (função de transição)
3. Clique em "Criar MT"
4. Digite a cadeia de entrada
5. Clique em "Simular"

## Exemplos

### AFD - Termina em "01"

**Configuração:**
- Estados: `q0,q1,q2`
- Alfabeto: `0,1`
- Estado inicial: `q0`
- Estados finais: `q2`
- Transições:
```
q0,0,q1
q0,1,q0
q1,0,q1
q1,1,q2
q2,0,q1
q2,1,q0
```

**Testes:**
- `01` → ACEITA
- `101` → ACEITA
- `10` → REJEITA

### AFN - Com transições epsilon

**Configuração:**
- Estados: `q0,q1,q2`
- Alfabeto: `a,b,c`
- Estado inicial: `q0`
- Estados finais: `q2`
- Transições (use vírgulas vazias para epsilon):
```
q0,a,q0,q1
q0,,q1
q1,b,q1
q1,,q2
q2,c,q2
```

**Testes:**
- `abc` → ACEITA
- `c` → ACEITA (por epsilon)
- `bac` → REJEITA

### APN - Linguagem {aⁿbⁿ}

**Configuração:**
- Estados: `q0,q1,q2`
- Alfabeto: `a,b`
- Estado inicial: `q0`
- Estados finais: `q2`
- Transições:
```
q0,a,Z,q0,Za
q0,a,a,q0,aa
q0,b,a,q1,
q1,b,a,q1,
q1,,Z,q2,Z
```

**IMPORTANTE:** A ordem dos símbolos ao empilhar é invertida (último elemento = topo).

**Testes:**
- `ab` → ACEITA
- `aabb` → ACEITA
- `aab` → REJEITA

### MT - Linguagem a*b*

**Configuração:**
- Q: `q0,q1,q2,q3`
- Sigma: `a,b`
- Gamma: `a,b,_`
- q0: `q0`
- F: `q3`
- delta:
```
q0,a,q0,a,R
q0,b,q1,b,R
q0,_,q3,_,L
q1,b,q1,b,R
q1,_,q3,_,L
```

**Testes:**
- `aabb` → ACEITA
- `aaaa` → ACEITA
- `abab` → REJEITA

## Formato das Transições

### AFD
```
estado_origem,simbolo,estado_destino
```

### AFN
```
estado_origem,simbolo,estado_destino1,estado_destino2,...
```
Use vírgula vazia para epsilon: `estado_origem,,estado_destino`

### APN
```
estado_origem,simbolo,topo_pilha,estado_destino,empilhar
```
- Use vírgula vazia para epsilon no símbolo
- `empilhar` = sequência a ser empilhada (ordem invertida: último = topo)
- Deixe vazio para apenas desempilhar

### MT
```
estado,simbolo_lido,novo_estado,simbolo_escrever,direcao
```
- `direcao` = L (esquerda) ou R (direita)

## Definições Formais

### AFD
M = (Q, Σ, δ, q₀, F)
- Q: conjunto de estados
- Σ: alfabeto de entrada
- δ: Q × Σ → Q (função de transição)
- q₀: estado inicial
- F ⊆ Q: estados finais

### AFN
M = (Q, Σ, δ, q₀, F)
- Q: conjunto de estados
- Σ: alfabeto de entrada
- δ: Q × (Σ ∪ {ε}) → P(Q) (função de transição)
- q₀: estado inicial
- F ⊆ Q: estados finais

### APN
M = (Q, Σ, Γ, δ, q₀, Z₀, F)
- Q: conjunto de estados
- Σ: alfabeto de entrada
- Γ: alfabeto da pilha
- δ: Q × (Σ ∪ {ε}) × Γ → P(Q × Γ*) (função de transição)
- q₀: estado inicial
- Z₀: símbolo inicial da pilha
- F ⊆ Q: estados finais

### MT
M = (Q, Σ, Γ, δ, q₀, blank, F)
- Q: conjunto de estados
- Σ: alfabeto de entrada
- Γ: alfabeto da fita
- δ: Q × Γ → Q × Γ × {L, R} (função de transição)
- q₀: estado inicial
- blank: símbolo branco
- F ⊆ Q: estados finais

## Características Técnicas

- **Linguagem:** Python 3.8+
- **Interface Gráfica:** Tkinter
- **Paradigma:** Programação Orientada a Objetos
- **Estruturas de Dados:**
  - Sets para conjuntos de estados
  - Dicionários para funções de transição
  - Listas para pilha e histórico
  - Dicionário para fita infinita (MT)

## Recursos Visuais

- Cores diferenciadas para aceitação (verde) e rejeição (vermelho)
- Histórico detalhado passo a passo
- Visualização da fita com indicador de posição (MT)
- Visualização do estado da pilha (APN)
- Exemplos pré-configurados
- Validação de entrada com mensagens de erro claras

## Limitações Conhecidas

- MT tem limite de 10.000 passos para evitar loops infinitos
- APN implementado executa apenas o primeiro caminho não-determinístico encontrado
- Interface gráfica básica (sem visualização de diagramas de estados)

## Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir novas funcionalidades
- Melhorar a documentação
- Adicionar novos exemplos

## Licença

Este projeto foi desenvolvido para fins educacionais como parte da disciplina de Linguagens Formais e Autômatos.

## Autores

[Adicione os nomes dos integrantes do grupo aqui]

## Referências

- SIPSER, Michael. Introduction to the Theory of Computation. 3rd ed. Cengage Learning, 2012.
- HOPCROFT, John E.; MOTWANI, Rajeev; ULLMAN, Jeffrey D. Introduction to Automata Theory, Languages, and Computation. 3rd ed. Pearson, 2006.
- MENEZES, Paulo Blauth. Linguagens Formais e Autômatos. 6ª ed. Bookman, 2011.

## Contato

[Adicione informações de contato aqui]

---

**Desenvolvido para a disciplina de Linguagens Formais e Autômatos**