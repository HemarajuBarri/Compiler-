import ply.lex as lex
import sys
SYMBOLS=(
 'P_DEF','P_CLASS','P_KEY',
 'C_KEY','C_INC','C_OUT',
 'J_KEY',
 'F_DEF','F_DCL','F_CALL',
 'V_DCL','OP_ASG','K_RET','ID_NUM',
 'KW_IF','KW_FOR','KW_WH',
 'ACC','CLS',
)

P_DEF = r'\bdef\s+[_A-Za-z]\w*\s*\([^)]*\)\s*:'
P_CLASS = r'\bclass\s+[_A-Za-z]\w*\s*:'
P_KEY = r'\b(self|pass|try|except)\b'
C_KEY = r'\b(namespace|using|std|virtual|cin|cout|>>|<<)\b'
C_INC = r'\#include\s*<[^>]+>'
C_OUT = r'\bcout\s*(<<\s*(?:\".*?\"|\w+)*)+;?'
J_KEY = r'\b(static|abstract|package|@Override|super|this\.\w+)\b'
F_DEF = r'\b(?:int|float|char|void)\s+\w+\s*\([^)]*\)\s*\{'
F_DCL = r'\b(?:int|float|char|void)\s+\w+\s*\([^)]*\)\s*;'
F_CALL = r'\b\w+\s*\([^)]*\)\s*;?'
V_DCL = r'\b(?:int|float|char)\s+\w+(?:\s*=\s*[^;]+)?;?'
OP_ASG = r'\w+\s*='
K_RET = r'\breturn\b'
ID_NUM = r'\b[A-Za-z_]\w*\b|\b\d+\b'
KW_IF = r'\bif\b|\belse\b'
KW_FOR = r'\bfor\s*\([^)]*\)\s*\{'
KW_WH = r'\bwhile\s*\([^)]*\)\s*\{'
ACC = r'\b(public|private|protected)\b'
CLS = r'\bclass\s+\w+\s*\{'

tokens=SYMBOLS
t_ignore=' \t\n'

def t_error(t):t.lexer.skip(1)
sys.modules[__name__].__file__='lexer_tool_obf.py'
lex.lex(module=sys.modules[__name__])

def analyze(txt):
    lex_obj=lex.lex(module=sys.modules[__name__])
    lex_obj.input(txt)
    out=[]
    while True:
        tk=lex_obj.token()
        if not tk:break
        out.append((tk.type,tk.value))
    return out

def detect(lst):
    s={x for x,_ in lst}
    res=[]
    if 'C_INC' in s:res.append('C++')
    if 'P_DEF' in s:res.append('Python')
    if 'J_KEY' in s:res.append('Java')
    return res or ['Unknown']

if __name__=='__main__':
    src='''def fn():\n x=1\n return x'''
    tk=analyze(src)
    print(tk,detect(tk))
