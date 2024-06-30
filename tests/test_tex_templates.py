import pytest
from jupyter_tikz import TexTemplate
from IPython import display


def test_preamble():
    # Arrange
    code = "any code"
    preamble = "any preamble"

    # Act
    tex_template = TexTemplate(code, preamble=preamble)

    # Assert
    assert tex_template.preamble == preamble
    assert preamble in tex_template.latex_str


def test_standalone_preamble():
    # Arrange
    code = "any code"
    tex_packages = "a,b"
    tikz_libraries = "c,d"
    pgfplots_libraries = "e,f"

    # Act
    tex_template = TexTemplate(
        code,
        tex_packages=tex_packages,
        tikz_libraries=tikz_libraries,
        pgfplots_libraries=pgfplots_libraries,
    )
    # Assert
    assert (
        "a,b" in tex_template.preamble
        and "c,d" in tex_template.preamble
        and "e,f" in tex_template.preamble
    )
    assert (
        "a,b" in tex_template.latex_str
        and "c,d" in tex_template.latex_str
        and "e,f" in tex_template.latex_str
    )


def test_raise_error_when_preamble_and_extras_are_provided():
    # Arrange
    code = "any code"
    preamble = "any preamble"
    tex_packages = "a,b"
    tikz_libraries = "c,d"
    pgfplots_libraries = "e,f"

    # Act
    with pytest.raises(ValueError) as err:
        res = TexTemplate(
            code,
            preamble=preamble,
            tex_packages=tex_packages,
            tikz_libraries=tikz_libraries,
            pgfplots_libraries=pgfplots_libraries,
        )
        # Assert
        assert res is None

    assert (
        "You cannot provide `preamble` and (`tex_packages`, `tikz_libraries`, and/or `pgfplots_libraries`) at the same time."
        in str(err.value)
    )


def test_scale():
    # Arrange
    code = "any code"
    scale = 1.5

    # Act
    tex_template = TexTemplate(code, scale=scale)

    # Assert
    assert (
        " " * 4 + "\\scalebox{%g}{\n" % scale in tex_template.latex_str
        and " " * 4 + "\n}\n"
        and "graphicx" in tex_template.preamble
    )


def test_scale_with_preamble():
    # Arrange
    code = "any code"
    scale = 1.5
    preamble = "any preamble"

    # Act
    tex_template = TexTemplate(code, scale=scale, preamble=preamble)

    # Assert
    assert (
        " " * 4 + "\\scalebox{%g}{\n" % scale in tex_template.latex_str
        and " " * 4 + "}\n"
        and "graphicx" not in tex_template.preamble
    )


def test_implicit_tikzpicture():
    # Arrange
    code = "any code"

    # Act
    tex_template = TexTemplate(code, implicit_tikzpicture=True)

    # Assert
    assert (
        4 * " " + "\\begin{tikzpicture}\n" in tex_template.latex_str
        and 4 * " " + "\\end{tikzpicture}\n" in tex_template.latex_str
    )


@pytest.mark.parametrize(
    "implicit_tikzpicture, indent_size, scale, expected_n_indents",
    [
        (True, 8, 1, 16),
        (False, 4, 1, 16),
        (True, 8, 0.75, 16),
        (False, 4, 0.75, 18),
    ],
)
def test_code_indent(implicit_tikzpicture, indent_size, scale, expected_n_indents):
    # Arrange
    code = "any code\n" * 16
    code_indent = " " * indent_size

    # Act
    tex_template = TexTemplate(
        code, implicit_tikzpicture=implicit_tikzpicture, scale=scale
    )

    # Assert
    assert tex_template.latex_str.count(code_indent) == expected_n_indents


# =========================== run_latex - tests ===========================

EXAMPLE_SRC_IMPLICIT_PIC = r"""
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

EXAMPLE_SRC_CIRCUITIKZ = r"""\draw (0,0)
    to[V,v=$U_q$] (0,2) % Voltage source
    to[short] (2,2)
    to[R=$R_1$] (2,0) % Resistor R1
    to[short] (0,0);
\draw (2,2)
    to[short] (4,2)
    to[L=$L_1$] (4,0) % Inductor L1
    to[short] (2,0);
