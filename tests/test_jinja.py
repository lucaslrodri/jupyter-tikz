import pytest

from jupyter_tikz import TexDocument
from tests.conftest import *
from IPython.display import SVG

EXAMPLE_TIKZ_JINJA_TEMPLATE = """\\begin{tikzpicture}
    \\node[draw] at (0,0) {Hello, (* name *)!};
\\end{tikzpicture}
"""

EXAMPLE_TIKZ_RENDERED_TEMPLATE = """\\begin{tikzpicture}
    \\node[draw] at (0,0) {Hello, World!};
\\end{tikzpicture}
"""

COMPLEX_TIKZ_JINJA_TEMPLATE = r"""
\begin{tikzpicture}
    (** for person in people -**)
    \node[draw] at (0,(* person.y *)) {Hello, (* person.name *)!};
    (** endfor **)
\end{tikzpicture}
"""


def test_disable_jinja__render_jinja_not_called(mocker):
    # Arrange
    spy = mocker.spy(TexDocument, "_render_jinja")

    # Act
    TexDocument(EXAMPLE_GOOD_TEX, disable_jinja=True)

    # Assert
    assert not spy.assert_not_called()


@pytest.mark.needs_latex
@pytest.mark.needs_pdftocairo
def test_disable_jinja__render_correctly(tmpdir, monkeypatch):
    # Arrange
    monkeypatch.chdir(tmpdir)
    tex_document = TexDocument(EXAMPLE_GOOD_TEX, disable_jinja=True)

    # Act
    res = tex_document.run_latex()

    # Assert
    assert isinstance(res, SVG)


def test__render_jinja_called_by_default(mocker):
    # Arrange
    spy = mocker.spy(TexDocument, "_render_jinja")

    # Act
    TexDocument(EXAMPLE_GOOD_TEX)

    # Assert
    assert not spy.assert_called_once()


def test_jinja_using_dict_ns():
    # Arrange
    name = "World"

    # Act
    tex_document = TexDocument(EXAMPLE_TIKZ_JINJA_TEMPLATE, ns={"name": name})

    # Assert
    assert str(tex_document).strip() == EXAMPLE_TIKZ_RENDERED_TEMPLATE.strip()


def test_jinja_using_local_ns():
    # Arrange
    name = "World"
    _ = name

    # Act
    tex_document = TexDocument(EXAMPLE_TIKZ_JINJA_TEMPLATE, ns=locals())

    # Assert
    assert str(tex_document).strip() == EXAMPLE_TIKZ_RENDERED_TEMPLATE.strip()


def test_jinja_with_complex_template():
    # Arrange
    people = [
        {"name": "Alice", "y": 0},
        {"name": "Bob", "y": 2},
        {"name": "Charlie", "y": 4},
    ]

    # Act
    tex_document = TexDocument(COMPLEX_TIKZ_JINJA_TEMPLATE, ns={"people": people})

    # Assert
    res = f"{tex_document}"
    assert (
        "Alice" in res
        and "Bob" in res
        and "Charlie" in res
        and "0" in res
        and "2" in res
        and "4" in res
    )


EXAMPLE_TIKZ_JINJA_PARENT_TEMPLATE = """\\begin{tikzpicture}
    \\draw (-2.5,-2.5) rectangle (5,5);
    (** block content **)(** endblock **)
\\end{tikzpicture}
"""

EXAMPLE_TIKZ_JINJA_CHILD_TEMPLATE = """(** extends 'parent_tmpl.tex' **)
    (** block content -**)
        \\node[draw] at (0,0) {Hello, (* name *)!};
    (**- endblock **)
"""
EXAMPLE_TIKZ_JINJA_EXTENDED_TEMPLATE = """\\begin{tikzpicture}
    \\draw (-2.5,-2.5) rectangle (5,5);
    \\node[draw] at (0,0) {Hello, World!};
\\end{tikzpicture}
"""


def test_jinja_extends_template(tmpdir, monkeypatch):
    # Arrange
    monkeypatch.chdir(tmpdir)
    parent_code = EXAMPLE_TIKZ_JINJA_PARENT_TEMPLATE
    parent = tmpdir / "parent_tmpl.tex"
    parent.write(parent_code)

    name = "World"
    _ = name

    # Act
    tex_document = TexDocument(EXAMPLE_TIKZ_JINJA_CHILD_TEMPLATE, ns=locals())

    # Assert
    assert f"{tex_document}".strip() == EXAMPLE_TIKZ_JINJA_EXTENDED_TEMPLATE.strip()
