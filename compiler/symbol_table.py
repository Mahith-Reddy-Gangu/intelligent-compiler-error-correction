from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional


@dataclass(frozen=True)
class SymbolInfo:
    name: str
    declared_line: int


class SymbolTable:
    """
    Minimal symbol table for demo purposes.
    Stores first declaration line of each variable.
    """
    def __init__(self):
        self._symbols: Dict[str, SymbolInfo] = {}

    def declare(self, name: str, line: int) -> bool:
        if name in self._symbols:
            return False
        self._symbols[name] = SymbolInfo(name=name, declared_line=line)
        return True

    def is_declared(self, name: str) -> bool:
        return name in self._symbols

    def declared_line(self, name: str) -> Optional[int]:
        info = self._symbols.get(name)
        return info.declared_line if info else None

    def items(self) -> List[Tuple[str, int]]:
        """
        Compatibility helper for printing:
        returns list of (name, declared_line)
        """
        return [(n, info.declared_line) for n, info in self._symbols.items()]

    def to_dict(self) -> Dict[str, int]:
        return {n: info.declared_line for n, info in self._symbols.items()}