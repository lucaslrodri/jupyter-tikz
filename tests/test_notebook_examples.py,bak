from IPython.display import SVG, Image
from IPython.testing.globalipapp import get_ipython

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


# Alternatively, generate TikZ output using a complete document by using the `-f` (or `--full-document`) parameter:

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


# Or, write only the content inside the `tikzpicture` environment by using the `-i` (or `--implicit-pic`) parameter. This will generate a standalone document with the `tikzpicture` environment:

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


# ================= USING PREAMBLE =================

# Not testesd because it's not possible to access the IPython strings from the line magic


# ================= LOADING PACKAGES AND LIBRARIES =================

# If you are not using the `-f` (or `--full-document`) flag, it's often useful to: ...

EXAMPLE_LOADING_PACKAGES_AND_LIBRARIES = r"""
% Example from Paul Gaborit
% http://www.texample.net/tikz/examples/angles-quotes/
\draw
    (3,-1) coordinate (a) node[right] {a}
    -- (0,0) coordinate (b) node[left] {b}
    -- (2,2) coordinate (c) node[above right] {c}
    pic["$\alpha$", draw=orange, <->, angle eccentricity=1.2, angle radius=1cm]
    {angle=a--b--c};
    
\node[rotate=10] (r) at (2.5, 0.65) {Something about in $\mathbb{R}^2$};
"""


def test_example_loading_packages_and_libraries():
    line = "-i -l=quotes,angles -t=amsfonts"
    cell = EXAMPLE_LOADING_PACKAGES_AND_LIBRARIES

    res = ipy.run_cell_magic("tikz", line, cell)

    assert isinstance(res, SVG)


# If you don't want to import the `tikz` package, you can use the flag `-nt` (or `--no-tikz`):

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


# ================= SCALE =================

# You can scale the Tikz image using the `-sc` (or `--scale`) parameter:
# Note: It uses `\boxscale` from the `graphicx` package

EXAMPLE_SCALE = r"""
\draw[help lines] grid (5, 5);
\draw[fill=black!10] (1, 1) rectangle (2, 2);
\draw[fill=black!10] (2, 1) rectangle (3, 2);
\draw[fill=black!10] (3, 1) rectangle (4, 2);
\draw[fill=black!10] (3, 2) rectangle (4, 3);
\draw[fill=black!10] (2, 3) rectangle (3, 4);
"""


def test_example_scale():
    line = "-i -sc=2"
    cell = EXAMPLE_SCALE

    res = ipy.run_cell_magic("tikz", line, cell)

    assert isinstance(res, SVG)


# Which also works with standalone documents:
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


# ================= RASTERIZE =================

# It is also possible to set the resolution (dots per inch) by using `-d=<dpi_of_image>` (or `--dpi=<dpi_of_image>`):

EXAMPLE_RASTERIZE = r"""
\begin{tikzpicture}
    \draw[help lines] grid (5, 5);
    \draw[fill=black!50] (1, 1) rectangle (2, 2);
    \draw[fill=black!50] (2, 1) rectangle (3, 2);
    \draw[fill=black!50] (3, 1) rectangle (4, 2);
\end{tikzpicture}
"""


def test_rasterize():
    line = "-r --dpi=150"
    cell = EXAMPLE_RASTERIZE

    res = ipy.run_cell_magic("tikz", line, cell)

    assert isinstance(res, Image)


# ================= SAVE ======================

# Saves tests are implemented in the test_save_path.py file


# ============= IPYTHON STRINGS ===============

# Cannot test the IPython strings because it's not possible to access the IPython strings from the cell magic

# ============= JINJA ===============

# Jinja2 tests are implemented in the test_jinja.py file

# ============== VARIABLES =============

EXAMPLE_NO_COMPILE = r"""
\usetikzlibrary{arrows,automata}
\definecolor{mymagenta}{RGB}{226,0,116}
"""


def test_no_compile():
    line = "-nc"
    cell = EXAMPLE_NO_COMPILE

    res = ipy.run_cell_magic("tikz", line, cell)

    assert res == None


# Other tests are implemented in the test_env_and_user_ns.py file


# ============== TEX PROGRAMS =============

# Tex programs test are implemented in run_latex.py


# =========== DEBUGGING AND ERROR =============

# If you write an invalid Tikz code, it will show a LaTeX error message limited in 20 lines


def test_rasterize():
    line = "-r --dpi=150"
    cell = EXAMPLE_RASTERIZE

    res = ipy.run_cell_magic("tikz", line, cell)

    assert isinstance(res, Image)


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


# ================== USE AS PACKAGE ==================

# The package functions are tested in they own files. i.e. test_save_path.py, test_run_latex.py...
