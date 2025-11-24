from typing import Protocol

class Automata(Protocol):

    def setup(self, ini_state: str, fin_state: str, transitions: str) -> None: ...

    def run(self) -> bool: ...


