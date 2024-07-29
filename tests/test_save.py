from pathlib import Path

import pytest
from IPython.display import SVG, Image

from jupyter_tikz import TexDocument

LATEX_CODE = r"""\documentclass{standalone}
\usepackage{tikz}
\begin{document}
\begin{tikzpicture}
    \draw[fill=blue] (0, 0) rectangle (1, 1);
\end{tikzpicture}
\end{document}"""

TIKZ_CODE = r"""\begin{tikzpicture}
    \draw[fill=blue] (0, 0) rectangle (1, 1);
\end{tikzpicture}"""


def test_tikz_code():
    # Arrange
    tex_document = TexDocument(LATEX_CODE)

    # Act
    res = tex_document.tikz_code

    # Assert
    assert res == TIKZ_CODE


DESTINATIONS_TIKZ_PARAMETRIZE = {
    "argnames": "file_name, expected_file_name",
    "argvalues": [
        ("test", "test.tikz"),
        ("test.tikz", "test.tikz"),
        ("folder/test folder/test.tikz", "folder/test folder/test.tikz"),
        ("folder/test folder/test", "folder/test folder/test.tikz"),
        ("folder/test folder/test.png", "folder/test folder/test.png.tikz"),
    ],
}


@pytest.mark.parametrize(**DESTINATIONS_TIKZ_PARAMETRIZE)
def test__save_tikz(tmpdir, monkeypatch, file_name, expected_file_name):
    # Arrange
    monkeypatch.chdir(tmpdir)
    tex_document = TexDocument(LATEX_CODE)

    # Act
    tex_document._save(file_name, "tikz")
    expected_file = Path(expected_file_name)

    # Assert
    assert expected_file.exists()
    assert expected_file.read_text() == TIKZ_CODE


@pytest.mark.parametrize(**DESTINATIONS_TIKZ_PARAMETRIZE)
def test__save_tikz_replace(tmpdir, monkeypatch, file_name, expected_file_name):
    # Arrange
    monkeypatch.chdir(tmpdir)
    tex_document = TexDocument(LATEX_CODE)

    file_path = Path(file_name)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text("Dummy content")

    # Act
    tex_document._save(file_name, "tikz")
    expected_file = Path(expected_file_name)

    # Assert
    assert expected_file.exists()
    assert expected_file.read_text() == TIKZ_CODE


def test__tikz_code_no_tikz_code(tmp_path, monkeypatch):
    # Arrange
    monkeypatch.chdir(tmp_path)

    # Act
    tex_document = TexDocument("No tikz code")

    # Assert
    assert tex_document.tikz_code == None


def test__save_tikz_no_tikz(tmpdir, monkeypatch):
    # Arrange
    monkeypatch.chdir(tmpdir)

    # Act
    tex_document = TexDocument("No tikz code")

    # Assert
    with pytest.raises(ValueError, match="No TikZ code to save."):
        tex_document._save("file", "tikz")


@pytest.mark.parametrize(**DESTINATIONS_TIKZ_PARAMETRIZE)
def test__save_tikz_env_dest(tmpdir, monkeypatch, file_name, expected_file_name):
    # Arrange
    monkeypatch.chdir(tmpdir)
    env_dir = tmpdir / "env_var_dir"
    monkeypatch.setenv("JUPYTER_TIKZ_SAVEDIR", str(env_dir))
    tex_document = TexDocument(LATEX_CODE)

    # Act
    tex_document._save(file_name, "tikz")
    expected_file = env_dir / expected_file_name

    # Assert
    assert expected_file.exists()
    assert Path(expected_file).read_text() == TIKZ_CODE


DESTINATIONS_OTHER_EXTS_PARAMETRIZE = {
    "argnames": "ext, file_name, expected_file_name",
    "argvalues": [
        ("tex", "test.tex", "test.tex"),
        ("tex", "test", "test.tex"),
        ("tex", "test.png", "test.png.tex"),
        ("tex", "another folder/another file", "another folder/another file.tex"),
        ("png", "test.png", "test.png"),
        ("png", "test", "test.png"),
        ("png", "another folder/another file", "another folder/another file.png"),
        ("svg", "another test.svg", "another test.svg"),
        ("svg", "another test", "another test.svg"),
        ("pdf", "yet another test file.pdf", "yet another test file.pdf"),
        ("pdf", "file", "file.pdf"),
        ("pdf", "folder/file.pdf", "folder/file.pdf"),
    ],
}


@pytest.mark.parametrize(**DESTINATIONS_OTHER_EXTS_PARAMETRIZE)
def test__save_others_exts(tmpdir, monkeypatch, ext, file_name, expected_file_name):
    # Arrange
    monkeypatch.chdir(tmpdir)
    tex_document = TexDocument(LATEX_CODE)
    dummy_file = Path(hex(abs(hash(LATEX_CODE)))[2:]).with_suffix(f".{ext}")
    dummy_file.write_text("Dummy content")

    # Act
    tex_document._save(file_name, ext)
    expected_file = Path(expected_file_name)

    # Assert

    assert expected_file.exists()
    assert expected_file.read_text() == "Dummy content"


