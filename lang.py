import streamlit as st
import pandas as pd
import base64
from la import lexer

def run_lexer_on(code_str: str):
    """Tokenize the input string and return a list of tokens."""
    lexer.input(code_str)
    toks = []
    while True:
        token = lexer.token()
        if not token:
            break
        toks.append(token)
    return toks

def make_download_link(df: pd.DataFrame, fname: str = "lexer_output.csv") -> str:
    """Generate a Markdown link to download a DataFrame as CSV."""
    csv_txt = df.to_csv(index=False)
    b64 = base64.b64encode(csv_txt.encode()).decode()
    return (
        f'<a href="data:file/csv;base64,{b64}" '
        f'download="{fname}">Download CSV file</a>'
    )

def detect_language(tokens):
    """Use the same detection logic as before, but refactored."""
    base_tokens = {
        'FUNCTION_DEF', 'FUNCTION_CALL', 'VAR_DECL', 'ASSIGN',
        'RETURN', 'CALCULATION_OR_IDENTIFIER', 'BRANCH',
        'FOR_LOOP', 'WHILE_LOOP', 'ACCESS_SPECIFIERS',
        'FUNCTION_DECL', 'CLASS'
    }
    types = {t.type for t in tokens}
    all_common = types.issubset(base_tokens)
    has_class = 'CLASS' in types

    cpp_set = base_tokens | {'CPP', 'CPP_INCLUDE', 'CPP_PRINT'}
    py_set = base_tokens | {'PYTHON', 'PYTHON_DEF', 'PYTHON_CLASS'}
    java_set = base_tokens | {'JAVA'}

    if all_common and has_class:
        return "C++ and Java"
    if all_common:
        return "C++, Java and Python"
    if types.issubset(cpp_set):
        return "C++"
    if types.issubset(py_set):
        return "Python"
    if types.issubset(java_set):
        return "Java"
    return None

def main():
    st.set_page_config(page_title="Programming Language Lexer",
                       page_icon="💻", layout="centered")
    st.title("Programming Language Lexer by Hema Raju")

    source_code = st.text_area(
        "Enter code below:",
        value=DEFAULT_SAMPLE,
        height=300
    )

    if st.button("Run Lexer"):
        token_list = run_lexer_on(source_code)
        df = pd.DataFrame(
            [(tok.type, tok.value) for tok in token_list],
            columns=["Token Type", "Token Value"]
        )

        st.dataframe(df, use_container_width=True)
        st.markdown(make_download_link(df), unsafe_allow_html=True)

        lang = detect_language(token_list)
        if lang:
            st.success(f"Detected language(s): {lang}")
        else:
            st.warning("Unable to detect the language.")

if __name__ == "__main__":
    DEFAULT_SAMPLE = """
def abc():
    a = b + c
    return a
"""
    main()
