import pytest
from jupyter_tikz import TikZMagics, TexTemplate, TexDocument


@pytest.fixture
def tikz_magic():
    tikz_magic = TikZMagics()
    return tikz_magic


def test_show_help_on_empy_code(tikz_magic, capsys):
    # Arrange
    line = ""

    # Act
    tikz_magic.tikz(line)  # magic_line

    # Assert
    _, err = capsys.readouterr()
    assert 'Use "%tikz?" for help\n' == err


# =================== Test input type ===================
@pytest.mark.parametrize(
    "input_type", ["fulldocument", "standalonedocument", "tikz-picture", "banana"]
)
def test_invalid_input_type(input_type, tikz_magic, capsys):
    # Arrange
    line = f"--input-type {input_type}"
    cell = "any cell content"

    # Act
    tikz_magic.tikz(line, cell)

    # Assert
    _, err = capsys.readouterr()
    assert tikz_magic._get_input_type(input_type) is None
    assert (
        err
        == f"`{input_type}` is not a valid input type. Valid input types are `full-document`, `standalone-document`, or `tikzpicture`.\n"
    )


@pytest.mark.parametrize(
    "input_type, expected_input_type",
    [
        ("full-document", "full-document"),
        ("full", "full-document"),
        ("f", "full-document"),
        ("standalone-document", "standalone-document"),
        ("standalone", "standalone-document"),
        ("s", "standalone-document"),
        ("tikzpicture", "tikzpicture"),
        ("tikz", "tikzpicture"),
        ("t", "tikzpicture"),
    ],
)
def test_valid_input_type(tikz_magic, input_type, expected_input_type):
    # Arrange
    line = f"--input-type {input_type}"
    cell = "any cell content"

    # Act
    tikz_magic.tikz(line, cell)

    # Assert
    assert tikz_magic._get_input_type(input_type) == expected_input_type


@pytest.mark.parametrize(
    "input_type, expected_input_type",
    [
        ("full-document", "full-document"),
        ("full", "full-document"),
        ("f", "full-document"),
        ("standalone-document", "standalone-document"),
        ("standalone", "standalone-document"),
        ("s", "standalone-document"),
        ("tikzpicture", "tikzpicture"),
        ("tikz", "tikzpicture"),
        ("t", "tikzpicture"),
    ],
)
def test_tex_obj_type(tikz_magic, input_type, expected_input_type):
    # Arrange
    line = f"-as={input_type}"
    code = "any code"

    # Act
    tikz_magic.tikz(line, code)

    # Assert
    assert tikz_magic.input_type == expected_input_type

    if tikz_magic.input_type != "full-document":
        assert isinstance(tikz_magic.tex_obj, TexTemplate)
        assert tikz_magic.tex_obj.template == expected_input_type
    else:
        assert isinstance(tikz_magic.tex_obj, TexDocument)


# =================== Test src content ===================
def test_src_is_cell_content(tikz_magic):
    # Arrange
    code = "code"

    line = ""  # DUMMY LINE
    cell = code

    # Act
    tikz_magic.tikz(line, cell)

    # Assert
    assert tikz_magic.src == cell


def test_src_is_line_code__code_not_in_local_ns(tikz_magic):
    """
    Code param is a string, not a variable
    """

    # Arrange
    code = "code"

    line = code
    local_ns = None

    # Act
    tikz_magic.tikz(line, local_ns=local_ns)  # magic_line

    # Assert
    assert tikz_magic.src == line


def test_src_is_line__code_is_in_in_local_ns(tikz_magic):
    """
    Code param is a variable
    """

    # Arrange
    code = "code"
    line = '"$code_var"'
    local_ns = {"$code_var": code}

    # Act
    tikz_magic.tikz(line, local_ns=local_ns)

    # Assert
    assert tikz_magic.src == code
