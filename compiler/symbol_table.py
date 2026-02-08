class SymbolTable:
    def __init__(self):
        self._symbols = {}

    def declare(self, name: str, line: int) -> bool:
        if name in self._symbols:
            return False
        self._symbols[name] = line
        return True

    def is_declared(self, name: str) -> bool:
        return name in self._symbols

    def items(self):
        return list(self._symbols.items())
