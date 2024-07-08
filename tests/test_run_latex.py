import os
import subprocess
import tempfile
from pathlib import Path
from unittest.mock import ANY

import pytest
from IPython import display

from jupyter_tikz import TexDocument


@pytest.fixture
def tex_document():
    return TexDocument("any code")


# ========================= texinputs env =========================


def test_texinputs_already_set(tex_document, tmp_path, monkeypatch):
    # Arrange
    initial_texinputs = f'{tmp_path / "LaTeX" / "local"}' + os.pathsep * 2
    monkeypatch.setenv("TEXINPUTS", initial_texinputs)

    current_dir = f'{tmp_path / "current_dir"}'

    expected_res = f"{current_dir}" + os.pathsep + initial_texinputs

    # Act
    res = tex_document._modify_texinputs(current_dir)

    # Assert
    assert res["TEXINPUTS"] == expected_res


def test_texinputs_not_set(tex_document, tmp_path, monkeypatch):
    # Arrange
    monkeypatch.delenv("TEXINPUTS", raising=False)

    current_dir = f'{tmp_path / "current_dir"}'

    expected_res = "." + os.pathsep + f"{current_dir}" + os.pathsep * 2

    # Act
    res = tex_document._modify_texinputs(current_dir)

    # Assert
    assert res["TEXINPUTS"] == expected_res


# ========================= run_command =========================


@pytest.mark.parametrize(
    "stdout, stderr, expected_err",
    [
        ("", "Error stderr", "Error stderr\n"),
        ("Error stdout", "", "Error stdout\n"),
        ("Error stdout", "Error stderr", "Error stderr\n"),
    ],
)
def test_run_command_failure(
    tex_document, mocker, capsys, tmp_path, stdout, stderr, expected_err
):
    # Arrange
    command = "command"
    mocker.patch.object(
        subprocess,
        "run",
        return_value=subprocess.CompletedProcess(command, 1, stdout, stderr),
    )

    # Act
    res = tex_document._run_command(command, working_dir=tmp_path)

    # Assert
    _, err = capsys.readouterr()
    assert res == 1
    assert expected_err == err


def test_run_command_invalid_command(tex_document, capsys, tmp_path):
    # Arrange
    command = "invalid_command"

    # Act
    res = tex_document._run_command(command, working_dir=tmp_path)

    # Assert
    _, err = capsys.readouterr()
    assert command in err.lower()
    assert res == 1


DUMMY_COMMAND = "dummy_command"


@pytest.fixture
def tex_document_mock__run_command(
    mocker, tex_document, very_long_err_msg_stdout, very_long_err_msg_stderr
):
    command = DUMMY_COMMAND
    mocker.patch.object(
        subprocess,
        "run",
        return_value=subprocess.CompletedProcess(
            command, 1, very_long_err_msg_stdout, very_long_err_msg_stderr
        ),
    )
    return tex_document


PARAMETRIZE_ARGS__RUN_COMMAND = {
    "argnames": "very_long_err_msg_stdout, very_long_err_msg_stderr",
    "argvalues": [
        ("fatal error stdout\n" * 100, ""),
        ("", "fatal error stderr\n" * 100),
        ("fatal error stdout\n" * 100, "fatal error stderr\n" * 100),
    ],
}


@pytest.mark.parametrize(**PARAMETRIZE_ARGS__RUN_COMMAND)
def test_run_command_tail_long_err_msg(tex_document_mock__run_command, capsys):
    # Arrange
    # Act
    res = tex_document_mock__run_command._run_command(
        DUMMY_COMMAND, working_dir="dummy_dir"
    )

    # Assert
    assert res == 1
    _, err = capsys.readouterr()
    assert len(err.splitlines()) == 20


@pytest.mark.parametrize(**PARAMETRIZE_ARGS__RUN_COMMAND)
def test_run_command_show_full_long_err_msg(tex_document_mock__run_command, capsys):
    # Arrange
    # Act
    res = tex_document_mock__run_command._run_command(
        DUMMY_COMMAND, working_dir="dummy_dir", full_err=True
    )

    # Assert
    assert res == 1
    _, err = capsys.readouterr()
    assert len(err.splitlines()) > 20


