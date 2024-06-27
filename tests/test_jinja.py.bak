from unittest.mock import patch

from jupyter_tikz import render_jinja

# Test rendering a simple TikZ template

SIMPLE_TIKZ_JINJA_TEMPLATE = """\\begin{tikzpicture}
    \\node[draw] at (0,0) {Hello, {{ name }}!};
\\end{tikzpicture}
"""

SIMPLE_TIKZ_RENDERED_TEMPLATE = """\\begin{tikzpicture}
    \\node[draw] at (0,0) {Hello, World!};
\\end{tikzpicture}
"""


def test_render_simple_tikz_template():
    jinja_template_src = SIMPLE_TIKZ_JINJA_TEMPLATE
    name = "World"
    _ = name

    expected_output = SIMPLE_TIKZ_RENDERED_TEMPLATE

    output = render_jinja(jinja_template_src, locals())
    assert (
        output.strip() == expected_output.strip()
    ), "Simple TikZ template was not rendered correctly"


# Test load_and_interpolate_jinja behavior when Jinja2 is not installed
def test_load_and_interpolate_jinja_no_jinja2(capsys):
    src = SIMPLE_TIKZ_JINJA_TEMPLATE
    name = "World"
    _ = name

    with patch.dict("sys.modules", {"jinja2": None}):
        output = render_jinja(src, locals())
        captured = capsys.readouterr()
        assert output is None, "Expected None when Jinja2 is not installed"
        assert (
            "Please install jinja2" in captured.err
        ), "Expected error message about missing Jinja2"


# Test rendering a complex TikZ template
COMPLEX_TIKZ_JINJA_TEMPLATE = r"""
\begin{tikzpicture}
    {% for person in people %}
    \node[draw] at ({{ person.x }},0) {Hello, {{ person.name }}!};
    {% endfor %}
\end{tikzpicture}
""".strip()


def test_render_complex_tikz_template():
    jinja_template_src = COMPLEX_TIKZ_JINJA_TEMPLATE
    people = [
        {"name": "Alice", "x": 1},
        {"name": "Bob", "x": 2},
        {"name": "Charlie", "x": 3},
    ]
    _ = people

    output = render_jinja(jinja_template_src, locals())
    assert (
        "Alice" in output
        and "Bob" in output
        and "Charlie" in output
        and "1" in output
        and "2" in output
        and "3" in output
    ), "Complex TikZ template was not rendered correctly"


def test_render_jinja_extends_template(monkeypatch, tmpdir):
    # Create the parent_tmpl.tex template.
    monkeypatch.chdir(tmpdir)
    parent_src = """Hello, {% block content -%}{% endblock -%}!"""
    parent = tmpdir / "parent_tmpl.tex"
    parent.write(parent_src)
    name = "World"
    _ = name

    child_src = (
        '{% extends "parent_tmpl.tex" %}'
        "{% block content -%}{{name}}{% endblock -%}"
        ""
    )
    output = render_jinja(child_src, locals())

    assert output == "Hello, World!"
