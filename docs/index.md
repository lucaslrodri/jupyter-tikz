---
hide:
  - navigation
---

{% include "templates/logo.html" %}

---

<div class="code-showcase" markdown>
```latex
%%tikz
\begin{tikzpicture}
    \draw[help lines] grid (7, 5);
     \filldraw [color=red, opacity=0.3] (2.5,2.5) circle (1.5);
     \filldraw [color=cyan, opacity=0.3] (4.5,2.5) circle (1.5);
\end{tikzpicture}
```
<div class="result-showcase">
<img src="./assets/tikz/dots_in_grid.svg" alt="A dot and a gridline">
</div>
</div>


---

<div style="display: flex; justify-content: center; margin: 0 auto;">
<pre style="height: 4em; overflow-x: auto;">
<code class="language-shell" style="padding-right: 3em;">pip install jupyter-tikz</code>
</pre>
</div>


---

# Getting started
{{ description }}

## Basic Usage

{% include "templates/basic-usage.md" %}

## Next steps

Choose the following links to continue your journey:

<div class="grid">
  {% for href, icon, text in [
    ("./installation/", "computer", "<strong>Install</strong> Jupyter-TikZ"), 
    ("./arguments/", "terminal", "IPython Magics <strong>additional options</strong>"),
    ("./usage/as-magic/", "magic", "<strong>Usage</strong> as IPython Magics"), 
    ("./usage/as-package/", "package", "<strong>Usage</strong> as a Python Package"), 
  ] %}
    <a class="card card-link" href="{{ href }}"><span class="twemoji">{{ icons[icon] }}</span> {{ text }}</a>
  {% endfor %}
</div>

## Project Links

Explore additional resources and related links for this project:

<div class="grid">
 {% for href, icon, text in [
  ("https://pypi.org/project/jupyter-tikz/", "python", "<strong>PyPI</strong> page"),
  ("https://github.com/lucaslrodri/jupyter-tikz/blob/main/notebooks/GettingStarted.ipynb", "jupyter", "Getting Started <strong>notebook</strong>"),
  ("https://github.com/lucaslrodri/jupyter-tikz/", "github", "<strong>Source code</strong> in Github"),
  ("https://github.com/lucaslrodri/jupyter-tikz/issues/", "issues", "Github <strong>issues</strong> page")
 ] %}
  <a class="card card-link" href="{{ href }}"><span class="twemoji">{{ icons[icon] }}</span>&nbsp; {{ text }}</a>
 {% endfor %}
</div>

## Contribute

{% include "templates/contribute.md" %}

## Thanks

{% include "templates/motivation.md" %}

## License

{% include "templates/copyright.md" %}