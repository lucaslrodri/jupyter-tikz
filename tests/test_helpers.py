import pytest
from jupyter_tikz.jupyter_tikz import _get_arg_help


@pytest.mark.parametrize(
    "arg,expected",
    [
        (
            "input-type",
            "Type of the input. Possible values are: `full-document`, `standalone-document` and `tikzpicture`, e.g., `-as=full-document`. Defaults to `standalone`.",
        ),
        (
            "latex-preamble",
            'LaTeX preamble to insert before the document, e.g., `-p="$preamble"`, with the preamble being an IPython variable.',
        ),
        (
            "tex-packages",
            "Comma-separated list of TeX packages, e.g., `-t=amsfonts,amsmath`.",
        ),
        ("no-tikz", "Force to not import the TikZ package."),
        (
            "tikz-libraries",
            "Comma-separated list of TikZ libraries, e.g., `-l=calc,arrows`.",
        ),
        (
            "pgfplots-libraries",
            "Comma-separated list of pgfplots libraries, e.g., `-pl=groupplots,external`.",
        ),
        ("use-jinja", "Render the code using Jinja2."),
        ("print-jinja", "Print the rendered Jinja2 template."),
        ("print-tex", "Print the full LaTeX document."),
        (
            "scale",
            "The scale factor to apply to the TikZ diagram, e.g., `-sc=0.5`. Defaults to `1.0`.",
        ),
        ("rasterize", "Output a rasterized image (PNG) instead of SVG."),
        (
            "dpi",
            "DPI to use when rasterizing the image, e.g., `-d=300`. Defaults to `96`.",
        ),
        ("full-err", "Print the full error message when an error occurs."),
        (
            "tex-program",
            "TeX program to use for compilation, e.g., `-tp=xelatex` or `-tp=lualatex`. Defaults to `pdflatex`.",
        ),
        (
            "tex-args",
            'Arguments to pass to the TeX program, e.g., `-ta="$tex_args_ipython_variable"`.',
        ),
        ("no-compile", "Do not compile the TeX code."),
        ("save-text", "Save the TikZ or LaTeX code to file, e.g., `-s filename.tikz`."),
        ("save-image", "Save the output image to file, e.g., `-S filename.png`."),
        (
            "save-var",
            "Save the TikZ or LaTeX code to an IPython variable, e.g., `-sv my_var`.",
        ),
    ],
)
def test_get_arg_help(arg, expected):
    # Act
    res = _get_arg_help(arg)

    # Assert
    assert res == expected
