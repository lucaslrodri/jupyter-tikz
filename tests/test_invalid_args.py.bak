from IPython.testing.globalipapp import get_ipython

EXAMPLE_RECTANGLE_TIKZ = r"""
\documentclass[tikz]{standalone}
\begin{document}
	\begin{tikzpicture}
		\draw[fill=blue] (0, 0) rectangle (1, 1);
	\end{tikzpicture}
\end{document}
"""

ipy = get_ipython()
ipy.run_line_magic("load_ext", "jupyter_tikz")


def test_magic_show_help_command_with_empty_input_line(capsys):
    line = ""

    res = ipy.run_line_magic("tikz", line)
    _, err = capsys.readouterr()

    assert res is None
    assert err.startswith('Use "%tikz?" for help\n')


def test_magic_no_simultaneous_implicit_pic_and_full_document(capsys):
    line = "-f -i"
    cell = EXAMPLE_RECTANGLE_TIKZ

    res = ipy.run_cell_magic("tikz", line, cell)
    _, err = capsys.readouterr()

    assert res is None
    assert err.startswith("Can't use --full-document and --implicit-pic together")


def test_magic_cannot_use_packages_or_libraries_with_preamble_at_the_same_time(capsys):
    line = "-t amsmath -p '\\usepackage{amssymb}'"
    cell = EXAMPLE_RECTANGLE_TIKZ

    res = ipy.run_cell_magic("tikz", line, cell)
    _, err = capsys.readouterr()

    assert res is None
    assert err.startswith(
        "Packages and libraries should be passed in the preamble or as arguments, not both"
    )
