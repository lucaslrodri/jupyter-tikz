<p align="center">
  <a
    ><img
      alt="Logo of Jupyter-TikZ"
      src="docs/assets/logo_wide.svg"
      style="width: calc(100% - 2rem); max-width: 800px; max-height: 10rem"
  /></a>
</p>

<p align="center">
  <em>IPython Magics for rendering TeX/TikZ in Jupyter Notebooks</em>
</p>

<p align="center">
  <a href="https://pypi.org/project/jupyter-tikz/" target="_blank"
    ><img
      src="https://img.shields.io/pypi/v/jupyter_tikz?color=4cc71e"
      alt="PyPI - Version"
  /></a>
  <a href="https://pepy.tech/project/jupyter-tikz" target="_blank"
    ><img
      src="https://static.pepy.tech/badge/jupyter-tikz"
      alt="Pypi - Downloads"
  /></a>
  <a
    href="https://raw.githubusercontent.com/lucaslrodri/jupyter-tikz/main/LICENSE"
    target="_blank"
    ><img src="https://img.shields.io/pypi/l/jupyter_tikz" alt="License"
  /></a>
</p>


# Demonstration notebook

A complete guide is available in the [Getting Started Notebook](https://github.com/lucaslrodri/jupyter-tikz/blob/main/GettingStarted.ipynb).

# Installation

```shell
pip install jupyter-tikz
```

# Dependencies

Before installation, you should verify the dependencies.

## LaTeX

LaTeX must be installed using one of the following distributions:

- [TeX Live](https://tug.org/texlive/) (All Platforms)
- [MikTeX](https://miktex.org/) (Windows)
- [MacTeX](https://www.tug.org/mactex/) (Mac)

## Poppler

This application requires Poppler’s `pdftocairo`. You must install it beforehand.

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

## Jinja2 (Optional)

Jinja2 is only necessary if you plan to use [Jinja2 templates](http://jinja.pocoo.org/docs/latest/templates/). To install it, use:

```shell
pip install jinja2
```

# Basic Usage

To begin, load the `jupyter_tikz` extension:

```
%load_ext jupyter_tikz
```

Use it as cell magic, it executes the TeX/TikZ code within the cell:

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

which produces:

![Conway example](https://raw.githubusercontent.com/lucaslrodri/jupyter-tikz/main/docs/assets/conway.svg)

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

which produces:

![Quadratic formula](https://raw.githubusercontent.com/lucaslrodri/jupyter-tikz/main/docs/assets/quadratic.png)

Don't forget visit the [Documentation]() and [Getting Started Notebook](https://github.com/lucaslrodri/jupyter-tikz/blob/main/GettingStarted.ipynb) to learn more.

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
| `-g`<br>`--gray` | Set grayscale to a rasterized image. |
| `-e`<br>`--full-err` | Print the full error message when an error occurs. |
| `-k`<br>`--keep-temp` | Keep temporary LaTeX files. |
| `-tp=<str>`<br>`--tex-program=<str>` | TeX program to use for compilation.<br>&nbsp;&nbsp;&nbsp;&nbsp;*Example:* `-tp=xelatex` or `-tp=lualatex`.<br>&nbsp;&nbsp;&nbsp;&nbsp;*Defaults* to `-tp=pdflatex`. |
| `-ta=<str>`<br>`--tex-args=<str>` | Arguments to pass to the TeX program.<br>&nbsp;&nbsp;&nbsp;&nbsp;*Example:* `-ta="$tex_args_ipython_variable"`.<br>&nbsp;&nbsp;&nbsp;&nbsp;*Defaults* to None. |
| `-nc`<br>`--no-compile` | Do not compile the TeX code. |
| `-s=<str>`<br>`--save-tikz=<str>` | Save the TikZ code to file.<br>&nbsp;&nbsp;&nbsp;&nbsp;*Example:* `-s filename.tikz`.<br>&nbsp;&nbsp;&nbsp;&nbsp;*Defaults* to None. |
| `-st=<str>`<br>`--save-tex=<str>` | Save full LaTeX code to file.<br>&nbsp;&nbsp;&nbsp;&nbsp;*Example:* `-st filename.tex`.<br>&nbsp;&nbsp;&nbsp;&nbsp;*Defaults* to None. |
| `-sp=<str>`<br>`--save-pdf=<str>` | Save PDF file.<br>&nbsp;&nbsp;&nbsp;&nbsp;*Example:* `-sp filename.pdf`.<br>&nbsp;&nbsp;&nbsp;&nbsp;*Defaults* to None. |
| `-S=<str>`<br>`--save-image=<str>` | Save the output image to file.<br>&nbsp;&nbsp;&nbsp;&nbsp;*Example:* `-S filename.svg` or `-S filename.png`.<br>&nbsp;&nbsp;&nbsp;&nbsp;*Defaults* to None. |
| `-sv=<str>`<br>`--save-var=<str>` | Save cell content (TikZ or LaTeX code) to an IPython variable.<br>&nbsp;&nbsp;&nbsp;&nbsp;*Example:* `-sv my_var`.<br>&nbsp;&nbsp;&nbsp;&nbsp;*Defaults* to None. |

# Adding TikZ Syntax highlight

If you are using Jupyter Lab 4. You can add LaTeX highlight by using [JupyterLab-lsp](https://jupyterlab-lsp.readthedocs.io/en/latest/Installation.html) and editing [this part of the code](https://github.com/jupyter-lsp/jupyterlab-lsp/blob/b159ae2736b26463d8cc8f0ef78f4b2ce9913370/packages/jupyterlab-lsp/src/transclusions/ipython/extractors.ts#L68-L74) in the file `extractor.ts`:

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

![Using Jupyter TikZ with LaTeX syntax highlight](https://raw.githubusercontent.com/lucaslrodri/jupyter-tikz/main/docs/assets/highlight_cell_tikz.png)

For more information refer to this [link](https://discourse.jupyter.org/t/getting-syntax-highlighting-to-work-for-custom-cell-magic/11734/9).

# Contribute

Contributions are welcome from everyone! Whether you're reporting bugs, submitting feedback, or actively improving the codebase, your involvement is valuable. Here’s how you can contribute:

1. If you encounter any issues or have suggestions for improvements, please report them using the [issues page](https://github.com/lucaslrodri/jupyter-tikz/issues).
2. If you're interested in developing the software further, please refer to [contributing guide](./DEVELOPMENT.md). 

# Thanks

I had been using [ITikZ](https://github.com/jbn/itikz) for years. However, it doesn't update often and relies on the outdated `pdf2svg` to convert PDFs to images, which causes problems in Windows environments. Inspired by ITikZ and [TikZ Magic](https://github.com/mkrphys/ipython-tikzmagic), I decided to create my own package, adding new features such as the ability to work with preambles. I also switched from `pdf2svg` to Poppler, which works perfectly in Windows.

# License

© Copyright 2024 [Lucas Lima Rodrigues](https://github.com/lucaslrodri).

Distributed under the terms of the [MIT License](https://raw.githubusercontent.com/lucaslrodri/jupyter-tikz/main/LICENSE), `jupyter-tikz` is free and open-source software.
