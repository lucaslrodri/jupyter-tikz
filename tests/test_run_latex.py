from jupyter_tikz.jupyter_tikz import run_latex
import os
from IPython.display import SVG, Image

EXAMPLE_BAD_TIKZ = "HELLO WORLD"

EXAMPLE_RECTANGLE_TIKZ = r"""
\documentclass[tikz]{standalone}
\begin{document}
	\begin{tikzpicture}
		\draw[fill=blue] (0, 0) rectangle (1, 1);
	\end{tikzpicture}
\end{document}
"""


def test_run_latex_good_input():
    res = run_latex(EXAMPLE_RECTANGLE_TIKZ, rasterize=False)
    expected_res = '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="28.745" height="28.745" viewBox="0 0 28.745 28.745">\n<defs>\n<clipPath id="clip-0">\n<path clip-rule="nonzero" d="M 0 0 L 28.492188 0 L 28.492188 28.492188 L 0 28.492188 Z M 0 0 "/>\n</clipPath>\n</defs>\n<g clip-path="url(#clip-0)">\n<path fill-rule="nonzero" fill="rgb(0%, 0%, 100%)" fill-opacity="1" stroke-width="0.3985" stroke-linecap="butt" stroke-linejoin="miter" stroke="rgb(0%, 0%, 0%)" stroke-opacity="1" stroke-miterlimit="10" d="M -0.00195486 -0.00189963 L -0.00195486 28.345014 L 28.344959 28.345014 L 28.344959 -0.00189963 Z M -0.00195486 -0.00189963 " transform="matrix(0.991207, 0, 0, -0.991207, 0.19725, 28.294992)"/>\n</g>\n</svg>'

    assert res.data == expected_res


def test_run_latex_bad_input(capsys):
    res = run_latex(EXAMPLE_BAD_TIKZ, rasterize=False)
    _, err = capsys.readouterr()

    assert res is None
    assert "error" in err.lower()
    assert len(err.splitlines()) == 20


def test_run_latex_bad_input_full_err(capsys):
    res = run_latex(EXAMPLE_BAD_TIKZ, rasterize=False, full_err=True)
    _, err = capsys.readouterr()

    assert res is None
    assert "error" in err.lower()
    assert len(err.splitlines()) > 20


def test_run_latex_good_input_rasterize():
    res = run_latex(EXAMPLE_RECTANGLE_TIKZ, rasterize=True)

    assert isinstance(res, Image)


def test_run_latex_good_input_rasterize_dpi_1200():
    res = run_latex(EXAMPLE_RECTANGLE_TIKZ, rasterize=True, dpi=1200)

    assert isinstance(res, Image)


def test_run_latex_tex_program_lualatex():
    res = run_latex(EXAMPLE_RECTANGLE_TIKZ, rasterize=False)
    expected_res = '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="28.745" height="28.745" viewBox="0 0 28.745 28.745">\n<defs>\n<clipPath id="clip-0">\n<path clip-rule="nonzero" d="M 0 0 L 28.492188 0 L 28.492188 28.492188 L 0 28.492188 Z M 0 0 "/>\n</clipPath>\n</defs>\n<g clip-path="url(#clip-0)">\n<path fill-rule="nonzero" fill="rgb(0%, 0%, 100%)" fill-opacity="1" stroke-width="0.3985" stroke-linecap="butt" stroke-linejoin="miter" stroke="rgb(0%, 0%, 0%)" stroke-opacity="1" stroke-miterlimit="10" d="M -0.00195486 -0.00189963 L -0.00195486 28.345014 L 28.344959 28.345014 L 28.344959 -0.00189963 Z M -0.00195486 -0.00189963 " transform="matrix(0.991207, 0, 0, -0.991207, 0.19725, 28.294992)"/>\n</g>\n</svg>'

    assert isinstance(res, SVG)
    assert res.data == expected_res


# @pytest.mark.skip(reason="This test depends on the path of pdftocairo in the system")
def test_run_latex_with_custom_pdftocairo_path(monkeypatch):
    # IMPORTANT: Modify this path to the path of pdftocairo.exe in your system
    custom_pdftocairo_path = os.path.join(
        os.getenv("LOCALAPPDATA"), "Poppler", "Library", "bin", "pdftocairo.exe"
    )
    monkeypatch.setenv("JUPYTER_TIKZ_PDFTOCAIROPATH", custom_pdftocairo_path)

    res = run_latex(EXAMPLE_RECTANGLE_TIKZ, rasterize=False)
    expected_res = '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="28.745" height="28.745" viewBox="0 0 28.745 28.745">\n<defs>\n<clipPath id="clip-0">\n<path clip-rule="nonzero" d="M 0 0 L 28.492188 0 L 28.492188 28.492188 L 0 28.492188 Z M 0 0 "/>\n</clipPath>\n</defs>\n<g clip-path="url(#clip-0)">\n<path fill-rule="nonzero" fill="rgb(0%, 0%, 100%)" fill-opacity="1" stroke-width="0.3985" stroke-linecap="butt" stroke-linejoin="miter" stroke="rgb(0%, 0%, 0%)" stroke-opacity="1" stroke-miterlimit="10" d="M -0.00195486 -0.00189963 L -0.00195486 28.345014 L 28.344959 28.345014 L 28.344959 -0.00189963 Z M -0.00195486 -0.00189963 " transform="matrix(0.991207, 0, 0, -0.991207, 0.19725, 28.294992)"/>\n</g>\n</svg>'

    assert isinstance(res, SVG)
    assert res.data == expected_res