@pytest.mark.parametrize(**DESTINATIONS_OTHER_EXTS_PARAMETRIZE)
def test__save_others_exts_replace(
    tmpdir, monkeypatch, ext, file_name, expected_file_name
):
    # Arrange
    monkeypatch.chdir(tmpdir)
    tex_document = TexDocument(LATEX_CODE)
    dummy_file = Path(hex(abs(hash(LATEX_CODE)))[2:]).with_suffix(f".{ext}")
    dummy_file.write_text("Dummy content")

    file_path = Path(file_name)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text("Dummy content")

    # Act
    tex_document._save(file_name, ext)
    expected_file = Path(expected_file_name)

    # Assert

    assert expected_file.exists()
    assert expected_file.read_text() == "Dummy content"


@pytest.mark.parametrize(**DESTINATIONS_OTHER_EXTS_PARAMETRIZE)
def test__save_others_exts_env_dest(
    tmpdir, monkeypatch, ext, file_name, expected_file_name
):
    # Arrange
    monkeypatch.chdir(tmpdir)
    env_dir = tmpdir / "env_var_dir"
    monkeypatch.setenv("JUPYTER_TIKZ_SAVEDIR", str(env_dir))

    dummy_file = Path(hex(abs(hash(LATEX_CODE)))[2:]).with_suffix(f".{ext}")
    dummy_file.write_text("Dummy content")
    tex_document = TexDocument(LATEX_CODE)

    # Act
    tex_document._save(file_name, ext)
    expected_file = env_dir / expected_file_name

    # Assert
    assert expected_file.exists()
    assert Path(expected_file).read_text() == "Dummy content"


# =========================== run_latex ===========================
@pytest.mark.needs_latex
@pytest.mark.needs_pdftocairo
@pytest.mark.parametrize(
    "save_tex, expected_file",
    [
        ("test.tex", "test.tex"),
        ("test.txt", "test.txt.tex"),
        ("folder/test", "folder/test.tex"),
    ],
)
def test_save_latex(tmpdir, monkeypatch, save_tex, expected_file):
    # Arrange
    monkeypatch.chdir(tmpdir)
    tex_document = TexDocument(LATEX_CODE)

    # Act
    tex_document.run_latex(save_tex=save_tex)

    # Assert
    assert Path(expected_file).exists()
    assert Path(expected_file).read_text() == LATEX_CODE


@pytest.mark.needs_latex
@pytest.mark.needs_pdftocairo
@pytest.mark.parametrize(
    "save_tikz, expected_file",
    [
        ("test.tikz", "test.tikz"),
        ("test.tex", "test.tex.tikz"),
        ("folder/test", "folder/test.tikz"),
    ],
)
def test_save_tikz(tmpdir, monkeypatch, save_tikz, expected_file):
    # Arrange
    monkeypatch.chdir(tmpdir)
    tex_document = TexDocument(LATEX_CODE)

    # Act
    res = tex_document.run_latex(save_tikz=save_tikz)

    # Assert
    assert Path(expected_file).exists()
    assert Path(expected_file).read_text() == TIKZ_CODE
    assert isinstance(res, SVG)


@pytest.mark.needs_latex
@pytest.mark.needs_pdftocairo
@pytest.mark.parametrize(
    "save_image, expected_file",
    [
        ("test.svg", "test.svg"),
        ("test.jpg", "test.jpg.svg"),
        ("test", "test.svg"),
        ("folder/test", "folder/test.svg"),
    ],
)
def test_save_image_svg(tmpdir, monkeypatch, save_image, expected_file):
    # Arrange
    monkeypatch.chdir(tmpdir)
    tex_document = TexDocument(LATEX_CODE)

    # Act
    res = tex_document.run_latex(save_image=save_image)

    # Assert
    assert Path(expected_file).exists()
    assert isinstance(res, SVG)


@pytest.mark.needs_latex
@pytest.mark.needs_pdftocairo
@pytest.mark.parametrize(
    "save_image, expected_file",
    [
        ("test.png", "test.png"),
        ("test.jpg", "test.jpg.png"),
        ("test", "test.png"),
        ("folder/test.png", "folder/test.png"),
    ],
)
def test_save_image_png(tmpdir, monkeypatch, save_image, expected_file):
    # Arrange
    monkeypatch.chdir(tmpdir)
    tex_document = TexDocument(LATEX_CODE)

    # Act
    res = tex_document.run_latex(save_image=save_image, rasterize=True)

    # Assert
    assert Path(expected_file).exists()
    assert isinstance(res, Image)


@pytest.mark.needs_latex
@pytest.mark.needs_pdftocairo
@pytest.mark.parametrize(
    "save_pdf, expected_file",
    [
        ("test.pdf", "test.pdf"),
        ("test.docx", "test.docx.pdf"),
        ("test", "test.pdf"),
        ("folder/test", "folder/test.pdf"),
    ],
)
def test_save_pdf(tmpdir, monkeypatch, save_pdf, expected_file):
    # Arrange
    monkeypatch.chdir(tmpdir)
    tex_document = TexDocument(LATEX_CODE)

    # Act
    res = tex_document.run_latex(save_pdf=save_pdf)

    # Assert
    assert Path(expected_file).exists()
    assert isinstance(res, SVG)