@pytest.mark.needs_latex
def test_run_command_invalid_pdflatex(tex_document, capsys, tmp_path):
    # Arrange
    command = "pdflatex not_exists.tex"

    # Act
    res = tex_document._run_command(command, working_dir=tmp_path)

    # Assert
    _, err = capsys.readouterr()
    assert "pdflatex" in err
    assert "fatal error" in err.lower()
    assert res == 1


@pytest.mark.needs_latex
def test_run_command_valid_pdflatex(tex_document, tmp_path):
    # Arrange
    command = "pdflatex --help"

    # Act
    res = tex_document._run_command(command, working_dir=tmp_path)

    # Assert
    assert res == 0


# =========================== run_latex ===========================


class TemporaryDirectoryMock:
    def __init__(self, tmpdir):
        self.name = tmpdir

    def __enter__(self):
        return self.name

    def __exit__(self, *_):
        pass


@pytest.fixture
def tex_document_mock__run_latex(mocker, tex_document, tmpdir):
    # current_dir = request.fspath.dirname
    # # env = {"TEXINPUTS": "." + os.pathsep + f"{current_dir}" + os.pathsep * 2}
    # # mocker.patch.object(
    # #     tex_document,
    # #     "_modify_texinputs",
    # #     return_value=env,
    # # )
    mocker.patch.object(
        tempfile, "TemporaryDirectory", return_value=TemporaryDirectoryMock(tmpdir)
    )
    mocker.patch.object(
        subprocess,
        "run",
        return_value=subprocess.CompletedProcess("dummy_command", 0, "", ""),
    )
    mocker.patch.object(display, "SVG", return_value="SVG")
    mocker.patch.object(display, "Image", return_value="Image")

    return tex_document


@pytest.mark.parametrize(
    "tex_program, tex_args",
    [
        ("pdflatex", ""),
        (
            "pdflatex",
            "--enable-write18 --extra-mem-top=10000000 --extra-mem-bot=10000000",
        ),
        ("lualatex", ""),
    ],
)
def test_run_latex__valid_tex_program(
    tex_document_mock__run_latex, tmp_path, mocker, tex_program, tex_args
):
    # Arrange
    full_err = False

    spy = mocker.spy(tex_document_mock__run_latex, "_run_command")

    if tex_args:
        expected_command = f"{tex_program} {tex_args} {tmp_path / 'tikz.tex'}"
    else:
        expected_command = f"{tex_program} {tmp_path / 'tikz.tex'}"

    # Act
    tex_document_mock__run_latex.run_latex(
        tex_program=tex_program, tex_args=tex_args, full_err=full_err
    )

    # Assert
    spy.assert_any_call(expected_command, ANY, ANY, env=ANY)


def test_pdf_cairo_custom_path(
    tex_document_mock__run_latex, monkeypatch, mocker, tmp_path
):
    # Arrange
    pdf_to_cairo_path = f"{tmp_path / 'pdftocairo_dir'/ 'pdftocairo.exe'}"

    monkeypatch.setenv(
        "JUPYTER_TIKZ_PDFTOCAIROPATH",
        pdf_to_cairo_path,
    )
    output_stem = tmp_path / "tikz"
    full_err = False

    spy = mocker.spy(tex_document_mock__run_latex, "_run_command")

    expected_command = f"{pdf_to_cairo_path} -svg {output_stem}.pdf {output_stem}.svg"

    # Act
    tex_document_mock__run_latex.run_latex(full_err=full_err)

    # Assert
    spy.assert_called_with(expected_command, tmp_path, full_err)