\draw (4,2)
    to[short] (6,2)
    to[C=$C_1$] (6,0) % Capacitor C1
    to[short] (4,0);"""

# ------------------------------ test implicit_tikzpicture ------------------------------

RES_IMPLICIT_PIC = r"""\documentclass{standalone}
\usepackage{tikz}
\begin{document}
    \begin{tikzpicture}
        \node[draw, circle] at (0, 0) {Hello};
        \draw[fill=blue] (0, 0) rectangle (1, 1);
        \draw[fill=red] (1, 1) rectangle (2, 2);
    \end{tikzpicture}
\end{document}"""


@pytest.fixture
def tex_template_implicit_pic():
    return TexTemplate(EXAMPLE_SRC_IMPLICIT_PIC, implicit_tikzpicture=True)


def test_build_tex_string_implicit_pic(tex_template_implicit_pic):
    # Assert
    assert tex_template_implicit_pic.latex_str.strip() == RES_IMPLICIT_PIC.strip()


@pytest.mark.needs_latex
@pytest.mark.needs_pdftocairo
def test_run_latex_implicit_pic(tex_template_implicit_pic):
    # Act
    res = tex_template_implicit_pic.run_latex()

    # Assert
    assert isinstance(res, display.SVG)


# ------------------------------ test implicit_tikzpicture with scale ------------------------------

RES_IMPLICIT_PIC_WITH_SCALE = r"""\documentclass{standalone}
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


@pytest.fixture
def tex_template_implicit_pic_with_scale():
    return TexTemplate(EXAMPLE_SRC_IMPLICIT_PIC, implicit_tikzpicture=True, scale=3)


def test_build_tex_string_implicit_pic_with_scale(tex_template_implicit_pic_with_scale):
    # Assert
    assert (
        tex_template_implicit_pic_with_scale.latex_str.strip()
        == RES_IMPLICIT_PIC_WITH_SCALE.strip()
    )


@pytest.mark.needs_latex
@pytest.mark.needs_pdftocairo
def test_run_latex_implicit_pic_with_scale(
    tex_template_implicit_pic_with_scale,
):
    # Act
    res = tex_template_implicit_pic_with_scale.run_latex()

    # Assert
    assert isinstance(res, display.SVG)


# ------------------------------ test implicit_tikzpicture with packages and scale ------------------------------

RES_IMPLICT_PIC_WITH_PACKAGES_AND_SCALE = r"""\documentclass{standalone}
\usepackage{graphicx}
\usepackage{tikz}
\usepackage{xcolor,amsmath}
\begin{document}
    \scalebox{2}{
    \begin{tikzpicture}
        \node[draw, circle] at (0, 0) {Hello};
        \draw[fill=blue] (0, 0) rectangle (1, 1);
        \draw[fill=red] (1, 1) rectangle (2, 2);
    \end{tikzpicture}
    }
\end{document}"""


@pytest.fixture
def tex_template_implicit_pic_with_packages_and_scale():
    return TexTemplate(
        EXAMPLE_SRC_IMPLICIT_PIC,
        implicit_tikzpicture=True,
        scale=2,
        tex_packages="xcolor,amsmath",
    )


def test_build_tex_string_implicit_pic_with_packages_and_scale(
    tex_template_implicit_pic_with_packages_and_scale,
):
    # Assert
    assert (
        tex_template_implicit_pic_with_packages_and_scale.latex_str.strip()
        == RES_IMPLICT_PIC_WITH_PACKAGES_AND_SCALE.strip()
    )


@pytest.mark.needs_latex
@pytest.mark.needs_pdftocairo
def test_run_latex_implicit_pic_with_packages_and_scale(
    tex_template_implicit_pic_with_packages_and_scale,
):
    # Act
    res = tex_template_implicit_pic_with_packages_and_scale.run_latex()

    # Assert
    assert isinstance(res, display.SVG)


# ------------------------------ test implicit_tikzpicture with no_tikz ------------------------------

RES_NO_IMPLICT_PIC_NO_TIKZ = r"""\documentclass{standalone}
\usepackage{circuitikz}
\begin{document}
    \begin{tikzpicture}
        \draw (0,0)
            to[V,v=$U_q$] (0,2) % Voltage source
            to[short] (2,2)
            to[R=$R_1$] (2,0) % Resistor R1
            to[short] (0,0);
        \draw (2,2)
            to[short] (4,2)
            to[L=$L_1$] (4,0) % Inductor L1
            to[short] (2,0);
        \draw (4,2)
            to[short] (6,2)
            to[C=$C_1$] (6,0) % Capacitor C1
            to[short] (4,0);
    \end{tikzpicture}
\end{document}"""


