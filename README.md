Programming-Language Lexer (Streamlit)
A tiny compiler-design sandbox that lets you **see how a lexer chops up source code**.  
Powered by Python Lex-Yacc (PLY) on the backend and Streamlit on the frontend.

What it does
Multi-language tokenisation** – Handles Python, C/C++, and Java snippets.
Detailed token output – Shows keywords, identifiers, literals, operators, braces, etc.
Instant feedback – Paste code in the browser, hit Analyse, and watch the tokens appear.

Repo layout
| File | Purpose |
|------|---------|
| `lang.py` | Streamlit UI (text box + token table) |
| `la.py`   | PLY lexer rules – add/modify regexes here |
| `requirements.txt` | App dependencies |
| `runtime.txt` | Pins Python 3.11 for smooth install on Streamlit Cloud |

All token definitions live in la.py.
Add new regex functions or tweak existing ones to support more languages or constructs. Changes hot-reload when you restart the Streamlit app.

The app is already hosted on Streamlit Community Cloud:
https://compilerdesign.streamlit.app