def test_pdf_cairo_default_path(tex_document_mock__run_latex, mocker, tmp_path):
    # Arrange
    output_stem = tmp_path / "tikz"
    full_err = False

    spy = mocker.spy(tex_document_mock__run_latex, "_run_command")

    expected_command = f"pdftocairo -svg {output_stem}.pdf {output_stem}.svg"

    # Act
    res = tex_document_mock__run_latex.run_latex(full_err=full_err)

    # Assert
    spy.assert_called_with(expected_command, tmp_path, full_err)
    assert res == "SVG"


def test_pdf_cairo_rasterize(tex_document_mock__run_latex, mocker, tmp_path):
    # Arrange
    output_stem = tmp_path / "tikz"
    full_err = False
    rasterize = True
    dpi = 300

    spy = mocker.spy(tex_document_mock__run_latex, "_run_command")

    expected_command = (
        f"pdftocairo -png -singlefile -transp -r {dpi} {output_stem}.pdf {output_stem}"
    )

    # Act
    res = tex_document_mock__run_latex.run_latex(
        full_err=full_err, rasterize=rasterize, dpi=dpi
    )

    # Assert
    spy.assert_called_with(expected_command, tmp_path, full_err)
    assert res == "Image"


def run_command_fail_side_effect_pdf_latex(*args, **kwargs):
    _ = kwargs
    if "pdflatex" in args[0]:
        return subprocess.CompletedProcess("pdflatex", 1, "", "Error")
    return subprocess.CompletedProcess("pdftocairo", 0, "", "")


def test_failed_latex_command(tex_document_mock__run_latex, mocker, capsys):
    # Arrange
    mocker.patch.object(
        subprocess,
        "run",
        side_effect=run_command_fail_side_effect_pdf_latex,
    )

    # Act
    res = tex_document_mock__run_latex.run_latex()

    # Assert
    assert res is None
    _, err = capsys.readouterr()
    assert "error" in err.lower()


def run_command_fail_side_effect_pdftocairo(*args, **kwargs):
    _ = kwargs
    if "pdftocairo" in args[0]:
        return subprocess.CompletedProcess("pdftocairo", 1, "", "Error")
    return subprocess.CompletedProcess("pdflatex", 0, "", "")


def test_passed_latex_but_failed_pdftocairo(
    tex_document_mock__run_latex, mocker, capsys
):
    # Arrange
    mocker.patch.object(
        subprocess,
        "run",
        side_effect=run_command_fail_side_effect_pdftocairo,
    )

    # Act
    res = tex_document_mock__run_latex.run_latex()

    # Assert
    assert res is None
    _, err = capsys.readouterr()
    assert "error" in err.lower()


@pytest.mark.parametrize("rasterize", [False, True])
def test_run_latex_save_image_call(
    tex_document_mock__run_latex, mocker, tmp_path, rasterize
):
    # Arrange
    def side_effect_save_image(*args, **kwargs):
        return str(tmp_path / args[0])

    format = "png" if rasterize else "svg"

    expected_path = tmp_path / f"tikz.{format}"

    image = f"image.{format}"
    mocker.patch.object(
        tex_document_mock__run_latex, "save", side_effect=side_effect_save_image
    )

    # Act
    res = tex_document_mock__run_latex.run_latex(save_image=image, rasterize=rasterize)

    # Assert
    tex_document_mock__run_latex.save.assert_called_once_with(
        image, str(expected_path), format
    )


# ========================= texinputs env - no mocks =========================

EXAMPLE_VIEWBOX_CODE_INPUT = r"""
\draw (-2.5,-2.5) rectangle (5,5);
"""
EXAMPLE_PARENT_WITH_INPUT_COMMANDT = r"""
\documentclass[tikz]{standalone}
\begin{document}
    \begin{tikzpicture}
        \input{viewbox.tex}
        \node[draw] at (0,0) {Hello, World!};
    \end{tikzpicture}
\end{document}    
"""


