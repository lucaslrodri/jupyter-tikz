from IPython.testing.globalipapp import get_ipython
from IPython.display import SVG, Image

ipy = get_ipython()
ipy.run_line_magic("load_ext", "jupyter_tikz")


EXAMPLE_SIMPLE_TIKZPICTURE = r"""
\begin{tikzpicture}
    \draw[help lines] grid (5, 5);
    \draw[fill=black] (1, 1) rectangle (2, 2);
    \draw[fill=black] (2, 1) rectangle (3, 2);
    \draw[fill=black] (3, 1) rectangle (4, 2);
    \draw[fill=black] (3, 2) rectangle (4, 3);
    \draw[fill=black] (2, 3) rectangle (3, 4);
\end{tikzpicture}
"""


def test_example_simple_tikzpicture():
    line = ""
    cell = EXAMPLE_SIMPLE_TIKZPICTURE

    res = ipy.run_cell_magic("tikz", line, cell)

    assert isinstance(res, SVG)


EXAMPLE_FULL_DOCUMENT = r"""
\documentclass[tikz]{standalone}
\begin{document}
    \begin{tikzpicture}
        \draw[help lines] grid (5, 5);
        \draw[fill=black] (1, 1) rectangle (2, 2);
        \draw[fill=black] (2, 1) rectangle (3, 2);
        \draw[fill=black] (3, 1) rectangle (4, 2);
        \draw[fill=black] (3, 2) rectangle (4, 3);
        \draw[fill=black] (2, 3) rectangle (3, 4);
    \end{tikzpicture}
\end{document}
"""


def test_example_full_document():
    line = "-f"
    cell = EXAMPLE_FULL_DOCUMENT

    res = ipy.run_cell_magic("tikz", line, cell)

    assert isinstance(res, SVG)


EXAMPLE_IMPLICIT_PIC = r"""
\draw[help lines] grid (5, 5);
\draw[fill=black] (1, 1) rectangle (2, 2);
\draw[fill=black] (2, 1) rectangle (3, 2);
\draw[fill=black] (3, 1) rectangle (4, 2);
\draw[fill=black] (3, 2) rectangle (4, 3);
\draw[fill=black] (2, 3) rectangle (3, 4);
"""


def test_example_implicit_pic():
    line = "-i"
    cell = EXAMPLE_IMPLICIT_PIC

    res = ipy.run_cell_magic("tikz", line, cell)

    assert isinstance(res, SVG)


EXAMPLE_SHOW_ERROR = r"""
% Error: Comma after the first coordinate
\draw[fill=black] (1, 1) rectangle (2, 2)
"""


def test_example_show_error(capsys):
    line = "-i"
    cell = EXAMPLE_SHOW_ERROR

    res = ipy.run_cell_magic("tikz", line, cell)
    _, err = capsys.readouterr()

    assert res is None
    assert "error" in err.lower()
    assert len(err.splitlines()) == 20


def test_example_show_full_error(capsys):
    line = "-i -e"
    cell = EXAMPLE_SHOW_ERROR

    res = ipy.run_cell_magic("tikz", line, cell)
    _, err = capsys.readouterr()

    assert res is None
    assert "error" in err.lower()
    assert len(err.splitlines()) > 20


EXAMPLE_LOADING_PACKAGES_AND_LIBRARIES = r"""
% Example from Paul Gaborit
% http://www.texample.net/tikz/examples/angles-quotes/
\draw
    (3,-1) coordinate (a) node[right] {a}
    -- (0,0) coordinate (b) node[left] {b}
    -- (2,2) coordinate (c) node[above right] {c};
"""
