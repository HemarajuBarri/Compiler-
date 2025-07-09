import streamlit as st
import pandas as pd
import base64
from la import lexer

def tokenize(code: str):
    """Feed code into the lexer and collect all tokens."""
    lexer.input(code)
    toks = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        toks.append(tok)
    return toks

def make_csv_download(df: pd.DataFrame, filename: str = "lexer_output.csv") -> str:
    """Return a Markdown link to download the DataFrame as CSV."""
    csv_str = df.to_csv(index=False)
    b64 = base64.b64encode(csv_str.encode()).decode()
    return (
        f'<a href="data:file/csv;base64,{b64}" '
        f'download="{filename}">Download CSV</a>'
    )

def detect_languages(tokens):
    """Given a list of tokens, return a list of possible languages."""
    common = {
        'FUNCTION_DEF', 'FUNCTION_CALL', 'VAR_DECL', 'ASSIGN',
        'RETURN', 'CALCULATION_OR_IDENTIFIER',
        'BRANCH', 'FOR_LOOP', 'WHILE_LOOP',
        'ACCESS_SPECIFIERS', 'FUNCTION_DECL', 'CLASS'
    }
    lang_rules = {
        'C++': common | {'CPP', 'CPP_INCLUDE', 'CPP_PRINT'},
        'Java': common | {'JAVA'},
        'Python': common | {'PYTHON', 'PYTHON_DEF', 'PYTHON_CLASS'},
    }
    types = {tok.type for tok in tokens}
    detected = []
    for lang, allowed in lang_rules.items():
        if types and types.issubset(allowed) and types & common:
            detected.append(lang)
    return detected

def main():
    st.set_page_config(
        page_title="Programming Language Lexer",
        page_icon="💻",
        layout="centered"
    )
    st.title("Programming Language Lexer")

    code_input = st.text_area(
        "Paste your code here:",
        value=default_code,
        height=300
    )

    if st.button("Run Lexer"):
        tokens = tokenize(code_input)
        df = pd.DataFrame(
            [(t.type, t.value) for t in tokens],
            columns=["Token Type", "Token Value"]
        )

        # Display the table
        st.dataframe(df, use_container_width=True)

        # Download link
        link = make_csv_download(df)
        st.markdown(link, unsafe_allow_html=True)

        # Language detection
        langs = detect_languages(tokens)
        if langs:
            st.success("Detected language(s): " + ", ".join(langs))
        else:
            st.warning("Unable to detect the language.")

if __name__ == "__main__":
    default_code = '''
    def abc():
        a = b + c
        return a
    '''
    main()
