# lexer_webapp.py
import streamlit as st
import pandas as pd
import ply.lex as lex
import base64
import sys

# ----------------------------
# Lexer setup
# ----------------------------

# List of token names
TOKENS = [
    'T_PY_DEF', 'T_PY_CLASS', 'T_PY_KEYWORD',
    'T_CPP', 'T_CPP_INCLUDE', 'T_CPP_PRINT',
    'T_JAVA',
    'T_FUNC_DEF', 'T_FUNC_DECL', 'T_FUNC_CALL',
    'T_VAR_DECL', 'T_ASSIGN', 'T_RETURN', 'T_IDENT_OR_NUM',
    'T_IF', 'T_FOR', 'T_WHILE',
    'T_ACCESS', 'T_CLASS'
]

# Regex rules for tokens
t_T_PY_DEF      = r'\bdef\s+[A-Za-z_]\w*\s*\([^)]*\)\s*:'
t_T_PY_CLASS    = r'\bclass\s+[A-Za-z_]\w*\s*:'
t_T_PY_KEYWORD  = r'\b(self|pass|try|except)\b'

t_T_CPP         = r'\b(namespace|using|std|virtual|cin|cout|>>|<<)\b'
t_T_CPP_INCLUDE = r'\#include\s*<[^>]+>'
t_T_CPP_PRINT   = r'\bcout\s*(<<\s*(?:".*?"|\w+)*)+;?'

t_T_JAVA        = r'\b(static|abstract|package|@Override|super|this\.\w+)\b'

t_T_FUNC_DEF    = r'\b(?:int|float|char|void)\s+\w+\s*\([^)]*\)\s*\{'
t_T_FUNC_DECL   = r'\b(?:int|float|char|void)\s+\w+\s*\([^)]*\)\s*;'
t_T_FUNC_CALL   = r'\b\w+\s*\([^)]*\)\s*;?'

t_T_VAR_DECL    = r'\b(?:int|float|char)\s+\w+(?:\s*=\s*[^;]+)?;?'
t_T_ASSIGN      = r'\w+\s*='
t_T_RETURN      = r'\breturn\b'
t_T_IDENT_OR_NUM= r'\b[A-Za-z_]\w*\b|\b\d+\b'

t_T_IF          = r'\bif\b|\belse\b'
t_T_FOR         = r'\bfor\s*\([^)]*\)\s*\{'
t_T_WHILE       = r'\bwhile\s*\([^)]*\)\s*\{'

t_T_ACCESS      = r'\b(public|private|protected)\b'
t_T_CLASS       = r'\bclass\s+\w+\s*\{'

# Ignore spaces and tabs
t_ignore = ' \t\r\n'

def t_error(t):
    t.lexer.skip(1)

# Force a __file__ attribute so PLY can locate this module
sys.modules[__name__].__file__ = 'lexer_webapp.py'
lexer = lex.lex(module=sys.modules[__name__], debug=False)

# ----------------------------
# Tokenization & Detection
# ----------------------------

def analyze_code(source: str):
    lexer.input(source)
    out = []
    while True:
        token = lexer.token()
        if not token:
            break
        out.append((token.type, token.value))
    return out

def language_from(tokens):
    types = {t for t, _ in tokens}
    results = []
    if 'T_CPP_INCLUDE' in types:
        results.append('C++')
    if 'T_PY_DEF' in types:
        results.append('Python')
    if 'T_JAVA' in types:
        results.append('Java')
    return results or ['Unknown']

# ----------------------------
# Streamlit UI
# ----------------------------

def make_download_link(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="tokens.csv">Download Tokens CSV</a>'

def main():
    st.set_page_config(page_title="Lexer Demo", layout="wide")
    st.header("📜 Programming Language Lexer")
    code = st.text_area("Paste your code here:", height=300)

    if st.button("Tokenize"):
        tokens = analyze_code(code)
        df = pd.DataFrame(tokens, columns=["Token Type", "Lexeme"])
        st.dataframe(df, width=700, height=300)
        st.markdown(make_download_link(df), unsafe_allow_html=True)

        langs = language_from(tokens)
        if 'Unknown' in langs:
            st.warning("Could not determine language.")
        else:
            st.success(f"Detected: {', '.join(langs)}")

if __name__ == "__main__":
    main()
