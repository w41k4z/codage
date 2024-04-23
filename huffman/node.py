from typing import Literal

class Node:
    
    def __init__(self, symbol: chr, value: float, parent: 'Node', position: Literal['1', '0']) -> None:
        self.symbol = symbol
        self.value = value
        self.parent = parent
        self.position = position