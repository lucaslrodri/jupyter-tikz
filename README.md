<p align="center">
  <a href="https://jupyter-tikz.readthedocs.io/en/stable/"
    ><img
      alt="Logo of Jupyter-TikZ"
      src="https://jupyter-tikz.readthedocs.io/en/stable/assets/logo_wide.svg"
      style="width: calc(100% - 2rem); max-width: 800px; max-height: 10rem"
  /></a>
</p>

<p align="center">
  <em>IPython Magics for rendering TeX/TikZ in Jupyter Notebooks</em>
</p>

<p align="center">
  <a href="https://jupyter-tikz.readthedocs.io/en/stable/"
    ><img
      alt="Read the Docs"
      src="https://img.shields.io/readthedocs/jupyter-tikz"
  /></a> <a href="https://pypi.org/project/jupyter-tikz/"
    ><img
      src="https://img.shields.io/pypi/v/jupyter_tikz?color=4cc71e"
      alt="PyPI - Version"
  /></a> <a href="https://pepy.tech/project/jupyter-tikz"
    ><img
      src="https://static.pepy.tech/badge/jupyter-tikz"
      alt="Pypi - Downloads"
  /></a> <a href="https://codecov.io/github/lucaslrodri/jupyter-tikz">
    <img
      src="https://codecov.io/github/lucaslrodri/jupyter-tikz/graph/badge.svg?token=6QVANQMJYC"
  /></a> <a
    href="https://raw.githubusercontent.com/lucaslrodri/jupyter-tikz/main/LICENSE"
    ><img src="https://img.shields.io/pypi/l/jupyter_tikz" alt="License"
  /></a>
</p>

<p align="center">
<a 
    href="https://jupyter-tikz.readthedocs.io/"
>Documentation</a> | <a
    href="https://github.com/lucaslrodri/jupyter-tikz/blob/main/notebooks/GettingStarted.ipynb"
>Getting Started notebook</a>
</p>

# Installation

## Prerequisites

Jupyter-TikZ is a Python (3.10+) and IPython Magics library. However, in order for Jupyter-TikZ to work properly, some non-Python dependencies need to be installed first:

- LaTeX
- Poppler

### LaTeX

LaTeX must be installed using one of the following distributions:

