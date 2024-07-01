from string import Template

import pytest

from jupyter_tikz import TexTemplate

TEMPLATE_TEX_PACKAGES = "\\usepackage{tikz}\n\\usepackage{$tex_packages}\n"
TEMPLATE_NO_TEX_PACKAGES = "\\usepackage{tikz}\n"


@pytest.mark.parametrize(
    "tex_packages",
    [
        None,
        "",
        "amsmath",
        "amsmath,amssymb,xcolor",
        "asmath,amssymb",
    ],
)
def test_latex_packages(tex_packages):
    # Arrange
    code = "any code"
    tex_template = TexTemplate(code)

    # Act
    res = tex_template._build_standalone_preamble(tex_packages=tex_packages)

    # Assert
    if tex_packages:
        expected_res = Template(TEMPLATE_TEX_PACKAGES).substitute(
            tex_packages=tex_packages
        )
    else:
        expected_res = TEMPLATE_NO_TEX_PACKAGES
    assert res == expected_res


TEMPLATE_TIKZ_LIBRARIES_NO_TEX_PACKAGES = (
    "\\usepackage{tikz}\n\\usetikzlibrary{$tikz_libraries}\n"
)
TEMPLATE_TIKZ_LIBRARIES_WITH_TEX_PACKAGES = (
    "\\usepackage{tikz}\n\\usepackage{$package}\n\\usetikzlibrary{$tikz_libraries}\n"
)


@pytest.mark.parametrize(
    "tex_packages, tikz_libraries, expected_template",
    [
        (None, "calc", TEMPLATE_TIKZ_LIBRARIES_NO_TEX_PACKAGES),
        (None, "calc,arrows,patterns", TEMPLATE_TIKZ_LIBRARIES_NO_TEX_PACKAGES),
        ("amsmath,amssymb,xcolor", "calc", TEMPLATE_TIKZ_LIBRARIES_WITH_TEX_PACKAGES),
        (
            "amsmath,amssymb,xcolor",
            "calc,arrows,patterns",
            TEMPLATE_TIKZ_LIBRARIES_WITH_TEX_PACKAGES,
        ),
    ],
)
def test_tikz_libraries(tex_packages, tikz_libraries, expected_template):
    # Arrange
    code = "any code"
    tikz_libraries = "calc,arrows,patterns"
    tex_template = TexTemplate(code)

    # Act
    res = tex_template._build_standalone_preamble(
        tex_packages=tex_packages, tikz_libraries=tikz_libraries
    )

    # Assert
    expected_res = Template(expected_template).substitute(
        package=tex_packages, tikz_libraries=tikz_libraries
    )

    assert res == expected_res


TEMPLATE_PGFPLOTS_LIBRARIES_NO_TIKZ_LIBRARIES = "\\usepackage{tikz}\n\\usepackage{$tex_packages}\n\\usepgfplotslibrary{$pgfplots_libraries}\n"
TEMPLATE_PGFPLOTS_LIBRARIES_TEX_PACKAGES_AND_TIKZ_LIBRARIES = "\\usepackage{tikz}\n\\usepackage{$tex_packages}\n\\usetikzlibrary{$tikz_libraries}\n\\usepgfplotslibrary{$pgfplots_libraries}\n"


