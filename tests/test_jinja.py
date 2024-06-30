import pytest
from jupyter_tikz import TexDocument
from jupyter_tikz.jupyter_tikz import JINJA_NOT_INTALLED_ERR, NS_NOT_PROVIDED_ERR

EXAMPLE_TIKZ_JINJA_TEMPLATE = """\\begin{tikzpicture}
    \\node[draw] at (0,0) {Hello, {{ name }}!};
\\end{tikzpicture}
"""

EXAMPLE_TIKZ_RENDERED_TEMPLATE = """\\begin{tikzpicture}
    \\node[draw] at (0,0) {Hello, World!};
\\end{tikzpicture}
"""

COMPLEX_TIKZ_JINJA_TEMPLATE = r"""
\begin{tikzpicture}
    {% for person in people %}
    \node[draw] at (0,{{ person.y }}) {Hello, {{ person.name }}!};
    {% endfor %}
\end{tikzpicture}
"""


def test_init_with_jinja_without_ns_raises_error():
    # Act
    with pytest.raises(ValueError) as err:
        TexDocument(EXAMPLE_TIKZ_JINJA_TEMPLATE, use_jinja=True)

    # Assert
    assert NS_NOT_PROVIDED_ERR in str(err.value)


def test_jinja_when_jinja_is_not_installed_raises_error(monkeypatch):
    # Arrange
    monkeypatch.setattr("sys.modules", {"jinja2": None})

    # Act
    with pytest.raises(ImportError) as err:
        res = TexDocument(
            EXAMPLE_TIKZ_JINJA_TEMPLATE, use_jinja=True, ns={"name": "World"}
        )
        # Assert
        assert res is None

    assert JINJA_NOT_INTALLED_ERR in str(err.value)


def test_jinja_using_dict_ns():
    # Arrange
    name = "World"

    # Act
    tex_document = TexDocument(
        EXAMPLE_TIKZ_JINJA_TEMPLATE, use_jinja=True, ns={"name": name}
    )

    # Assert
    assert str(tex_document).strip() == EXAMPLE_TIKZ_RENDERED_TEMPLATE.strip()


def test_jinja_using_local_ns():
    # Arrange
    name = "World"
    _ = name

    # Act
    tex_document = TexDocument(EXAMPLE_TIKZ_JINJA_TEMPLATE, use_jinja=True, ns=locals())

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
    tex_document = TexDocument(
        COMPLEX_TIKZ_JINJA_TEMPLATE, use_jinja=True, ns={"people": people}
    )

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
    {% block content %}{% endblock %}
\\end{tikzpicture}
"""

EXAMPLE_TIKZ_JINJA_CHILD_TEMPLATE = """{% extends 'parent_tmpl.tex' %}
{% block content %}
    \node[draw] at (0,0) {Hello, {{ name }}!};
{% endblock %}
"""
EXAMPLE_TIKZ_JINJA_EXTENDED_TEMPLATE = """\\begin{tikzpicture}
    \\draw (-2.5,-2.5) rectangle (5,5);
    
    \node[draw] at (0,0) {Hello, World!};

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
    tex_document = TexDocument(
        EXAMPLE_TIKZ_JINJA_CHILD_TEMPLATE, use_jinja=True, ns=locals()
    )

    # Assert
    assert f"{tex_document}".strip() == EXAMPLE_TIKZ_JINJA_EXTENDED_TEMPLATE.strip()
