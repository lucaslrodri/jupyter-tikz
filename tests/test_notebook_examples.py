from IPython.testing.globalipapp import get_ipython
from IPython.display import SVG, Image

ipy = get_ipython()
ipy.run_line_magic("load_ext", "jupyter_tikz")


# ================= BASIC USAGE =================

# Create a simple `tikzpicture`:

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


# Or write full document by passing parameter `-f` (or `--full-document`):

EXAMPLE_FULL_DOCUMENT = r"""
\documentclass[tikz]{standalone}
\begin{document}
    \begin{tikzpicture}
        \draw[help lines] grid (5, 5);
        \draw[fill=red] (1, 1) rectangle (2, 2);
        \draw[fill=red] (2, 1) rectangle (3, 2);
        \draw[fill=red] (3, 1) rectangle (4, 2);
        \draw[fill=red] (3, 2) rectangle (4, 3);
        \draw[fill=red] (2, 3) rectangle (3, 4);
    \end{tikzpicture}
\end{document}
"""


def test_example_full_document():
    line = "-f"
    cell = EXAMPLE_FULL_DOCUMENT

    res = ipy.run_cell_magic("tikz", line, cell)

    assert isinstance(res, SVG)


# You can implictly wrap the code in a standalone document with `tikzpicture` enviroment:

EXAMPLE_IMPLICIT_PIC = r"""
\draw[help lines] grid (5, 5);
\draw[fill=magenta!10] (1, 1) rectangle (2, 2);
\draw[fill=magenta!10] (2, 1) rectangle (3, 2);
\draw[fill=magenta!10] (3, 1) rectangle (4, 2);
\draw[fill=magenta!10] (3, 2) rectangle (4, 3);
\draw[fill=magenta!10] (2, 3) rectangle (3, 4);
"""


def test_example_implicit_pic():
    line = "-i"
    cell = EXAMPLE_IMPLICIT_PIC

    res = ipy.run_cell_magic("tikz", line, cell)

    assert isinstance(res, SVG)


# ================= LOADING PACKAGES AND LIBRARIES =================

# If you not using the flag `-f` (or `--full-document`), it's often usefull to use ...

EXAMPLE_LOADING_PACKAGES_AND_LIBRARIES = r"""
% Example from Paul Gaborit
% http://www.texample.net/tikz/examples/angles-quotes/
\draw
    (3,-1) coordinate (a) node[right] {a}
    -- (0,0) coordinate (b) node[left] {b}
    -- (2,2) coordinate (c) node[above right] {c};
"""


def test_example_loading_packages_and_libraries():
    line = "-i -l=quotes,angles -t=amsfonts"
    cell = EXAMPLE_LOADING_PACKAGES_AND_LIBRARIES

    res = ipy.run_cell_magic("tikz", line, cell)

    assert isinstance(res, SVG)


# If you don't want to import `tikz` package you can use the flag `-nt` (or `--no-tikz`):

EXAMPLE_PGFPLOTS_NO_TIKZ = r"""
\begin{axis}[
    title={Box Plot Example},
    boxplot/draw direction=y,
    ylabel={Values},
    xtick={1,2,3},
    xticklabels={Sample A, Sample B, Sample C},
]
% Sample A
\addplot+[
    boxplot prepared={
        median=3,
        upper quartile=4.5,
        lower quartile=2,
        upper whisker=6,
        lower whisker=1,
    },
] coordinates {};
\end{axis}
"""


def test_example_pgfplots_no_tikz():
    line = " -i -nt -t=pgfplots --pgfplots-libraries=statistics"
    cell = EXAMPLE_PGFPLOTS_NO_TIKZ

    res = ipy.run_cell_magic("tikz", line, cell)

    assert isinstance(res, SVG)


# ================= PREAMBLE =================

# Cannot test the preamble because it's not possible to access the preamble from the cell magic

# ================= SCALE =================

# You can scale the Tikz image using the `-sc` (or `--scale`) parameter:
# Note: It uses `\boxscale` from the `graphicx` package

EXAMPLE_SCALE = r"""
\draw[help lines] grid (5, 5);
\draw[fill=my_color] (1, 1) rectangle (2, 2);
\draw[fill=my_color] (3, 1) rectangle (4, 2);
\draw[fill=my_color] (2, 2) rectangle (3, 3);
\draw[fill=my_color] (2, 3) rectangle (3, 4);
"""


def test_example_scale():
    line = "-i -sc=2"
    cell = EXAMPLE_SCALE

    res = ipy.run_cell_magic("tikz", line, cell)

    assert isinstance(res, SVG)


# Also works in standalone output:
# Note: not applicable with the `-f` (or `--full-document`) parameter

EXAMPLE_STANDALONE_SCALE = r"""
\begin{tikzpicture}
    \draw[help lines] grid (5, 5);
    \draw[fill=black!50] (1, 1) rectangle (2, 2);
    \draw[fill=black!50] (2, 1) rectangle (3, 2);
    \draw[fill=black!50] (3, 1) rectangle (4, 2);
    \draw[fill=black!50] (3, 2) rectangle (4, 3);
    \draw[fill=black!50] (2, 3) rectangle (3, 4);
\end{tikzpicture}
"""


def test_example_scale():
    line = "-sc=0.75"
    cell = EXAMPLE_STANDALONE_SCALE

    res = ipy.run_cell_magic("tikz", line, cell)

    assert isinstance(res, SVG)


# ============= IPYTHON STRINGS ===============

# Cannot test the IPython strings because it's not possible to access the IPython strings from the cell magic

# =========== DEBUGGING AND ERROR =============

# If you write an invalid Tikz code, it will show a LaTeX error message limited in 20 lines

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


# If you want to see the full error message, you can use the `-e` (or `--full-error`) parameter:


def test_example_show_full_error(capsys):
    line = "-i -e"
    cell = EXAMPLE_SHOW_ERROR

    res = ipy.run_cell_magic("tikz", line, cell)
    _, err = capsys.readouterr()

    assert res is None
    assert "error" in err.lower()
    assert len(err.splitlines()) > 20