- [TeX Live](https://tug.org/texlive/) (All Platforms)
- [MikTeX](https://miktex.org/) (Windows)
- [MacTeX](https://www.tug.org/mactex/) (Mac)

You can test if a LaTeX distribution is installed by using the following command:

```latex
pdflatex --version
```


### Poppler

This application requires Poppler's `pdftocairo`. You must install it beforehand.

#### Conda - Platform Independent

```shell
conda install -c conda-forge poppler
```

#### Windows

Download Poppler for Windows [here](https://github.com/oschwartz10612/poppler-windows/releases/). You must add the `bin` folder to your [PATH](https://www.c-sharpcorner.com/article/how-to-addedit-path-environment-variable-in-windows-11/).

#### Linux

Most distributions come with `pdftocairo`. If it is not installed, refer to your package manager to install `poppler-utils`.

#### Mac

Install using `brew`:

```shell
brew install poppler
```

#### Checking the Installation

Finally, you can check if the `pdftocairo` utility is installed by using the following command in your terminal:

```shell
pdftocairo -v
```



#### Using custom pdftocairo path

Alternatively, if you are facing issues, you can configure the `pdftocairo` location (exclusive for use in `jupyter_tikz`) by setting the environment variable `JUPYTER_TIKZ_PDFTOCAIROPATH`:


```python
import os
custom_pdftocairo_path = os.path.join(
  os.getenv("LOCALAPPDATA"), "Poppler", "Library", "bin", "pdftocairo.exe"
)
os.environ["JUPYTER_TIKZ_PDFTOCAIROPATH"] = custom_pdftocairo_path
```


### Jinja2 (Optional)

Jinja2 is only necessary if you plan to use [Jinja2 templates](https://jinja.palletsprojects.com/en/latest/templates/). To install it, use:

```shell
pip install jinja2
```

## Install Jupyter TikZ

You can install `jupyter-tikz` by using the following command in your terminal:

```shell
pip install jupyter-tikz
```


## Adding TikZ Syntax highlight

If you are using Jupyter Lab 4. You can add LaTeX highlight to `%%tikz` magic cells by using [JupyterLab-lsp](https://jupyterlab-lsp.readthedocs.io/en/latest/Installation.html) and editing [this part of the code in JupyterLab-lsp](https://github.com/jupyter-lsp/jupyterlab-lsp/blob/b159ae2736b26463d8cc8f0ef78f4b2ce9913370/packages/jupyterlab-lsp/src/transclusions/ipython/extractors.ts#L68-L74) in the file `extractor.ts`:

```ts
new RegExpForeignCodeExtractor({
  language: 'latex',
  pattern: '^%%(latex|tikz)( .*?)?\n([^]*)', // Add tikz support to this line
  foreignCaptureGroups: [3],
  isStandalone: false,
  fileExtension: 'tex'
}),
```

Now, you will have LaTeX syntax code highlighting for `%%tikz` magic cells, as demonstrated below:

![Using Jupyter TikZ with LaTeX syntax highlight](https://jupyter-tikz.readthedocs.io/en/stable/assets/highlight_cell_tikz.png)

For more information refer to this [link](https://discourse.jupyter.org/t/getting-syntax-highlighting-to-work-for-custom-cell-magic/11734/9).

# Basic usage

To begin, load the `jupyter_tikz` extension:

```
%load_ext jupyter_tikz
```

Use it as cell magic, it executes the TeX/TikZ code within the cell:

```latex
%%tikz
\begin{tikzpicture}
    \draw[help lines] grid (5, 5);
    \draw[fill=black!10] (1, 1) rectangle (2, 2);
    \draw[fill=black!10] (2, 1) rectangle (3, 2);
    \draw[fill=black!10] (3, 1) rectangle (4, 2);
    \draw[fill=black!10] (3, 2) rectangle (4, 3);
    \draw[fill=black!10] (2, 3) rectangle (3, 4);
\end{tikzpicture}
```
![Conway example](https://jupyter-tikz.readthedocs.io/en/stable/assets/conway.svg)

Or use it as line magic, where the TeX/TikZ code is passed as an IPython string variable:

```python
%tikz "$ipython_string_variable_with_code"
```

Additional options can be passed to the magic command:

```latex
%%tikz -i -t=pgfplots -nt -S=docs/assets/quadratic -r --dpi=150
\begin{axis}[
  xlabel=$x$,
  ylabel={$f(x) = x^2 + 4$}
]
    \addplot [red] {x^2 + 4};
\end{axis}
```
![Quadratic formula](https://jupyter-tikz.readthedocs.io/en/stable/assets/quadratic.png)

Going further, it is also possible to use it as a Python package:

```python
from jupyter_tikz import TexFragment

tikz_code = tex_template_code = r"""\begin{tikzpicture}
    \draw[help lines] grid (5, 5);
     \filldraw [color=orange, opacity=0.3] (2.5,2.5) circle (1.5);
\end{tikzpicture}"""

tikz = TexFragment(tikz_code)  # Create the tex template object

tikz.run_latex()  # Run LaTeX and shows the output
```
![Orange dot in a grid](https://jupyter-tikz.readthedocs.io/en/stable/assets/dot_in_grid.svg)

# Additional options

All additional options are listed below:


| Argument | Description |
| -------- | ----------- |
| `-as=<str>`<br>`--input-type=<str>` | Type of the input. Possible values are: `full-document`, `standalone-document` and `tikzpicture`.<br>&nbsp;&nbsp;&nbsp;&nbsp;*Example:* `-as=full-document`.<br>&nbsp;&nbsp;&nbsp;&nbsp;*Defaults* to `-as=standalone-document`. |
| `-i`<br>`--implicit-pic` | Alias for `-as=tikzpicture`. |
| `-f`<br>`--full-document` | Alias for `-as=full-document`. |
| `-p=<str>`<br>`--latex-preamble=<str>` | LaTeX preamble to insert before the document.<br>&nbsp;&nbsp;&nbsp;&nbsp;*Example:* `-p="$preamble"`, with the preamble being an IPython variable.<br>&nbsp;&nbsp;&nbsp;&nbsp;*Defaults* to None. |
| `-t=<str>`<br>`--tex-packages=<str>` | Comma-separated list of TeX packages.<br>&nbsp;&nbsp;&nbsp;&nbsp;*Example:* `-t=amsfonts,amsmath`.<br>&nbsp;&nbsp;&nbsp;&nbsp;*Defaults* to None. |
| `-nt`<br>`--no-tikz` | Force to not import the TikZ package. |
| `-l=<str>`<br>`--tikz-libraries=<str>` | Comma-separated list of TikZ libraries.<br>&nbsp;&nbsp;&nbsp;&nbsp;*Example:* `-l=calc,arrows`.<br>&nbsp;&nbsp;&nbsp;&nbsp;*Defaults* to None. |
| `-lp=<str>`<br>`--pgfplots-libraries=<str>` | Comma-separated list of pgfplots libraries.<br>&nbsp;&nbsp;&nbsp;&nbsp;*Example:* `-pl=groupplots,external`.<br>&nbsp;&nbsp;&nbsp;&nbsp;*Defaults* to None. |
| `-j`<br>`--use-jinja` | Render the code using Jinja2. |
| `-pj`<br>`--print-jinja` | Print the rendered Jinja2 template. |
| `-pt`<br>`--print-tex` | Print the full LaTeX document. |
| `-sc=<float>`<br>`--scale=<float>` | The scale factor to apply to the TikZ diagram.<br>&nbsp;&nbsp;&nbsp;&nbsp;*Example:* `-sc=0.5`.<br>&nbsp;&nbsp;&nbsp;&nbsp;*Defaults* to `-sc=1.0`. |
| `-r`<br>`--rasterize` | Output a rasterized image (PNG) instead of SVG. |
| `-d=<int>`<br>`--dpi=<int>` | DPI to use when rasterizing the image.<br>&nbsp;&nbsp;&nbsp;&nbsp;*Example:* `--dpi=300`.<br>&nbsp;&nbsp;&nbsp;&nbsp;*Defaults* to `-d=96`. |
| `-g`<br>`--gray` | Set grayscale to the rasterized image. |
| `-e`<br>`--full-err` | Print the full error message when an error occurs. |
| `-k`<br>`--keep-temp` | Keep temporary files. |
| `-tp=<str>`<br>`--tex-program=<str>` | TeX program to use for compilation.<br>&nbsp;&nbsp;&nbsp;&nbsp;*Example:* `-tp=xelatex` or `-tp=lualatex`.<br>&nbsp;&nbsp;&nbsp;&nbsp;*Defaults* to `-tp=pdflatex`. |
| `-ta=<str>`<br>`--tex-args=<str>` | Arguments to pass to the TeX program.<br>&nbsp;&nbsp;&nbsp;&nbsp;*Example:* `-ta="$tex_args_ipython_variable"`.<br>&nbsp;&nbsp;&nbsp;&nbsp;*Defaults* to None. |
| `-nc`<br>`--no-compile` | Do not compile the TeX code. |
| `-s=<str>`<br>`--save-tikz=<str>` | Save the TikZ code to file.<br>&nbsp;&nbsp;&nbsp;&nbsp;*Example:* `-s filename.tikz`.<br>&nbsp;&nbsp;&nbsp;&nbsp;*Defaults* to None. |
| `-st=<str>`<br>`--save-tex=<str>` | Save full LaTeX code to file.<br>&nbsp;&nbsp;&nbsp;&nbsp;*Example:* `-st filename.tex`.<br>&nbsp;&nbsp;&nbsp;&nbsp;*Defaults* to None. |
| `-sp=<str>`<br>`--save-pdf=<str>` | Save PDF file.<br>&nbsp;&nbsp;&nbsp;&nbsp;*Example:* `-sp filename.pdf`.<br>&nbsp;&nbsp;&nbsp;&nbsp;*Defaults* to None. |
| `-S=<str>`<br>`--save-image=<str>` | Save the output image to file.<br>&nbsp;&nbsp;&nbsp;&nbsp;*Example:* `-S filename.png`.<br>&nbsp;&nbsp;&nbsp;&nbsp;*Defaults* to None. |
| `-sv=<str>`<br>`--save-var=<str>` | Save the TikZ or LaTeX code to an IPython variable.<br>&nbsp;&nbsp;&nbsp;&nbsp;*Example:* `-sv my_var`.<br>&nbsp;&nbsp;&nbsp;&nbsp;*Defaults* to None. |


# Contribute

Contributions are welcome from everyone! Whether you're reporting bugs, submitting feedback, or actively improving the codebase, your involvement is valuable. Here's how you can contribute:

<ol>
<li>If you encounter any issues or have suggestions for improvements, please report them using the <a href="https://github.com/lucaslrodri/jupyter-tikz/issues">issues page</a>.</li>
<li>If you're interested in developing the software further, please refer to <a href="about/development/">development guide</a>.</li>
</ol>

# Changelog

All notable changes to this project are presented below.

## v0.4.0

**🚀 Features**

- Added support for PGFPlots with external data files.
- Introduced a new flag (`-k`) to retain LaTeX temporary files.
- Added support for grayscale output in rasterized mode.
- Introduced new flags `--save-tikz` and `--save-pdf` to save the TikZ and PDF files respectively; `--save-tex` now explicitly saves the full LaTeX document.

**🚨 Breaking Changes**

- Modified the save functionality: Options must now be passed in `TexDocument.run_latex(...)` as `TexDocument.save()` is no longer used.
- LaTeX rendering is now performed in the current folder, moving away from the use of a temporary directory (`tempdir`). This change facilitates access to external files for PGFPlots.

## v0.3.2

**🐞 Bug Fixes**

- Improved documentation visibility on mobile devices.

## v0.3.1

**🐞 Bug Fixes**

- Fixed DOCs links.

## v0.3.0

**🚀 Features**

- Web documentation.
- Flag (`--print-tex`) to print the full LaTeX document.
- UTF-8 support.
- Added support for Python 3.10.

**🚨 Breaking Changes**

- Replaced `--full-document` and `--implicit-pic` with `--input-type=<str>`. `-f` and `-i` still working as aliases.
- Changed the `--as-jinja` flag to `--use-jinja`.
- Reworked the API to an object-oriented approach.

## v0.2.1

**🐞 Bug Fixes**

- Minor adjustments in the README and Getting Started Notebook.

## v0.2.0

**🚀 Features**

- Option to save output code to an IPython variable (`-sv=<var_name>`).
- Flag (`--no-compile`) to prevent LaTeX compilation and image rendering.
- Support for LaTeX `\input{...}` commands.

## v0.1.1

**🐞 Bug Fixes**

- Minor fixes in README.

**🚀 Features**

- Added PyPI badge.

## v0.1.0

- First version released on PyPI.

# Thanks

I had been using [ITikZ](https://github.com/jbn/itikz) for years. However, it doesn't update often and relies on the outdated `pdf2svg` to convert PDFs to images, which causes problems in Windows environments. Inspired by ITikZ and [IPython TikZ Magic](https://github.com/mkrphys/ipython-tikzmagic), I decided to create my own package, adding new features such as the ability to work with preambles and save the LaTeX result to IPython variables. I also switched from `pdf2svg` to Poppler, which works perfectly in Windows.

# License

Copyright 2024 &copy; [Lucas Lima Rodrigues](https://github.com/lucaslrodri).

Distributed under the terms of the [MIT License](https://github.com/lucaslrodri/jupyter-tikz/blob/main/LICENSE), Jupyter-TikZ is free and open-source software.