@pytest.fixture
def tex_template_implicit_pic_no_tikz():
    return TexTemplate(
        EXAMPLE_SRC_CIRCUITIKZ,
        implicit_tikzpicture=True,
        no_tikz=True,
        tex_packages="circuitikz",
    )


def test_build_tex_string_implicit_pic_no_tikz(
    tex_template_implicit_pic_no_tikz,
):
    # Assert
    assert (
        tex_template_implicit_pic_no_tikz.latex_str.strip()
        == RES_NO_IMPLICT_PIC_NO_TIKZ.strip()
    )


@pytest.mark.needs_latex
@pytest.mark.needs_pdftocairo
def test_run_latex_implicit_pic_no_tikz(
    tex_template_implicit_pic_no_tikz,
):
    # Act
    res = tex_template_implicit_pic_no_tikz.run_latex()

    # Assert
    assert isinstance(res, display.SVG)


# ------------------------------ test no_implicit_tikzpicture with scale and no extras ------------------------------

RES_NO_IMPLICT_PIC_WITH_SCALE_AND_NO_EXTRAS = r"""\documentclass{standalone}
\usepackage{graphicx}
\usepackage{tikz}
\begin{document}
    \scalebox{1.5}{
    \begin{tikzpicture}
        \node[draw, circle] at (0, 0) {Hello};
        \draw[fill=blue] (0, 0) rectangle (1, 1);
        \draw[fill=red] (1, 1) rectangle (2, 2);
    \end{tikzpicture}
    }
\end{document}"""


@pytest.fixture
def tex_template_no_implicit_pic_with_scale_and_no_extras():
    return TexTemplate(EXAMPLE_SRC_STANDALONE, scale=1.5)


def test_build_tex_string_no_implicit_pic_with_scale_and_no_extras(
    tex_template_no_implicit_pic_with_scale_and_no_extras,
):
    # Assert
    assert (
        tex_template_no_implicit_pic_with_scale_and_no_extras.latex_str.strip()
        == RES_NO_IMPLICT_PIC_WITH_SCALE_AND_NO_EXTRAS.strip()
    )


@pytest.mark.needs_latex
@pytest.mark.needs_pdftocairo
def test_run_latex_no_implicit_pic_with_scale_and_no_extras(
    tex_template_no_implicit_pic_with_scale_and_no_extras,
):
    # Act
    res = tex_template_no_implicit_pic_with_scale_and_no_extras.run_latex()

    # Assert
    assert isinstance(res, display.SVG)


# ------------------------------

RES_NO_IMPLICT_PIC_WITH_SCALE_AND_PACKAGES = r"""\documentclass{standalone}
\usepackage{graphicx}
\usepackage{tikz}
\usepackage{xcolor,amsmath}
\begin{document}
    \scalebox{0.5}{
    \begin{tikzpicture}
        \node[draw, circle] at (0, 0) {Hello};
        \draw[fill=blue] (0, 0) rectangle (1, 1);
        \draw[fill=red] (1, 1) rectangle (2, 2);
    \end{tikzpicture}
    }
\end{document}"""


@pytest.fixture
def tex_template_no_implicit_pic_with_scale_and_packages():
    return TexTemplate(EXAMPLE_SRC_STANDALONE, scale=0.5, tex_packages="xcolor,amsmath")


def test_build_tex_string_no_implicit_pic_with_scale_and_packages(
    tex_template_no_implicit_pic_with_scale_and_packages,
):
    # Assert
    assert (
        tex_template_no_implicit_pic_with_scale_and_packages.latex_str.strip()
        == RES_NO_IMPLICT_PIC_WITH_SCALE_AND_PACKAGES.strip()
    )


@pytest.mark.needs_latex
@pytest.mark.needs_pdftocairo
def test_run_latex_no_implicit_pic_with_scale_and_packages(
    tex_template_no_implicit_pic_with_scale_and_packages,
):
    # Act
    res = tex_template_no_implicit_pic_with_scale_and_packages.run_latex()

    # Assert
    assert isinstance(res, display.SVG)
