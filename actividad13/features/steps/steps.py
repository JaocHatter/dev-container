from behave import given, when, then
from src.lexer import lex
from src.parser import parse
from src.executor import execute_code
from src.errors import LexicalError, SyntaxError

@given('el código fuente es:\n{code}')
def step_given_code(context, code):
    context.code = code

@when('el compilador ejecuta el código')
def step_when_execute(context):
    try:
        tokens = lex(context.code)
        parse(tokens)
        context.result = execute_code(tokens)
    except (LexicalError, SyntaxError) as e:
        context.result = str(e)

@then('el resultado debe ser:\n{expected_result}')
def step_then_result(context, expected_result):
    assert context.result.strip() == expected_result.strip()
