import pytest

from jupyter_tikz.jupyter_tikz import _get_arg_params


@pytest.mark.parametrize(
    "arg,expected_args,expected_kwargs",
    [
        (
            "input-type",
            ("-as", "--input-type"),
            {
                "dest": "input_type",
                "default": "standalone-document",
                "help": "Type of the input. Possible values are: `full-document`, `standalone-document` and `tikzpicture`, e.g., `-as=full-document`. Defaults to `-as=standalone-document`.",
            },
        ),
        (
            "latex-preamble",
            ("-p", "--latex-preamble"),
            {
                "dest": "latex_preamble",
                "default": None,
                "help": 'LaTeX preamble to insert before the document, e.g., `-p="$preamble"`, with the preamble being an IPython variable.',
            },
        ),
        (
            "tex-packages",
            ("-t", "--tex-packages"),
            {
                "dest": "tex_packages",
                "default": None,
                "help": "Comma-separated list of TeX packages, e.g., `-t=amsfonts,amsmath`.",
            },
        ),
        (
            "no-tikz",
            ("-nt", "--no-tikz"),
            {
                "dest": "no_tikz",
                "action": "store_true",
                "default": False,
                "help": "Force to not import the TikZ package.",
            },
        ),
        (
            "tikz-libraries",
            ("-l", "--tikz-libraries"),
            {
                "dest": "tikz_libraries",
                "default": None,
                "help": "Comma-separated list of TikZ libraries, e.g., `-l=calc,arrows`.",
            },
        ),
        (
            "pgfplots-libraries",
            ("-lp", "--pgfplots-libraries"),
            {
                "dest": "pgfplots_libraries",
                "default": None,
                "help": "Comma-separated list of pgfplots libraries, e.g., `-pl=groupplots,external`.",
            },
        ),
        (
            "no-jinja",
            ("-nj", "--no-jinja"),
            {
                "dest": "no_jinja",
                "action": "store_true",
                "default": False,
                "help": "Disable Jinja2 rendering.",
            },
        ),
        (
            "print-jinja",
            ("-pj", "--print-jinja"),
            {
                "dest": "print_jinja",
                "action": "store_true",
                "default": False,
                "help": "Print the rendered Jinja2 template.",
            },
        ),
        (
            "print-tex",
            ("-pt", "--print-tex"),
            {
                "dest": "print_tex",
                "action": "store_true",
                "default": False,
                "help": "Print the full LaTeX document.",
            },
        ),
        (
            "scale",
            ("-sc", "--scale"),
            {
                "dest": "scale",
                "default": 1.0,
                "type": float,
                "help": "The scale factor to apply to the TikZ diagram, e.g., `-sc=0.5`. Defaults to `-sc=1.0`.",
            },
        ),
        (
            "rasterize",
            ("-r", "--rasterize"),
            {
                "dest": "rasterize",
                "action": "store_true",
                "default": False,
                "help": "Output a rasterized image (PNG) instead of SVG.",
            },
        ),
        (
            "dpi",
            ("-d", "--dpi"),
            {
                "dest": "dpi",
                "default": 96,
                "type": int,
                "help": "DPI to use when rasterizing the image, e.g., `--dpi=300`. Defaults to `-d=96`.",
            },
        ),
        (
            "full-err",
            ("-e", "--full-err"),
            {
                "dest": "full_err",
                "action": "store_true",
                "default": False,
                "help": "Print the full error message when an error occurs.",
            },
        ),
    ],
)
def test_get_arg_params(arg, expected_args, expected_kwargs):
    # Act
    args, kwargs = _get_arg_params(arg)

    # Assert
    assert args == expected_args
    assert kwargs == expected_kwargs
