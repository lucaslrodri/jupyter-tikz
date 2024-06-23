import os
import pytest
from unittest.mock import patch, mock_open, MagicMock
from jupyter_tikz.jupyter_tikz import save, run_latex
from pathlib import Path
from tempfile import TemporaryDirectory

EXAMPLE_RECTANGLE_TIKZ = r"""
\documentclass[tikz]{standalone}
\begin{document}
	\begin{tikzpicture}
		\draw[fill=blue] (0, 0) rectangle (1, 1);
	\end{tikzpicture}
\end{document}
"""


def test_run_latex_save_image(tmp_path):
    src = EXAMPLE_RECTANGLE_TIKZ
    save_image_path = os.path.join(tmp_path, "output")
    expected_image_path = save_image_path + ".svg"

    # Call the function
    run_latex(src, save_image=str(save_image_path))

    # Assert that the file was created
    assert os.path.exists(expected_image_path)


def test_run_latex_save_image_rasterize(tmp_path):
    src = EXAMPLE_RECTANGLE_TIKZ
    save_image_path = os.path.join(tmp_path, "output")
    expected_image_path = save_image_path + ".svg"

    # Call the function
    run_latex(src, save_image=str(save_image_path))

    # Assert that the file was created
    assert os.path.exists(expected_image_path)


# Test environment variable handling
def test_save_with_env_var(monkeypatch):
    custom_dir = "custom_dir"
    file_name = "test.tex"

    expected_file = os.path.join(custom_dir, file_name)

    monkeypatch.setenv("JUPYTER_TIKZ_SAVEDIR", custom_dir)
    with patch("builtins.open", mock_open()) as mocked_file:
        res = save("source code", "test.tex")

        mocked_file.assert_called_with(expected_file, "w")
        assert res == expected_file


@pytest.mark.parametrize("extension", [".tex", ".tikz", ".pgf", ".txt"])
def test_save_with_custom_extension(tmpdir, extension):
    dest = os.path.join(tmpdir, f"output{extension}")
    src = "\draw (0, 0) -- (1, 1);"
    res = save(src, dest, "code")

    assert Path(dest).exists()
    assert res == dest


def test_save_extension_appending_code_extension(tmpdir):
    dest = os.path.join(tmpdir, "output")
    expected_extension = ".tex"
    src = "\draw (0, 0) -- (1, 1);"
    res = save(src, dest, "code")

    assert Path(f"{dest}{expected_extension}").exists()
    assert res == f"{dest}{expected_extension}"


def test_save_directory_creation(monkeypatch):
    with TemporaryDirectory() as tmpdirname:
        dest_path = os.path.join(tmpdirname, "new_dir/test.tex")
        monkeypatch.setattr("os.makedirs", MagicMock())
        with patch("builtins.open", mock_open()):
            save("source code", dest_path)
            os.makedirs.assert_called_with(os.path.dirname(dest_path), exist_ok=True)


def test_save_no_destination():
    src = "\draw (0, 0) -- (1, 1);"
    res = save(src, None, "code")

    assert res is None


def test_save_source_code(monkeypatch):
    src = "\draw (0, 0) -- (1, 1);"
    dest = "test_code.tex"
    monkeypatch.setattr("os.makedirs", MagicMock())
    with patch("builtins.open", mock_open()) as mocked_file:
        res = save(src, dest, "code")
        mocked_file().write.assert_called_with(src)

        assert res == dest


@pytest.mark.parametrize("format", ["svg", "png"])
def test_save_copy_image_file(format, tmp_path):
    # Setup
    src_path = os.path.join(tmp_path, f"source.{format}")
    dest_folder = os.path.join(tmp_path, "dest")
    os.mkdir(dest_folder)
    dest_path = os.path.join(dest_folder, f"source.{format}")
    with open(src_path, "w") as f:
        f.write("dummy content")

    # Action
    res = save(src_path, dest_path, format=format)

    # Assert
    assert os.path.exists(dest_path)
    assert res == dest_path


@pytest.mark.parametrize(
    "format,expected_extension", [("svg", ".svg"), ("png", ".png")]
)
def test_save_copy_image_file_and_appending_extension(
    format, expected_extension, tmp_path
):
    # Setup
    src_path = os.path.join(tmp_path, f"source")
    dest_folder = os.path.join(tmp_path, "dest")
    os.mkdir(dest_folder)
    dest_path = os.path.join(dest_folder, f"source.{expected_extension}")
    with open(src_path, "w") as f:
        f.write("dummy content")

    # Action
    res = save(src_path, dest_path, format=format)

    # Assert
    assert os.path.exists(dest_path)
    res == dest_path
