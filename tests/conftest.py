from hashlib import md5

import pytest

from jupyter_tikz import TexDocument

EXAMPLE_BAD_TIKZ = "HELLO WORLD"

EXAMPLE_GOOD_TEX = r"""
\documentclass[tikz]{standalone}
\begin{document}
    \begin{tikzpicture}
        \draw[fill=blue] (0, 0) rectangle (1, 1);
    \end{tikzpicture}
\end{document}"""

HASH_EXAMPLE_GOOD_TEX = md5(EXAMPLE_GOOD_TEX.strip().encode()).hexdigest()

# LATEX_CODE = r"""\documentclass{standalone}
# \usepackage{tikz}
# \begin{document}
# \begin{tikzpicture}
#     \draw[fill=blue] (0, 0) rectangle (1, 1);
# \end{tikzpicture}
# \end{document}"""

TIKZ_CODE = r"""\begin{tikzpicture}
    \draw[fill=blue] (0, 0) rectangle (1, 1);
\end{tikzpicture}"""

EXAMPLE_TIKZ_BASIC_STANDALONE = r"\draw[fill=blue] (0, 0) rectangle (1, 1);"

RENDERED_SVG_PATH_GOOD_TIKZ = "M -0.00195486 -0.00189963 L -0.00195486 28.345014 L 28.344959 28.345014 L 28.344959 -0.00189963 Z M -0.00195486 -0.00189963"

EXAMPLE_VIEWBOX_CODE_INPUT = r"""
\draw (-2.5,-2.5) rectangle (5,5);
"""
EXAMPLE_PARENT_WITH_INPUT_COMMANDT = r"""
\documentclass[tikz]{standalone}
\begin{document}
    \begin{tikzpicture}
        \input{viewbox.tex}
        \node[draw] at (0,0) {Hello, World!};
    \end{tikzpicture}
\end{document}    
"""

EXAMPLE_JINJA_TEMPLATE = r"""
\documentclass[tikz]{standalone}
\begin{document}
    \begin{tikzpicture}
        (~ A Jinja Template Commentary ~)
        (** for person in people **)
        \node[draw] at (0,(* person.y *)) {Hello, (* person.name *)!};
        (** endfor **)
    \end{tikzpicture}
\end{document}"""

DUMMY_COMMAND = "dummy_command"

ANY_CODE_HASH = md5("any code".encode()).hexdigest()
ANY_CODE = "any code"


@pytest.fixture
def tex_document():
    return TexDocument(ANY_CODE)
