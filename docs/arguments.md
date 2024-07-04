# Additional arguments

All Jupyter-TikZ IPython Magics additional options are listed below:

- `-as=<str>` or `-input-type=<str>`: 
        Type of the input. 
        Possible values are: `full-document`, `standalone-document`, `tikzpicture`.
        e.g., `-as=full-document`.
        Defaults to `standalone-document`.
    
- `-p=<str>` or `--latex_preamble=<str>`:
         LaTeX preamble to insert before the document.
         e.g., `-p="$preamble"`, with the preamble being an IPython variable.
        Defaults to None.
     
- `-t=<str>` or `--tex-packages=<str>`:
        Comma-separated list of TeX packages.
        e.g., `-t=amsfonts,amsmath`.
        Defaults to None.
    
- `-nt` or `--no-tikz`:
        Force to not import the TikZ package.
    
- `-l=<str>` or `--tikz-libraries=<str>`:
        Comma-separated list of TikZ libraries.
        e.g., `-l=arrows,automata`.
        Defaults to None.
    
- `-lp=<str>` or `--pgfplots-libraries=<str>`:
        Comma-separated list of PGFPlots libraries.
        e.g., `-lp groupplots,external`.
        Defaults to None.
    
- `-j` or  `--use-jinja`:
        Render the input as a Jinja2 template.
    
- `-pj` or `--print-jinja`:
        Print the rendered Jinja2 template.
    
- `-pt` or `--print-tex`:
        Print full LaTeX document.
    
- `-sc=<float | int>` or `--scale=<float | int>`:
        The scale factor to apply to the TikZ diagram.
        e.g., `-sc=2.5`.
        Defaults to 1.
    
- `-r` or `--rasterize`:
        Output a rasterized image (PNG) instead of SVG.
    
- `-d=<int>` or `--dpi=<int>`:
        DPI of the rasterized output image.
        e.g., `--dpi=300`.
        Defaults to 96.
    
- `-e` or `--full-err`:
        Show the full error message.
    
- `-tp=<str>` or `--tex-program=<str>`: 
        TeX program to use for rendering.
        e.g., `-tp=lualatex`.
        Defaults to `pdflatex`.
    
- `-ta=<str>` or `--tex-args=<str>`: 
        Additional arguments to pass to the TeX program.
        e.g., `-ta="$tex_args_ipython_variable"`.
        Defaults to None.
    
- `-nc` or `--no-compile`:
        Do not compile the LaTeX code. 

- `-s=<str>` or `--save-tex=<str>`:
        Save the TikZ or TeX code to file.
        e.g., `-s=filename.tikz`.
        Defaults to None.
    
- `-S=<str>` or `--save-image=<str>`:
        Save the output image to file.
        e.g., `-S=filename.svg`.
        Defaults to None.

- `-sv=<str>` or `--save-var=<str>`:
        Save the TikZ or LaTeX code to an IPython variable.
        e.g., `-sv=var_name`.
        Defaults to None.