@pytest.mark.needs_latex
@pytest.mark.needs_pdftocairo
def test_texinputs_no_mocks(monkeypatch, tmpdir):
    # Arrange
    monkeypatch.chdir(tmpdir)
    viewbox_code = EXAMPLE_VIEWBOX_CODE_INPUT
    child = tmpdir / "viewbox.tex"
    child.write(viewbox_code)

    # Act
    tex_document = TexDocument(EXAMPLE_PARENT_WITH_INPUT_COMMANDT)
    res = tex_document.run_latex()

    # Assert
    assert isinstance(res, display.SVG)


# =========================== run_latex - no mocks ===========================
EXAMPLE_BAD_TIKZ = "HELLO WORLD"

EXAMPLE_GOOD_TIKZ = r"""
\documentclass[tikz]{standalone}
\begin{document}
	\begin{tikzpicture}
		\draw[fill=blue] (0, 0) rectangle (1, 1);
	\end{tikzpicture}
\end{document}"""
RENDERED_SVG_GOOD_TIKZ = '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="28.745" height="28.745" viewBox="0 0 28.745 28.745">\n<defs>\n<clipPath id="clip-0">\n<path clip-rule="nonzero" d="M 0 0 L 28.492188 0 L 28.492188 28.492188 L 0 28.492188 Z M 0 0 "/>\n</clipPath>\n</defs>\n<g clip-path="url(#clip-0)">\n<path fill-rule="nonzero" fill="rgb(0%, 0%, 100%)" fill-opacity="1" stroke-width="0.3985" stroke-linecap="butt" stroke-linejoin="miter" stroke="rgb(0%, 0%, 0%)" stroke-opacity="1" stroke-miterlimit="10" d="M -0.00195486 -0.00189963 L -0.00195486 28.345014 L 28.344959 28.345014 L 28.344959 -0.00189963 Z M -0.00195486 -0.00189963 " transform="matrix(0.991207, 0, 0, -0.991207, 0.19725, 28.294992)"/>\n</g>\n</svg>'


@pytest.mark.needs_latex
@pytest.mark.needs_pdftocairo
def test_run_latex_good_input_with_no_aditional_params(monkeypatch, tmpdir):
    # Arrange
    monkeypatch.chdir(tmpdir)

    # Act
    tex_document = TexDocument(EXAMPLE_GOOD_TIKZ)
    res = tex_document.run_latex()
    expected_res = RENDERED_SVG_GOOD_TIKZ

    assert isinstance(res, display.SVG)
    assert res.data == expected_res


@pytest.mark.needs_latex
@pytest.mark.needs_pdftocairo
def test_run_latex_bad_input(monkeypatch, tmpdir, capsys):
    # Arrange
    monkeypatch.chdir(tmpdir)

    # Act
    tex_document = TexDocument(EXAMPLE_BAD_TIKZ)
    res = tex_document.run_latex()

    assert res is None

    _, err = capsys.readouterr()
    assert "error" in err.lower()
    assert len(err.splitlines()) == 20


@pytest.mark.needs_latex
@pytest.mark.needs_pdftocairo
def test_run_latex_bat_input_full_err(monkeypatch, tmpdir, capsys):
    # Arrange
    monkeypatch.chdir(tmpdir)

    # Act
    tex_document = TexDocument(EXAMPLE_BAD_TIKZ)
    res = tex_document.run_latex(full_err=True)

    assert res is None

    _, err = capsys.readouterr()
    assert "error" in err.lower()
    assert len(err.splitlines()) > 20


@pytest.mark.needs_latex
@pytest.mark.needs_pdftocairo
@pytest.mark.parametrize(
    "texprogram, texargs",
    [
        ("pdflatex", ""),
        (
            "pdflatex",
            "--enable-write18 --extra-mem-top=10000000 --extra-mem-bot=10000000",
        ),
        ("lualatex", ""),
    ],
)
def test_run_latex_custom_tex_command(monkeypatch, tmpdir, texprogram, texargs):
    # Arrange
    monkeypatch.chdir(tmpdir)

    # Act
    tex_document = TexDocument(EXAMPLE_GOOD_TIKZ)
    res = tex_document.run_latex(tex_program=texprogram, tex_args=texargs)
    expected_res = RENDERED_SVG_GOOD_TIKZ

    assert isinstance(res, display.SVG)
    assert res.data == expected_res


