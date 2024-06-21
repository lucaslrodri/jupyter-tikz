from jupyter_tikz.jupyter_tikz import build_tex_string

IMPLICIT_PIC_EXAMPLE = r"""\documentclass{standalone}
\usepackage{tikz}
\begin{document}
	\begin{tikzpicture}
		code
	\end{tikzpicture}
\end{document}"""


def test_build_tex_string_implicit_pic():
    src = "code"
    implicit_pic = True
    extras = "\\usepackage{tikz}\n"

    res = build_tex_string(src, implicit_pic, extras)
    expected_res = IMPLICIT_PIC_EXAMPLE

    assert res.strip() == expected_res.strip()


NO_IMPLICT_PIC_EXAMPLE = r"""\documentclass{standalone}
\begin{document}
	code
\end{document}"""


def test_build_tex_string_not_implicit_pic():
    src = "code"
    implicit_pic = False
    extras = ""

    res = build_tex_string(src, implicit_pic, extras)
    expected_res = NO_IMPLICT_PIC_EXAMPLE

    assert res.strip() == expected_res.strip()


def test_build_tex_string_with_no_implicit_pic_extras():
    src = "code"
    implicit_pic = False
    extras = "\\usepackage{a}\n"

    res = build_tex_string(src, implicit_pic, extras)
    expected_res = r"""\documentclass{standalone}
\usepackage{a}
\begin{document}
	code
\end{document}"""

    assert res.strip() == expected_res.strip()


def test_build_tex_string_implicit_pic_extras():
    src = "code"
    implicit_pic = True
    extras = "\\usepackage{a}\n\\usepackage{b}\n"

    res = build_tex_string(src, implicit_pic, extras)
    expected_res = r"""\documentclass{standalone}
\usepackage{a}
\usepackage{b}
\begin{document}
	\begin{tikzpicture}
		code
	\end{tikzpicture}
\end{document}"""

    assert res.strip() == expected_res.strip()
