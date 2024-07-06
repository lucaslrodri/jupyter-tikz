## Basic Usage

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

![Conway example](./assets/tikz/conway.svg)


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

![Quadratic formula](./assets/tikz/quadratic.png)

Going further, it is also possible to use it as a Python package:

```python
from jupyter_tikz import TexTemplate

tikz_code = tex_template_code = r"""\begin{tikzpicture}
    \draw[help lines] grid (5, 5);
     \filldraw [color=orange, opacity=0.3] (2.5,2.5) circle (1.5);
\end{tikzpicture}"""

tikz = TexTemplate(tikz_code)  # Create the tex template object

tikz.run_latex()  # Run LaTeX and shows the output
```