@pytest.mark.needs_latex
@pytest.mark.needs_pdftocairo
def test_run_latex_rasterize_with_no_additional_commands(monkeypatch, tmpdir):
    # Arrange
    monkeypatch.chdir(tmpdir)

    # Act
    tex_document = TexDocument(EXAMPLE_GOOD_TIKZ)
    res = tex_document.run_latex(rasterize=True)

    assert isinstance(res, display.Image)


@pytest.mark.needs_latex
@pytest.mark.needs_pdftocairo
@pytest.mark.parametrize("dpi", [48, 150, 300, 600])
def test_run_latex_rasterize_with_dpi(monkeypatch, tmpdir, dpi):
    # Arrange
    monkeypatch.chdir(tmpdir)

    # Act
    tex_document = TexDocument(EXAMPLE_GOOD_TIKZ)
    res = tex_document.run_latex(rasterize=True, dpi=dpi)
    expected_res = display.Image

    assert isinstance(res, display.Image)
    assert isinstance(res, expected_res)


@pytest.mark.needs_latex
@pytest.mark.needs_pdftocairo
@pytest.mark.skipif(
    not os.path.exists(
        os.path.expandvars("$LOCALAPPDATA/Poppler/Library/bin/pdftocairo.exe")
    ),
    reason="pdftocairo not found",
)
def test_run_latex_with_custom_pdftocairo_path(monkeypatch, tmpdir):
    # Arrange
    monkeypatch.chdir(tmpdir)
    # IMPORTANT: Modify this path to the path of pdftocairo.exe in your system
    pdftocairo_path = os.path.expandvars(
        "$LOCALAPPDATA/Poppler/Library/bin/pdftocairo.exe"
    )
    monkeypatch.setenv("JUPYTER_TIKZ_PDFTOCAIROPATH", pdftocairo_path)

    # Act
    tex_document = TexDocument(EXAMPLE_GOOD_TIKZ)
    res = tex_document.run_latex()
    expected_res = RENDERED_SVG_GOOD_TIKZ

    # Assert
    assert isinstance(res, display.SVG)
    assert res.data == expected_res


@pytest.mark.needs_latex
def test_run_latex_invalid_pdftocairo_path(monkeypatch, tmpdir, capsys):
    # Arrange
    monkeypatch.chdir(tmpdir)
    pdfcairo_path = "invalid_path/agfdgfdgdfgdfgfdgbcvvc"
    monkeypatch.setenv("JUPYTER_TIKZ_PDFTOCAIROPATH", pdfcairo_path)

    # Act
    tex_document = TexDocument(EXAMPLE_GOOD_TIKZ)
    res = tex_document.run_latex()

    # Assert
    assert res == None
    _, err = capsys.readouterr()
    assert len(err) > 0


# =========================== save - no mocks ===========================

SAVE_PARAMETRIZE = {
    "argnames": "rasterize, dest, expected_dest",
    "argvalues": [
        (False, "image", "image.svg"),
        (False, "image.svg", "image.svg"),
        (False, "image.png", "image.png.svg"),
        (False, "folder/image.svg", "folder/image.svg"),
        (False, "folder/image.jpg", "folder/image.jpg.svg"),
        (True, "image", "image.png"),
        (True, "image.png", "image.png"),
        (True, "image.svg", "image.svg.png"),
        (True, "folder/image.png", "folder/image.png"),
        (True, "folder/image.gif", "folder/image.gif.png"),
    ],
}


@pytest.mark.needs_latex
@pytest.mark.needs_pdftocairo
@pytest.mark.parametrize(**SAVE_PARAMETRIZE)
def test_run_latex_save_image(
    tex_document, tmpdir, monkeypatch, rasterize, dest, expected_dest
):
    # Arrange
    monkeypatch.chdir(tmpdir)
    image_path = Path(tmpdir) / expected_dest

    # Arrange
    tex_document.full_latex = EXAMPLE_GOOD_TIKZ

    # Act
    tex_document.run_latex(save_image=dest, rasterize=rasterize)

    # Assert
    assert image_path.exists()


