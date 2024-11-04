import re
from src.errors import LexicalError
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Definición de patrones de tokens
token_patterns = {
    'PRINT': r'print',
    'STRING': r'"[^"]*"',
    'LPAREN': r'\(',
    'RPAREN': r'\)',
    'INVALID': r'[^\s]+'
}

def lex(code):
    tokens = []
    lines = code.splitlines()
    for line_num, line in enumerate(lines, start=1):
        for token_name, pattern in token_patterns.items():
            match = re.match(pattern, line)
            if match:
                if token_name == 'INVALID':
                    raise LexicalError(f"Error léxico en línea {line_num}: token '{match.group()}' inválido.")
                tokens.append((token_name, match.group()))
                line = line[match.end():]  # Avanzar al siguiente token en la línea
    return tokens
