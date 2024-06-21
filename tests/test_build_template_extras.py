import pytest
from jupyter_tikz.jupyter_tikz import TikZMagics


@pytest.fixture
def jupyter_tikz_magic(mocker, monkeypatch):
    obj = TikZMagics()
    shell = mocker.MagicMock()
    shell.user_ns = {}
    monkeypatch.setattr(obj, "shell", shell)
    return obj


def test_build_template_extras_no_extras_tikz_false(jupyter_tikz_magic):
    src = "code"
    jupyter_tikz_magic.tikz("--no-tikz", src)

    res = jupyter_tikz_magic.build_template_extras()
    expected_res = ""

    assert res == expected_res


def test_build_template_extras_no_extras_line(jupyter_tikz_magic):
    src = "code"
    jupyter_tikz_magic.tikz(src)

    res = jupyter_tikz_magic.build_template_extras()
    expected_res = "\\usepackage{tikz}\n"

    assert res == expected_res


def test_build_template_extras_no_extras_no_extras_cell(jupyter_tikz_magic):
    src = "code"
    jupyter_tikz_magic.tikz("", src)

    res = jupyter_tikz_magic.build_template_extras()
    expected_res = "\\usepackage{tikz}\n"

    assert res == expected_res


def test_build_template_extras_package_line(jupyter_tikz_magic):
    src = "code"
    jupyter_tikz_magic.tikz(f"-t=a,b {src}")

    res = jupyter_tikz_magic.build_template_extras()
    expected_res = "\\usepackage{tikz}\n\\usepackage{a,b}\n"

    assert res == expected_res


def test_build_template_extras_package_tikz_library_line(jupyter_tikz_magic):
    src = "code"
    jupyter_tikz_magic.tikz(f"-t=a,b -l=c,d", src)

    res = jupyter_tikz_magic.build_template_extras()
    expected_res = "\\usepackage{tikz}\n\\usepackage{a,b}\n\\usetikzlibrary{c,d}\n"

    assert res == expected_res


def test_build_template_extras_package_library_tikz_and_pgfplots_line(
    jupyter_tikz_magic,
):
    src = "code"
    jupyter_tikz_magic.tikz(f"-sc 3 -t=a,b -l=c,d -lp=e,f", src)

    res = jupyter_tikz_magic.build_template_extras()
    expected_res = "\\usepackage{tikz}\n\\usepackage{a,b}\n\\usetikzlibrary{c,d}\n\\usepgfplotslibrary{e,f}\n"

    assert res == expected_res


def test_build_template_extras_preamble_line(
    jupyter_tikz_magic,
):
    src = "code"
    jupyter_tikz_magic.tikz(f"-p preamble", src)

    res = jupyter_tikz_magic.build_template_extras()
    expected_res = "preamble\n"

    assert res == expected_res
