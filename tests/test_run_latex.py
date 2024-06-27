from jupyter_tikz import TexDocument


def run_latex_tex_inputs_is_in_env(temp_dir, tex_document, monkeypatch):
    # Arrange
    code = "any code"
    tex_document = TexDocument(code)

    monkeypatch.setenv("TEXINPUTS", temp_dir)

    # Act
    tex_document.run_latex()

    # Assert
