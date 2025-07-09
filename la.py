import ply.lex as lex
tokens = (
    'IMPORT',
    'CPP_PRINT',
    'JAVA_PRINT',               
    'VAR_DECL',
    'FUNCTION_DECL',
    'CLASS_DEF',
    'BRANCH',
    'SEMICOLON',
    'RETURN',
    'CALCULATION_OR_IDENTIFIER',
    'PYTHON_DEF',
    'DECORATOR',
    'COMMENT',
    'COMMA',
    'NUMBER',
    'ASSIGN',
    'CPP_INCLUDE',
    'WHILE_LOOP',
    'FUNCTION_DEF',
    'ACCESS_SPECIFIERS',
    'CPP',
    'PYTHON',
    'JAVA',
    'FOR_LOOP',
    'CLASS',
    'PYTHON_CLASS',
    'FUNCTION_CALL',
    'STRING_LITERAL',
)

def t_IMPORT(t):
    r'import\s+[a-zA-Z_][\w\.]*'
    return t

def t_COMMENT(t):
    r'//.*|\#.*'
    return t

def t_COMMA(t):
    r','
    return t

def t_SEMICOLON(t):
    r';'
    return t

def t_STRING_LITERAL(t):
    r'"([^\\\n]|(\\.)*?)"'
    return t

def t_NUMBER(t):
    r'\b\d+\b'
    return t

def t_ASSIGN(t):
    r'[a-zA-Z_]\w*\s*='
    t.value = t.value.rstrip('\n')
    return t

def t_CPP_INCLUDE(t):
    r'\#include\s*<.*?>'
    return t

def t_CPP_PRINT(t):
    r'\bcout\s*(<<\s*(?:[a-zA-Z_]\w*|"([^"]*)"))*\s*(<<endl)*;?'
    return t

def t_JAVA_PRINT(t):
    r'\bSystem\.out\.print(?:ln)?\s*\(\s*(?:.+?)?\s*\);?'
    return t

def t_PYTHON_DEF(t):
    r'\bdef\b\s+[a-zA-Z_]\w*\s*\(\s*\)\s*:\s*'
    return t

def t_FUNCTION_DEF(t):
    r'\b(?:int|float|char|void)\s+[a-zA-Z_]\w*\s*\(\s*(?:[a-zA-Z_]\w*\s+[a-zA-Z_]\w*\s*)*\)\s*{'
    return t

def t_PYTHON_CLASS(t):
    r'class\s+[a-zA-Z_]\w*\s*:'
    return t

def t_CLASS(t):
    r'\bclass\b\s+[a-zA-Z_]\w*\s*(\([^)]*\))?\s*{'
    return t

def t_FOR_LOOP(t):
    r'\bfor\s*\(\s*.*?\s*\)\s*{'
    return t

def t_WHILE_LOOP(t):
    r'\bwhile\s*\(\s*.*?\s*\)\s*{'
    return t

def t_BRANCH(t):
    r'\b(if|else\sif)\b\(\s*(.*?)\s*\){? |else'
    return t

def t_FUNCTION_CALL(t):
    r'\b(?:[a-zA-Z_]\w*\.)*[a-zA-Z_]\w*\(\s*(?:.+?)?\s*\);?'
    return t

def t_FUNCTION_DECL(t):
    r'\b(int|float|char|void)\s+[a-zA-Z_]\w*\(\s*(?:.+?)?\s*\);?'
    return t

def t_VAR_DECL(t):
    r'\b(?:int|float|char)\s+[a-zA-Z_]\w*\s*(?:=\s*\S+)?\s*;?'
    return t

def t_RETURN(t):
    r'\breturn\b\s+([a-zA-Z_]|\d+)\w*(\s*[\+\-%\*/]\s*([a-zA-Z_]|\d+)\w*)*\s*;?'
    return t

def t_CALCULATION_OR_IDENTIFIER(t):
    r'([a-zA-Z_]|\d+)\w*(\s*[\+\-%\*/]\s*([a-zA-Z_]|\d+)\w*)*\s*;?'
    return t

def t_PYTHON(t):
    r'\b(self|pass|except|try)\b'
    return t

def t_CPP(t):
    r'\b(this->[a-zA-Z_]\w*|virtual|cin|using|namespace|std|<<|>>)\b[a-zA-Z_]?;?'
    return t

def t_JAVA(t):
    r'\b(finally|super|this\.[a-zA-Z_]\w*|@Override|static|abstract|package)\b;?'
    return t

def t_ACCESS_SPECIFIERS(t):
    r'\b(public|private|protected)\b'
    return t

t_ignore = ' \t\n}'

def t_error(t):
    print(f"Invalid character: {t.value[0]}")
    t.lexer.skip(1)
lexer = lex.lex()

def test_lexer(data):
    lexer.input(data)
    result = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)
        result.append(tok)
    return result
