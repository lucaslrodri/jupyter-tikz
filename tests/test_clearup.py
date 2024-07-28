from pathlib import Path

import pytest

from jupyter_tikz import TexDocument


@pytest.mark.parametrize("code", ["test code", "any code", "multi\nline\ncode"])
def test_clearup_latex_garbage(tmpdir, monkeypatch, code):
    # Arrange
    monkeypatch.chdir(tmpdir)
    exts = ["tex", "aux", "log", "pdf", "svg", "png"]
    dummy_content = "Dummy content"
    file_name = str(hash(code))

    file_path = Path(file_name)
    for ext in exts:
        file_path.with_suffix(f".{ext}").write_text(dummy_content)

    # Assert
    tex_document = TexDocument(code)
    tex_document._clearup_latex_garbage()

    # Act
    for ext in exts:
        assert not file_path.with_suffix(f".{ext}").exists()


EXAMPLE_BAD_TIKZ = "HELLO WORLD"

EXAMPLE_GOOD_TIKZ = r"""
\documentclass[tikz]{standalone}
\begin{document}
	\begin{tikzpicture}
		\draw[fill=blue] (0, 0) rectangle (1, 1);
	\end{tikzpicture}
\end{document}"""


@pytest.mark.needs_latex
@pytest.mark.needs_pdftocairo
def test_clearup_latex_garbage_no_mocks_good_tikz(tmpdir, monkeypatch):
    # Arrange
    monkeypatch.chdir(tmpdir)

    tex_document = TexDocument(EXAMPLE_GOOD_TIKZ)

    # Assert
    tex_document.run_latex()

    # Act
    garbage = Path().glob(f"{tex_document.__hash__()}.*")
    assert not list(garbage)