@pytest.mark.needs_latex
@pytest.mark.needs_pdftocairo
@pytest.mark.parametrize(**SAVE_PARAMETRIZE)
def test_run_latex_save_image_absolute_tmp_path(
    tex_document, tmp_path, monkeypatch, rasterize, dest, expected_dest
):
    # Arrange
    env_dir = tmp_path / "env_var_dir"
    monkeypatch.setenv("JUPYTER_TIKZ_SAVEDIR", str(env_dir))
    monkeypatch.chdir(tmp_path)
    image_path = env_dir / expected_dest

    # Arrange
    tex_document.full_latex = EXAMPLE_GOOD_TIKZ

    # Act
    tex_document.run_latex(save_image=dest, rasterize=rasterize)

    # Assert
    assert image_path.exists()


@pytest.mark.needs_latex
@pytest.mark.needs_pdftocairo
@pytest.mark.parametrize(**SAVE_PARAMETRIZE)
def test_run_latex_save_image_relative_tmp_path(
    tex_document, tmp_path, monkeypatch, rasterize, dest, expected_dest
):
    # Arrange
    env_dir = tmp_path / "env_var_dir"
    monkeypatch.setenv("JUPYTER_TIKZ_SAVEDIR", str(env_dir))
    monkeypatch.chdir(tmp_path)
    image_path = env_dir / expected_dest

    # Arrange
    tex_document.full_latex = EXAMPLE_GOOD_TIKZ

    # Act
    tex_document.run_latex(save_image=dest, rasterize=rasterize)

    # Assert
    assert image_path.exists()


# =========================== jinja - no mocks ===========================

EXAMPLE_JINJA_TEMPLATE = r"""
\documentclass[tikz]{standalone}
\begin{document}
    \begin{tikzpicture}
        {% for person in people %}
        \node[draw] at (0,{{ person.y }}) {Hello, {{ person.name }}!};
        {% endfor %}
    \end{tikzpicture}
\end{document}"""


@pytest.mark.needs_latex
@pytest.mark.needs_pdftocairo
def test_jinja_template():
    # Arrange
    people = [
        {"name": "Alice", "y": 0},
        {"name": "Bob", "y": 2},
        {"name": "Charlie", "y": 4},
    ]

    # Act
    tex_document = TexDocument(
        EXAMPLE_JINJA_TEMPLATE, use_jinja=True, ns={"people": people}
    )
    res = tex_document.run_latex()

    # Assert
    assert isinstance(res, display.SVG)


EXAMPLE_JINJA_PARENT_TEMPLATE = r"""
\documentclass[tikz]{standalone}
\begin{document}
	\begin{tikzpicture}
        \draw (-2.5,-2.5) rectangle (5,5);
        {% block content %}{% endblock %}
	\end{tikzpicture}
\end{document}"""

EXAMPLE_JINJA_CHILD_TEMPLATE = """{% extends 'parent_tmpl.tex' %}
{% block content %}
    \node[draw] at (0,0) {Hello, {{ name }}!};
{% endblock %}
"""


@pytest.mark.needs_latex
@pytest.mark.needs_pdftocairo
def test_jinja_extends_template(tmpdir, monkeypatch):
    # Arrange
    monkeypatch.chdir(tmpdir)
    parent_code = EXAMPLE_JINJA_PARENT_TEMPLATE
    parent = tmpdir / "parent_tmpl.tex"
    parent.write(parent_code)

    # Act
    tex_document = TexDocument(
        EXAMPLE_JINJA_CHILD_TEMPLATE, use_jinja=True, ns={"name": "World"}
    )
    res = tex_document.run_latex()

    # Assert
    assert isinstance(res, display.SVG)
