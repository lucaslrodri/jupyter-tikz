import pytest
import jupyter_tikz
from jupyter_tikz.jupyter_tikz import build_tex_string

# from IPython.testing.globalipapp import get_ipython

# ip = get_ipython()
# ip.run_line_magic("load_ext", "jupyter_tikz")

EXAMPLE_RECTANGLE_TIKZ = r"""
\documentclass[tikz]{standalone}
\begin{document}
\begin{tikzpicture}
\draw[fill=blue] (0, 0) rectangle (1, 1);
\end{tikzpicture}
\end{document}
""".strip()


@pytest.fixture
def jupyter_tikz_magic(mocker, monkeypatch):
    obj = jupyter_tikz.TikZMagics()
    shell = mocker.MagicMock()
    shell.user_ns = {}
    monkeypatch.setattr(obj, "shell", shell)
    return obj


# ========================= ValueErrors =========================
def test_magic_raise_error_with_empty_input_cell(jupyter_tikz_magic):
    with pytest.raises(ValueError, match="No code provided"):
        jupyter_tikz_magic.tikz("")


def test_magic_no_simultaneous_implicit_pic_and_full_document(jupyter_tikz_magic):
    with pytest.raises(
        ValueError, match="Can't use --full-document and --implicit-pic together"
    ):
        jupyter_tikz_magic.tikz("-f -i", EXAMPLE_RECTANGLE_TIKZ)


def test_tikz_error_packages_and_libraries_in_preamble_and_arguments(
    jupyter_tikz_magic,
):
    with pytest.raises(
        ValueError,
        match="Packages and libraries should be passed in the preamble or as arguments, not both.",
    ):
        jupyter_tikz_magic.tikz(
            "-t amsmath -p '\\usepackage{amssymb}'", EXAMPLE_RECTANGLE_TIKZ
        )


# ========================= build_template_extras =========================
def test_build_template_extras_no_extras_line(jupyter_tikz_magic):
    src = "code"
    jupyter_tikz_magic.tikz(src)
    res = jupyter_tikz_magic.build_template_extras()
    assert res == "\\usepackage{tikz}"


def test_build_template_extras_no_extras_no_extras_cell(jupyter_tikz_magic):
    src = "code"
    jupyter_tikz_magic.tikz("", src)
    res = jupyter_tikz_magic.build_template_extras()
    assert res == "\\usepackage{tikz}"


def test_build_template_extras_package_line(jupyter_tikz_magic):
    src = "code"
    jupyter_tikz_magic.tikz(f"-t=a,b {src}")
    res = jupyter_tikz_magic.build_template_extras()
    assert res == "\\usepackage{tikz}\n\\usepackage{a,b}"


def test_build_template_extras_package_tikz_library_line(jupyter_tikz_magic):
    src = "code"
    jupyter_tikz_magic.tikz(f"-t=a,b -l=c,d", src)
    res = jupyter_tikz_magic.build_template_extras()
    assert res == "\\usepackage{tikz}\n\\usepackage{a,b}\n\\usetikzlibrary{c,d}"


def test_build_template_extras_package_library_tikz_and_pgfplots_line(
    jupyter_tikz_magic,
):
    src = "code"
    jupyter_tikz_magic.tikz(f"-sc 3 -t=a,b -l=c,d -lp=e,f", src)
    res = jupyter_tikz_magic.build_template_extras()
    assert (
        res
        == "\\usepackage{tikz}\n\\usepackage{a,b}\n\\usetikzlibrary{c,d}\n\\usepgfplotslibrary{e,f}"
    )


def test_build_template_extras_preamble_line(
    jupyter_tikz_magic,
):
    src = "code"
    jupyter_tikz_magic.tikz(f"-p preamble", src)
    res = jupyter_tikz_magic.build_template_extras()
    assert res == "preamble"


# ========================= build_tex_string Tests =========================


def test_build_tex_string_implicit_pic_scale_1():
    src = "code"
    implicit_pic = True
    scale = 1.0
    extras = r"\usepackage{tikz}"
    expected_result = r"""\documentclass{standalone}
\usepackage{tikz}
\begin{document}
\begin{tikzpicture}
code
\end{tikzpicture}
\end{document}"""
    result = build_tex_string(src, implicit_pic, scale, extras)
    assert result.strip() == expected_result.strip()


def test_build_tex_string_not_implicit_pic_scale_1():
    src = "code"
    implicit_pic = False
    scale = 1.0
    extras = ""
    expected_result = r"""\documentclass{standalone}

\begin{document}
code
\end{document}"""
    result = build_tex_string(src, implicit_pic, scale, extras)
    assert result.strip() == expected_result.strip()


def test_build_tex_string_with_no_implicit_pic_extras_scale_1():
    src = "code"
    implicit_pic = False
    scale = 1.0
    extras = r"\usepackage{a}"
    expected_result = r"""\documentclass{standalone}
\usepackage{a}
\begin{document}
code
\end{document}"""
    result = build_tex_string(src, implicit_pic, scale, extras)
    assert result.strip() == expected_result.strip()


def test_build_tex_string_with_scale_scale_neq_1():
    src = "code"
    implicit_pic = True
    scale = 2.0
    extras = ""
    expected_result = r"""\documentclass{standalone}

\begin{document}
\scalebox{2.0}{
\begin{tikzpicture}
code
\end{tikzpicture}
}
\end{document}"""
    result = build_tex_string(src, implicit_pic, scale, extras)
    assert result.strip() == expected_result.strip()


def test_build_tex_string_with_all_options():
    src = "code"
    implicit_pic = True
    scale = 2.5
    extras = "\\usepackage{a}\n\\usepackage{b}"
    expected_result = r"""\documentclass{standalone}
\usepackage{a}
\usepackage{b}
\begin{document}
\scalebox{2.5}{
\begin{tikzpicture}
code
\end{tikzpicture}
}
\end{document}"""
    result = build_tex_string(src, implicit_pic, scale, extras)
    assert result.strip() == expected_result.strip()


# ==================== Examples =================
