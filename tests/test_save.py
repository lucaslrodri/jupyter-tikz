from pathlib import Path
import pytest
from jupyter_tikz import TexDocument


@pytest.fixture
def tex_document():
    return TexDocument("any code")


def test_save_with_invalid_format(tex_document):
    # Arrange
    src = "any_src"
    dest = "any_dest"
    format = "invalid_format"

    # Act
    with pytest.raises(ValueError) as exc_info:
        res = tex_document.save(src, dest, format)
        # Assert
        assert res is None

    assert (
        "`invalid_format` is not a valid format. Valid formats are `svg`, `png`, and `code`."
        in str(exc_info.value)
    )


def test_save_no_destination(tex_document):
    # Arrange
    src = "any_src"

    # Act
    res = tex_document.save(dest=None, src=src)

    # Assert
    assert res is None


@pytest.mark.parametrize("format", ["svg", "png"])
def test_save_src_none_format_not_code(tex_document, format):
    with pytest.raises(ValueError) as excinfo:
        tex_document.save(dest="output", src=None, format=format)
    assert "src must be provided when format is not code." in str(excinfo.value)


SAVE_TEXT_PARAMETRIZE = {
    "argnames": "ext, expected_ext",
    "argvalues": [
        ("", ".tex"),
        (".tex", ".tex"),
        (".tikz", ".tikz"),
        (".pgf", ".pgf"),
        (".txt", ".txt"),
    ],
}


@pytest.mark.parametrize(**SAVE_TEXT_PARAMETRIZE)
def test_save_code_format(tex_document, tmp_path, ext, expected_ext):
    # Arrange
    dest_path = tmp_path / f"destination{ext}"
    expected_dest_path = tmp_path / f"destination{expected_ext}"
    src = "any code"

    # Act
    res = tex_document.save(f"{dest_path}")

    # Assert

    assert expected_dest_path.read_text() == src
    assert res == f"{expected_dest_path}"


@pytest.mark.parametrize(**SAVE_TEXT_PARAMETRIZE)
def test_save_code_format_with_env_var(
    tex_document, monkeypatch, tmp_path, ext, expected_ext
):
    # Arrange
    env_dir = tmp_path / "env_var_dir"
    monkeypatch.setenv("JUPYTER_TIKZ_SAVEDIR", str(env_dir))

    dest_path = f"destination{ext}"
    expected_dest_path = (env_dir / f"destination{expected_ext}").resolve()
    src = "any code"

    # Act
    res = tex_document.save(f"{dest_path}")

    # Assert
    assert expected_dest_path.read_text() == src
    assert res == f"{expected_dest_path}"


DESTINATIONS_PARAMETRIZE = {
    "argnames": "format, destination",
    "argvalues": [
        ("svg", "image"),
        ("svg", "image.svg"),
        ("svg", "image.png"),
        ("svg", "folder/image"),
        ("svg", "folder/image.svg"),
        ("svg", "folder/image.png"),
        ("svg", "image.jpg"),
        ("png", "image"),
        ("png", "image.png"),
        ("png", "image.svg"),
    ],
}


@pytest.mark.parametrize(**DESTINATIONS_PARAMETRIZE)
def test_save_image(tex_document, format, destination, monkeypatch, tmpdir, tmp_path):
    # Arrange
    monkeypatch.chdir(tmpdir)

    src_path = tmp_path / f"source.{format}"
    dest_path = tmp_path / destination
    dummy_image = "svg content" if format == "svg" else b"png content"

    if format == "svg":
        src_path.write_text(dummy_image)
    else:
        src_path.write_bytes(dummy_image)

    # Act
    res = tex_document.save(str(dest_path), str(src_path), format)

    # Assert
    if f".{format}" != dest_path.suffix:
        dest_path = dest_path.with_suffix(dest_path.suffix + f".{format}")
    if format == "svg":
        assert dest_path.read_text() == dummy_image
    else:
        assert dest_path.read_bytes() == dummy_image
    assert res == str(dest_path.resolve())


@pytest.mark.parametrize(**DESTINATIONS_PARAMETRIZE)
def test_save_image_with_env_var(
    tex_document, tmpdir, monkeypatch, format, destination, tmp_path
):
    # Arrange
    monkeypatch.chdir(tmpdir)
    env_dir = tmp_path / "env_var_dir"
    monkeypatch.setenv("JUPYTER_TIKZ_SAVEDIR", str(env_dir))

    src_path = Path(f"source.{format}")
    dest_path = Path(destination)

    if format == "svg":
        dummy_image = "svg content"
        src_path.write_text(dummy_image)
    else:
        dummy_image = b"png content"
        src_path.write_bytes(dummy_image)

    # Act
    res = tex_document.save(str(dest_path), str(src_path), format)

    # Assert
    if f".{format}" != dest_path.suffix:
        dest_path = dest_path.with_suffix(dest_path.suffix + f".{format}")
    dest_path = (env_dir / dest_path).resolve()
    if format == "svg":
        assert dest_path.read_text() == dummy_image
    else:
        assert dest_path.read_bytes() == dummy_image
    assert res == str(dest_path)
