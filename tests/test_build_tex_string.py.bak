from jupyter_tikz import build_tex_string

EXAMPLE_SRC_PIC = r"""
\node[draw, circle] at (0, 0) {Hello};
\draw[fill=blue] (0, 0) rectangle (1, 1);
\draw[fill=red] (1, 1) rectangle (2, 2);
"""

EXAMPLE_SRC_STANDALONE = r"""
\begin{tikzpicture}
	\node[draw, circle] at (0, 0) {Hello};
	\draw[fill=blue] (0, 0) rectangle (1, 1);
	\draw[fill=red] (1, 1) rectangle (2, 2);
\end{tikzpicture}
"""


# ------------------------------

EXAMPLE_IMPLICIT_PIC = r"""\documentclass{standalone}
\usepackage{tikz}
\begin{document}
	\begin{tikzpicture}
		\node[draw, circle] at (0, 0) {Hello};
		\draw[fill=blue] (0, 0) rectangle (1, 1);
		\draw[fill=red] (1, 1) rectangle (2, 2);
	\end{tikzpicture}
\end{document}"""


def test_build_tex_string_implicit_pic():
    src = EXAMPLE_SRC_PIC
    implicit_pic = True
    extras = "\\usepackage{tikz}\n"

    res = build_tex_string(src, implicit_pic, extras)
    expected_res = EXAMPLE_IMPLICIT_PIC

    assert res.strip() == expected_res.strip()


# ------------------------------

EXAMPLE_IMPLICIT_PIC_WITH_SCALE = r"""\documentclass{standalone}
\usepackage{graphicx}
\usepackage{tikz}
\begin{document}
	\scalebox{3}{
	\begin{tikzpicture}
		\node[draw, circle] at (0, 0) {Hello};
		\draw[fill=blue] (0, 0) rectangle (1, 1);
		\draw[fill=red] (1, 1) rectangle (2, 2);
	\end{tikzpicture}
	}
\end{document}"""


def test_build_tex_string_implicit_pic_with_scale():
    src = EXAMPLE_SRC_PIC
    implicit_pic = True
    extras = "\\usepackage{tikz}\n"
    scale = 3

    res = build_tex_string(src, implicit_pic, extras, scale)
    expected_res = EXAMPLE_IMPLICIT_PIC_WITH_SCALE

    assert res.strip() == expected_res.strip()


# ------------------------------


EXAMPLE_IMPLICT_PIC_WITH_EXTRAS_AND_SCALE = r"""\documentclass{standalone}
\usepackage{graphicx}
\usepackage{tikz}
\usepackage{a}
\usepackage{b}
\begin{document}
	\scalebox{2}{
	\begin{tikzpicture}
		\node[draw, circle] at (0, 0) {Hello};
		\draw[fill=blue] (0, 0) rectangle (1, 1);
		\draw[fill=red] (1, 1) rectangle (2, 2);
	\end{tikzpicture}
	}
\end{document}"""


def test_build_tex_string_implicit_pic_with_extras():
    src = EXAMPLE_SRC_PIC
    implicit_pic = True
    extras = "\\usepackage{tikz}\n\\usepackage{a}\n\\usepackage{b}\n"
    scale = 2

    res = build_tex_string(src, implicit_pic, extras, scale)
    expected_res = EXAMPLE_IMPLICT_PIC_WITH_EXTRAS_AND_SCALE

    assert res.strip() == expected_res.strip()


# ------------------------------

EXAMPLE_NO_IMPLICT_PIC_NO_EXTRAS = r"""\documentclass{standalone}
\begin{document}
	\begin{tikzpicture}
		\node[draw, circle] at (0, 0) {Hello};
		\draw[fill=blue] (0, 0) rectangle (1, 1);
		\draw[fill=red] (1, 1) rectangle (2, 2);
	\end{tikzpicture}
\end{document}"""


def test_build_tex_string_no_implicit_pic_no_extras():
    src = EXAMPLE_SRC_STANDALONE
    implicit_pic = False
    extras = ""

    res = build_tex_string(src, implicit_pic, extras)
    expected_res = EXAMPLE_NO_IMPLICT_PIC_NO_EXTRAS

    assert res.strip() == expected_res.strip()


# ------------------------------

EXAMPLE_NO_IMPLICT_PIC_WITH_SCALE_AND_NO_EXTRAS = r"""\documentclass{standalone}
\usepackage{graphicx}
\begin{document}
	\scalebox{1.5}{
	\begin{tikzpicture}
		\node[draw, circle] at (0, 0) {Hello};
		\draw[fill=blue] (0, 0) rectangle (1, 1);
		\draw[fill=red] (1, 1) rectangle (2, 2);
	\end{tikzpicture}
	}
\end{document}"""


def test_build_tex_string_no_implicit_pic_with__scale_and_no_extras():
    src = EXAMPLE_SRC_STANDALONE
    implicit_pic = False
    extras = ""
    scale = 1.5

    res = build_tex_string(src, implicit_pic, extras, scale)
    expected_res = EXAMPLE_NO_IMPLICT_PIC_WITH_SCALE_AND_NO_EXTRAS

    assert res.strip() == expected_res.strip()


# ------------------------------

EXAMPLE_NO_IMPLICT_PIC_WITH_SCALE_AND_EXTRAS = r"""\documentclass{standalone}
\usepackage{graphicx}
\usepackage{a}
\begin{document}
	\scalebox{0.5}{
	\begin{tikzpicture}
		\node[draw, circle] at (0, 0) {Hello};
		\draw[fill=blue] (0, 0) rectangle (1, 1);
		\draw[fill=red] (1, 1) rectangle (2, 2);
	\end{tikzpicture}
	}
\end{document}"""


def test_build_tex_string_with_no_implicit_pic_with_scale_and_extras():
    src = EXAMPLE_SRC_STANDALONE
    implicit_pic = False
    extras = "\\usepackage{a}\n"
    scale = 0.5

    res = build_tex_string(src, implicit_pic, extras, scale)
    expected_res = EXAMPLE_NO_IMPLICT_PIC_WITH_SCALE_AND_EXTRAS

    assert res.strip() == expected_res.strip()
