from IPython.display import SVG, Image
from IPython.testing.globalipapp import get_ipython
import pytest

ipy = get_ipython()
ipy.run_line_magic("load_ext", "jupyter_tikz")

EXAMPLE_LINE_TIKZ = "\\draw (0,0) -- (1,1);"
EXAMPLE_TIKZ_INPUT = r"\input{component.tikz}"


def test_user_ns_save_parameter_var_name():
    var_name = "test_var"
    line = f"-sv {var_name} -i"
    cell = EXAMPLE_LINE_TIKZ

    ipy.run_cell_magic("tikz", line, cell)

    assert var_name in ipy.user_ns
    assert ipy.user_ns[var_name] == EXAMPLE_LINE_TIKZ
    # assert EXAMPLE_LINE_TIKZ == ipy.user_ns[var_name].value


@pytest.mark.skip(reason="Not implemented yet")
def test_user_ns_local_folder(tmpdir):
    local_folder = tmpdir.mkdir("local_folder")
    with local_folder.as_cwd():
        with open("component.tikz", "w") as f:
            f.write(EXAMPLE_LINE_TIKZ)

        line = "-i"
        cell = EXAMPLE_TIKZ_INPUT

        res = ipy.run_cell_magic("tikz", line, cell)

        assert isinstance(res, SVG)
