---
hide:
  - navigation
---

{% include "templates/logo.html" %}

---

<div style="display: flex; justify-content: center; align-items: center; column-gap: 1em; margin: 0 auto; flex-wrap: wrap" markdown>
```latex
%%tikz
\begin{tikzpicture}
    \draw[help lines] grid (7, 5);
     \filldraw [color=red, opacity=0.3] (2.5,2.5) circle (1.5);
     \filldraw [color=cyan, opacity=0.3] (4.5,2.5) circle (1.5);
\end{tikzpicture}
```
![A dot and a gridline](./assets/dots_in_grid.svg){height="300"}
</div>


---

<div style="display: flex; justify-content: center; margin: 0 auto;">
<pre style="min-width: 16em; height: 2em;">
<code class="language-shell">pip install jupyter-tikz</code>
</pre>
</div>


---

# Getting started

{{ description }}

{% include "templates/basic-usage.md" %}

## Next steps

Choose the following links to continue your journey:

<div class="grid">
  {% for href, icon, text in [
    ("/install/", "computer", "<strong>Install</strong> Jupyter-TikZ"), 
    ("#", "closed-book", "<strong>Usage</strong> tutorials"), 
    ("#", "terminal", "IPython <strong>Magics arguments</strong> reference")
  ] %}
    <a class="card card-link" href="{{ href }}"><span class="twemoji">{{ icons[icon] }}</span> {{ text }}</a>
  {% endfor %}
</div>


## Project Links

Explore additional resources and related links for this project:

<div class="grid">
 {% for href, icon, text in [
  ("https://pypi.org/project/jupyter-tikz/", "python", "<strong>PyPI</strong> page"),
  ("https://github.com/lucaslrodri/jupyter-tikz/", "github", "<strong>Source code</strong> in Github"),
  ("https://github.com/lucaslrodri/jupyter-tikz/blob/main/GettingStarted.ipynb", "jupyter", "Example <strong>notebook</strong>")
 ] %}
  <a class="card card-link" href="https://pypi.org/project/jupyter-tikz/" target="_blank"><span class="twemoji">{{ icons[icon] }}</span> {{ text }}</a>
 {% endfor %}
</div>

{% include "templates/contribute.md" %}
{% include "templates/motivation.md" %}
{% include "templates/license.md" %}