from src.errors import SyntaxError

def parse(tokens):
    if not tokens:
        raise SyntaxError("Error sintáctico: código vacío.")
    
    # Reglas simples de la gramática para este lenguaje básico
    expected = ['PRINT', 'LPAREN', 'STRING', 'RPAREN']
    if [token[0] for token in tokens] != expected:
        raise SyntaxError("Error sintáctico: se esperaba 'print(\"string\")'.")
