import pytest
from jupyter_tikz import TexTemplate, TexDocument


def test__str__() -> None:
    # Arrange
    code = "any code"

    # Act
    tex_template = TexTemplate(code)
    tex_document = TexDocument(code)

    # Assert
    assert str(tex_template) == code
    assert str(tex_document) == code


@pytest.mark.parametrize(
    "code, expected_result",
    [
        (r"\node at(0,0) {};", r"'\\node at(0,0) {};'"),
        (
            "\\node at(0,0) {};\n\\draw (1,0) -- (2,0) -- (2,1) -- (1,1) -- cycle;",
            r"'\\node at(0,0) {};\n\\d...'",
        ),
        (
            "% comment\n\\draw (1,0) -- (2,0) -- (2,1) -- (1,1) -- cycle;",
            r"'% comment\n\\draw (1,0...'",
        ),
    ],
)
def test_get_arg_head(code, expected_result):
    tex_document = TexDocument(code)
    res = tex_document.arg_head(code, limit=20)
    assert res == expected_result


@pytest.mark.parametrize(
    "class_, kwargs, expected_result",
    [
        (
            "TexDocument",
            {},
            "TexDocument('\\\\node at(0,0) {};\\n\\\\draw (1,0) -- (2,0) -- (2,1) -- (1,1) -- ...')",
        ),
        (
            "TexDocument",
            {"ns": {"name": "World"}, "use_jinja": True},
            "TexDocument('\\\\node at(0,0) {};\\n\\\\draw (1,0) -- (2,0) -- (2,1) -- (1,1) -- ...', use_jinja=True)",
        ),
        (
            "TexTemplate",
            {
                "ns": {"name": "World"},
                "use_jinja": True,
                "preamble": "custom preamble",
            },
            "TexTemplate('\\\\node at(0,0) {};\\n\\\\draw (1,0) -- (2,0) -- (2,1) -- (1,1) -- ...', template='standalone-document', preamble='custom preamble', use_jinja=True)",
        ),
        (
            "TexTemplate",
            {
                "ns": {"name": "World"},
                "scale": 2,
            },
            "TexTemplate('\\\\node at(0,0) {};\\n\\\\draw (1,0) -- (2,0) -- (2,1) -- (1,1) -- ...', template='standalone-document', scale=2, preamble='\\\\documentclass{standalone}\\n\\\\usepackage{graphicx}\\n\\\\usepackage...')",
        ),
    ],
)
def test__repr__(kwargs, expected_result, class_) -> None:
    # Arrange
    code = "\\node at(0,0) {};\n\\draw (1,0) -- (2,0) -- (2,1) -- (1,1) -- cycle;"

    # Act
    if class_ == "TexDocument":
        obj = TexDocument(code, **kwargs)
    else:
        obj = TexTemplate(code, **kwargs)

    # Assert
    assert repr(obj) == expected_result
