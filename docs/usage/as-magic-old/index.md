## Basic usage

To use the Jupyter-TikZ package, you'll need to follow these steps:

1. Install the dependences:

Before proceding with the installation of the package, you need to ensure that the dependencies LaTeX and Poppler are installed. For more information visit [installation guide](../../installation.md).

2. Install the Package:

Once the dependencies are installed, you can proceed with the installation of the jupyter-tikz package using pip:

```shell
pip install jupyter_tikz
```

3. Load the Extension in a Jupyter Notebook:

Next, you need to load the `jupyter_tikz` extension in your Jupyter Notebook. You can do this by running the following code cell:

```python
%load_ext jupyter_tikz
```

Create a simple `tikzpicture`:

```latex
%%tikz
\begin{tikzpicture}
    \draw[help lines] grid (5, 5);
    \draw[fill=black] (1, 1) rectangle (2, 2);
    \draw[fill=black] (2, 1) rectangle (3, 2);
    \draw[fill=black] (3, 1) rectangle (4, 2);
    \draw[fill=black] (3, 2) rectangle (4, 3);
    \draw[fill=black] (2, 3) rectangle (3, 4);
\end{tikzpicture}
```
<div class="result" markdown>
![Conway black](../assets/tikz/conway_black.svg)
</div>

Finally, if you forget the usage, as for help by typing `%tikz?`, or visit **additional options** reference [here](../arguments.md).

```python
%tikz?
```
<div class="result" style="padding-right: 0;">
<div class="log-output">
<pre>
%tikz [-as INPUT_TYPE] [-i] [-f] [-p LATEX_PREAMBLE] [-t TEX_PACKAGES]
        [-nt] [-l TIKZ_LIBRARIES] [-lp PGFPLOTS_LIBRARIES] [-j] [-pj]
        [-pt] [-sc SCALE] [-r] [-d DPI] [-e] [-tp TEX_PROGRAM]
        [-ta TEX_ARGS] [-nc] [-s SAVE_TEX] [-S SAVE_IMAGE] [-sv SAVE_VAR]
        [--as-jinja]
        [code]

positional arguments:
code                  the variable in IPython with the Tex/TikZ code

options:
-as INPUT_TYPE, --input-type INPUT_TYPE
                        Type of the input. Possible values are: \`full-
                        document\`, \`standalone-document\` and \`tikzpicture\`,
                        e.g., \`-as=full-document\`. Defaults to
                        \`-as=standalone-document\`.
-i, --implicit-pic    Alias for \`-as=tikzpicture\`.
-f, --full-document   Alias for \`-as=full-document\`.
-p LATEX_PREAMBLE, --latex-preamble LATEX_PREAMBLE
                        LaTeX preamble to insert before the document, e.g.,
                        \`-p="$preamble"\`, with the preamble being an IPython
                        variable.
-t TEX_PACKAGES, --tex-packages TEX_PACKAGES
                        Comma-separated list of TeX packages, e.g.,
                        \`-t=amsfonts,amsmath\`.
-nt, --no-tikz        Force to not import the TikZ package.
-l TIKZ_LIBRARIES, --tikz-libraries TIKZ_LIBRARIES
                        Comma-separated list of TikZ libraries, e.g.,
                        \`-l=calc,arrows\`.
-lp PGFPLOTS_LIBRARIES, --pgfplots-libraries PGFPLOTS_LIBRARIES
                        Comma-separated list of pgfplots libraries, e.g.,
                        \`-pl=groupplots,external\`.
-j, --use-jinja       Render the code using Jinja2.
-pj, --print-jinja    Print the rendered Jinja2 template.
-pt, --print-tex      Print the full LaTeX document.
-sc SCALE, --scale SCALE
                        The scale factor to apply to the TikZ diagram, e.g.,
                        \`-sc=0.5\`. Defaults to \`-sc=1.0\`.
-r, --rasterize       Output a rasterized image (PNG) instead of SVG.
-d DPI, --dpi DPI     DPI to use when rasterizing the image, e.g.,
                        \`--dpi=300\`. Defaults to \`-d=96\`.
-e, --full-err        Print the full error message when an error occurs.
-tp TEX_PROGRAM, --tex-program TEX_PROGRAM
                        TeX program to use for compilation, e.g.,
                        \`-tp=xelatex\` or \`-tp=lualatex\`. Defaults to
                        \`-tp=pdflatex\`.
-ta TEX_ARGS, --tex-args TEX_ARGS
                        Arguments to pass to the TeX program, e.g.,
                        \`-ta="$tex_args_ipython_variable"\`.
-nc, --no-compile     Do not compile the TeX code.
-s SAVE_TEX, --save-text SAVE_TEX
                        Save the TikZ or LaTeX code to file, e.g., \`-s
                        filename.tikz\`.
-S SAVE_IMAGE, --save-image SAVE_IMAGE
                        Save the output image to file, e.g., \`-S
                        filename.png\`.
-sv SAVE_VAR, --save-var SAVE_VAR
                        Save the TikZ or LaTeX code to an IPython variable,
                        e.g., \`-sv my_var\`.
--as-jinja            Deprecated. Use \`--use-jinja\` instead.
</pre>
</div>
</div>

This is the basic usage:



Additionally, you always can view **additional options** reference [here](../arguments.md).