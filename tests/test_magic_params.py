import pytest

from jupyter_tikz import TikZMagics, TexTemplate, TexDocument


from jupyter_tikz.jupyter_tikz import (
    EXTRAS_CONFLITS_ERR,
    DEPRECATED_I_ERR,
    DEPRECATED_F_ERR,
    DEPRECATED_I_AND_F_ERR,
    DEPRECATED_ASJINJA_ERR,
)


@pytest.fixture
def tikz_magic():
    return TikZMagics()


@pytest.fixture
def tikz_magic_mock(mocker, tmp_path):
    tikz_magic = TikZMagics()

    def run_latex_mock(*args, **kwargs):
        _ = kwargs
        return "dummy_image"

    def save_mock(*args, **kwargs):
        _ = args
        _ = kwargs
        return args

    # def jinja_mock(*args, **kwargs):
    #     _ = args
    #     _ = kwargs
    #     return None

    mocker.patch.object(TexDocument, "run_latex", side_effect=run_latex_mock)
    mocker.patch.object(TexDocument, "save", side_effect=save_mock)
    mocker.patch.object(TexTemplate, "_build_latex_str", return_value="dummy_code")
    mocker.patch.object(
        TexTemplate, "_build_standalone_preamble", return_value="dummy preamble"
    )
    # mocker.patch.object(TexDocument, "_render_jinja", side_effect=jinja_mock)

    return tikz_magic


def test_show_help_on_empy_code(tikz_magic, capsys):
    # Arrange
    line = ""

    # Act
    tikz_magic.tikz(line)  # magic_line

    # Assert
    _, err = capsys.readouterr()
    assert 'Use "%tikz?" for help\n' == err


EXAMPLE_TIKZ_JINJA_TEMPLATE = """\\begin{tikzpicture}
    \\node[draw] at (0,0) {Hello, {{ name }}!};
\\end{tikzpicture}
"""

EXAMPLE_TIKZ_RENDERED_TEMPLATE = """\\begin{tikzpicture}
    \\node[draw] at (0,0) {Hello, World!};
\\end{tikzpicture}
"""


def test_print_jinja(tikz_magic_mock, capsys):
    # Arrange
    line = "-pj"
    cell = EXAMPLE_TIKZ_JINJA_TEMPLATE

    # Act
    tikz_magic_mock.tikz(line, cell=cell, local_ns={"name": "World"})  # magic_line

    # Assert
    out, err = capsys.readouterr()
    assert out.strip() == EXAMPLE_TIKZ_RENDERED_TEMPLATE.strip()


@pytest.mark.needs_latex
@pytest.mark.needs_pdftocairo
def test_print_jinja_no_mocks(tikz_magic, capsys):
    # Arrange
    line = "-pj"
    cell = EXAMPLE_TIKZ_JINJA_TEMPLATE

    # Act
    tikz_magic.tikz(line, cell=cell, local_ns={"name": "World"})  # magic_line

    # Assert
    out, err = capsys.readouterr()
    assert out.strip() == EXAMPLE_TIKZ_RENDERED_TEMPLATE.strip()


def test_image_none(tikz_magic_mock, mocker, capsys):
    # Arrange
    line = ""
    cell = "any cell content"
    mocker.patch.object(TexDocument, "run_latex", return_value=None)

    # Act
    res = tikz_magic_mock.tikz(line, cell)

    # Assert
    assert res is None


def test_save_tex(tikz_magic_mock):
    # Arrange
    line = "-s=any_file.tex -sv=any_local_var"
    cell = "any cell content"

    # Act
    tikz_magic_mock.tikz(line, cell)

    # Assert
    assert "any_file.tex" in tikz_magic_mock.saved_path


@pytest.mark.needs_latex
@pytest.mark.needs_pdftocairo
def test_save_tex_no_mocks(tikz_magic, mocker, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    # Arrange
    file_name = "any_file.tex"
    file_path = tmp_path / "any_file.tex"

    line = f"-s={file_name} -sv=any_local_var"
    cell = "any cell content"

    # Act
    tikz_magic.tikz(line, cell)

    # Assert
    assert file_path.read_text() == cell
    assert "any_file.tex" in tikz_magic.saved_path


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
def test_valid_input_type(tikz_magic_mock, input_type, expected_input_type):
    # Arrange
    line = f"--input-type {input_type}"
    cell = "any cell content"

    # Act
    tikz_magic_mock.tikz(line, cell)

    # Assert
    assert tikz_magic_mock._get_input_type(input_type) == expected_input_type


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
def test_tex_obj_type(tikz_magic_mock, input_type, expected_input_type):
    # Arrange
    line = f"-as={input_type}"
    code = "any code"

    # Act
    tikz_magic_mock.tikz(line, code)

    # Assert
    assert tikz_magic_mock.input_type == expected_input_type

    if tikz_magic_mock.input_type != "full-document":
        assert isinstance(tikz_magic_mock.tex_obj, TexTemplate)
        assert tikz_magic_mock.tex_obj.template == expected_input_type
    else:
        assert isinstance(tikz_magic_mock.tex_obj, TexDocument)


# =================== Test src content ===================
def test_src_is_cell_content(tikz_magic_mock):
    # Arrange
    code = "code"

    line = ""  # DUMMY LINE
    cell = code

    # Act
    tikz_magic_mock.tikz(line, cell)

    # Assert
    assert tikz_magic_mock.src == cell


def test_src_is_line_code__code_not_in_local_ns(tikz_magic_mock):
    """
    Code param is a string, not a variable
    """

    # Arrange
    code = "code"

    line = code
    local_ns = None

    # Act
    tikz_magic_mock.tikz(line, local_ns=local_ns)  # magic_line

    # Assert
    assert tikz_magic_mock.src == line


def test_src_is_line__code_is_in_in_local_ns(tikz_magic_mock):
    """
    Code param is a variable
    """

    # Arrange
    code = "code"
    line = '"$code_var"'
    local_ns = {"$code_var": code}

    # Act
    tikz_magic_mock.tikz(line, local_ns=local_ns)

    # Assert
    assert tikz_magic_mock.src == code


# =================== Raise errors ===================
@pytest.mark.parametrize(
    "args",
    [
        "-t=a,b,c",
        "-l=d,e,f",
        "-lp=g,h,i",
        "-t=a,b,c -l=d,e,f",
        "-t=a,b,c -l=d,e,f -lp=g,h,i",
    ],
)
def test_raise_error_tex_preamble_and_extras_not_allowed_at_same_time(
    tikz_magic_mock, capsys, args
):
    # Arrange
    line = f"-preamble=any_preamble {args}"
    cell = "any cell content"

    # Act
    tikz_magic_mock.tikz(line, cell)

    # Assert
    _, err = capsys.readouterr()
    assert EXTRAS_CONFLITS_ERR + "\n" == err


@pytest.mark.parametrize(
    "args, expected_err",
    [
        ("-i -f", DEPRECATED_I_AND_F_ERR),
        ("-i -as=f", DEPRECATED_I_ERR),
        ("-i", DEPRECATED_I_ERR),
        ("-f -as=t", DEPRECATED_F_ERR),
        ("-f", DEPRECATED_F_ERR),
        ("--as-jinja", DEPRECATED_ASJINJA_ERR),
    ],
)
def test_raise_deprecated_args(tikz_magic_mock, capsys, args, expected_err):
    # Arrange
    line = args
    cell = "any cell content"

    # Act
    res = tikz_magic_mock.tikz(line, cell)

    # Assert
    _, err = capsys.readouterr()
    assert f"{expected_err}\n" == err
    assert res is None
