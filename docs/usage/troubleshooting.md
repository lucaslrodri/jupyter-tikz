## Troubleshooting pdflatex PATH Issues

If you encounter issues with the `pdflatex` PATH and receive the following error message:

<div class="result" style="padding-right: 0;">
<div class="log-output">
/bin/sh: 1: pdflatex: not found
</div>
</div>

First, ensure that the `pdflatex` command is accessible in your IDE environment. In some cases, you may need to add `pdflatex` to your system's PATH, or specify the `~` symbol before the command.

If you continue to experience issues, you can use the `-tp=<tex_program>` option to specify a custom `pdflatex` PATH. Here's an example:

```python
# Replace it for the path 
PDF_LATEX_PATH = r"C:\Users\lucas\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe"
```

```latex
%%tikz -as=tikz -t=pgfplots -nt -tp="$PDF_LATEX_PATH"
\begin{axis}[
  xlabel=$x$,
  ylabel={$f(x) = x^2 - x + 4$}
]
\addplot {x^2 - x + 4};
\end{axis}
```

<div class="result" markdown>
![Another quadratic formula](../assets/tikz/another_quadratic.svg)
</div>