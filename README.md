[![PyPI version](https://badge.fury.io/py/jupyter-tikz.svg)](https://badge.fury.io/py/jupyter-tikz)

Jupyter TikZ is an IPython Magic for rendering TeX/TikZ outputs in Jupyter Notebooks.

# Installation

```shell
pip install jupyter-tikz
```

## Dependencies

Before installation, you should verify the dependencies.

### LaTeX

LaTeX must be installed using one of the following distributions:

- [TeX Live](https://tug.org/texlive/) (All Platforms)
- [MikTeX](https://miktex.org/) (Windows)
- [MacTeX](https://www.tug.org/mactex/) (Mac)

### Poppler

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

### Jinja2 (Optional)

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

Or use it as line magic, the TeX/TikZ code is passed as an IPython string variable:

```python
%tikz "$ipython_string_variable_with_code"
```

Furthermore, additional arguments can be passed to the magic command:

```latex
 %%tikz -i --rasterize --dpi=1200 -l arrows,automata
\draw (0,0) rectangle (1,1);
\filldraw (0.5,0.5) circle (.1);
```

# Getting Started Notebook

A complete guide is available in the [Getting Started Notebook](https://github.com/lucaslrodri/jupyter-tikz/blob/main/GettingStarted.ipynb).

# Additional Arguments

All additional arguments are listed below:

- `-p` or `--latex_preamble` (`str`): LaTeX preamble to insert before the document, e.g., `-p "$preamble"`, with the preamble being an IPython variable.
- `-t` or `--tex-packages` (`str`): Comma-separated list of TeX packages, e.g., `-t amsfonts,amsmath`.
- `-nt` or `--no-tikz`: Force to not import the TikZ package.
- `-l` or `--tikz-libraries` (`str`): Comma-separated list of TikZ libraries, e.g., `-l arrows,automata`.
- `-lp` or `--pgfplots-libraries` (`str`): Comma-separated list of PGFPlots libraries, e.g., `-lp groupplots,external`.
- `-i` or `--implicit-pic`: Implicitly wrap the code in a standalone document with a `tikzpicture` environment.
- `-f` or `--full-document`: Use a full LaTeX document as input.
- `-j` or  `--as-jinja`: Render the input as a Jinja2 template.
- `-pj` or `--print-jinja`: Print the rendered Jinja2 template.
- `-sc` or `--scale` (`float` or `int`): The scale factor to apply to the TikZ diagram. Default is 1.
- `-r` or `--rasterize`: Output a rasterized image (PNG) instead of SVG.
- `-d` or `--dpi` (`int`): DPI of the rasterized output image. Default is 96.
- `-e` or `--full-err`: Show the full error message.
- `-tp` or `--tex-program`: TeX program to use for rendering, e.g., `-tp lualatex`.
- `-ta` or `--tex-args` (`str`): Additional arguments to pass to the TeX program, e.g., `-ta "$tex_args_ipython_variable"`.
- `-nc` or `--no-compile`: Do not compile the LaTeX code.
- `-s` or `--save-tex` (`str`): Save the TikZ or TeX code to file, e.g., `-s filename.tikz`. Default is None.
- `-S` or `--save-image` (`str`): Save the output image to file, e.g., `-S filename.svg`. Default is None.
- `-sv` or `--save-var` (`str`): Save the TikZ or TeX code to an IPython variable, e.g., `-sv varname`. Default is None.

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

For more information refer to this [link](https://discourse.jupyter.org/t/getting-syntax-highlighting-to-work-for-custom-cell-magic/11734/9).

# Contribute

Contributions are welcome from everyone! Whether you're reporting bugs, submitting feedback, or actively improving the codebase, your involvement is valuable. Here’s how you can contribute:

1. If you encounter any issues or have suggestions for improvements, please report them using the [issues page](https://github.com/lucaslrodri/jupyter-tikz/issues).
2. If you're interested in developing the software further, please refer to [contributing guide](./DEVELOPMENT.md). 

# Thanks

I had been using [ITikZ](https://github.com/jbn/itikz) for years. However, it doesn't update often and relies on the outdated `pdf2svg` to convert PDFs to images, which causes problems in Windows environments. Inspired by ITikZ and [TikZ Magic](https://github.com/mkrphys/ipython-tikzmagic), I decided to create my own package, adding new features such as the ability to work with preambles. I also switched from `pdf2svg` to Poppler, which works perfectly in Windows.

# License

Distributed under the terms of the [MIT](./LICENSE) license, Jupyter TikZ is free and open source software.