@pytest.mark.parametrize(
    "tex_packages, tikz_libraries, pgfplots_libraries, expected_template",
    [
        ("pgfplots", None, "colormaps", TEMPLATE_PGFPLOTS_LIBRARIES_NO_TIKZ_LIBRARIES),
        (
            "pgfplots",
            "calc",
            "polar",
            TEMPLATE_PGFPLOTS_LIBRARIES_TEX_PACKAGES_AND_TIKZ_LIBRARIES,
        ),
        (
            "pgfplots",
            "calc,arrows,patterns",
            "smithchart,groupplots",
            TEMPLATE_PGFPLOTS_LIBRARIES_TEX_PACKAGES_AND_TIKZ_LIBRARIES,
        ),
        (
            "amsmath,amssymb,xcolor",
            "calc",
            "3d",
            TEMPLATE_PGFPLOTS_LIBRARIES_TEX_PACKAGES_AND_TIKZ_LIBRARIES,
        ),
        (
            "amsmath,amssymb,xcolor",
            "calc,arrows,patterns",
            "statistcs,external",
            TEMPLATE_PGFPLOTS_LIBRARIES_TEX_PACKAGES_AND_TIKZ_LIBRARIES,
        ),
        (
            "amsmath,amssymb,xcolor",
            "calc,arrows,patterns",
            "fillbetween,spy,shapes.geometric",
            TEMPLATE_PGFPLOTS_LIBRARIES_TEX_PACKAGES_AND_TIKZ_LIBRARIES,
        ),
    ],
)
def test_pgfplots_libraries(
    tex_packages, tikz_libraries, pgfplots_libraries, expected_template
):
    # Arrange
    code = "any code"
    tex_template = TexTemplate(code)

    # Act
    res = tex_template._build_standalone_preamble(
        tex_packages=tex_packages,
        tikz_libraries=tikz_libraries,
        pgfplots_libraries=pgfplots_libraries,
    )

    # Assert
    expected_res = Template(expected_template).substitute(
        tex_packages=tex_packages,
        tikz_libraries=tikz_libraries,
        pgfplots_libraries=pgfplots_libraries,
    )

    assert res == expected_res


TEMPLATE_NO_TIKZ_ONLY_PACKAGE = "\\usepackage{$tex_packages}\n"
TEMPLATE_NO_TIKZ_WITH_ALL_EXTRAS = "\\usepackage{$tex_packages}\n\\usetikzlibrary{$tikz_libraries}\n\\usepgfplotslibrary{polar}\n"


@pytest.mark.parametrize(
    "tex_packages, tikz_libraries, pgfplots_libraries, expected_template",
    [
        ("circuitikz", None, None, TEMPLATE_NO_TIKZ_ONLY_PACKAGE),
        (
            "amsmath,pgfplots",
            "calc,arrows,patterns",
            "polar",
            TEMPLATE_NO_TIKZ_WITH_ALL_EXTRAS,
        ),
    ],
)
def test_no_tikz(tex_packages, tikz_libraries, pgfplots_libraries, expected_template):
    # Arrange
    code = "any code"
    tex_template = TexTemplate(code)

    # Act
    res = tex_template._build_standalone_preamble(
        tex_packages=tex_packages,
        tikz_libraries=tikz_libraries,
        pgfplots_libraries=pgfplots_libraries,
        no_tikz=True,
    )

    # Assert
    expected_res = Template(expected_template).substitute(
        tex_packages=tex_packages,
        tikz_libraries=tikz_libraries,
        pgfplots_libraries=pgfplots_libraries,
    )
    assert res == expected_res


TEMPLATE_SCALE_ONLY_PACKAGE = (
    "\\usepackage{graphicx}\n\\usepackage{tikz}\n\\usepackage{$tex_packages}\n"
)
TEMPLATE_SCALE_WITH_ALL_EXTRAS = "\\usepackage{graphicx}\n\\usepackage{tikz}\n\\usepackage{$tex_packages}\n\\usetikzlibrary{$tikz_libraries}\n\\usepgfplotslibrary{polar}\n"


@pytest.mark.parametrize(
    "tex_packages, tikz_libraries, pgfplots_libraries, expected_template",
    [
        ("circuitikz", None, None, TEMPLATE_SCALE_ONLY_PACKAGE),
        (
            "amsmath,pgfplots",
            "calc,arrows,patterns",
            "polar",
            TEMPLATE_SCALE_WITH_ALL_EXTRAS,
        ),
    ],
)
def test_scale(tex_packages, tikz_libraries, pgfplots_libraries, expected_template):
    # Arrange
    code = "any code"
    tex_template = TexTemplate(code, scale=2)

    # Act
    res = tex_template._build_standalone_preamble(
        tex_packages=tex_packages,
        tikz_libraries=tikz_libraries,
        pgfplots_libraries=pgfplots_libraries,
    )

    # Assert
    expected_res = Template(expected_template).substitute(
        tex_packages=tex_packages,
        tikz_libraries=tikz_libraries,
        pgfplots_libraries=pgfplots_libraries,
    )
    assert res == expected_res
