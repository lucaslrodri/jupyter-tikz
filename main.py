import os
import re
import sys
from textwrap import dedent

import jinja2

sys.path.insert(1, "./jupyter_tikz")

import jupyter_tikz

DESCRIPTION = "Jupyter TikZ is an IPython Cell and Line Magic for rendering TeX/TikZ outputs in Jupyter Notebooks."


def _args_table():
    """
    This macro generates a table of the command line arguments
    """
    table = dedent(
        """
    | Argument | Description |
    | -------- | ----------- |
    """
    )
    for arg, params in jupyter_tikz._ARGS.items():
        type = params.get("type", str).__name__
        short = params.get("short-arg", arg)
        if params.get("type") == bool:
            argument = f"`-{short}`<br>`--{arg}`"
        else:
            argument = f"`-{short}=<{type}>`<br>`--{arg}=<{type}>`"

        description = [params["desc"] + "."]
        if "example" in params:
            description.append("&nbsp;" * 4 + f"*Example:* {params['example']}.")
        if "default" in params:
            if params["default"]:
                description.append(
                    "&nbsp;" * 4 + f"*Defaults* to `-{short}={params['default']}`."
                )
            elif params["default"] is None:
                description.append("&nbsp;" * 4 + f"*Defaults* to None.")
        description = "<br>".join(description)

        table += f"| {argument} | {description} |\n"
    return table


def define_env(env):
    """
    This is the hook for defining variables, macros and filters

    - variables: the dictionary that contains the environment variables
    - macro: a decorator function, to declare a macro.
    - filter: a function with one of more arguments,
        used to perform a transformation
    """

    # add to the dictionary of variables available to markdown pages:
    env.variables["description"] = DESCRIPTION

    env.variables["icons"] = {
        "computer": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 512"><path d="M384 96v224H64V96h320zM64 32C28.7 32 0 60.7 0 96v224c0 35.3 28.7 64 64 64h117.3l-10.7 32H96c-17.7 0-32 14.3-32 32s14.3 32 32 32h256c17.7 0 32-14.3 32-32s-14.3-32-32-32h-74.7l-10.7-32H384c35.3 0 64-28.7 64-64V96c0-35.3-28.7-64-64-64H64zm464 0c-26.5 0-48 21.5-48 48v352c0 26.5 21.5 48 48 48h64c26.5 0 48-21.5 48-48V80c0-26.5-21.5-48-48-48h-64zm16 64h32c8.8 0 16 7.2 16 16s-7.2 16-16 16h-32c-8.8 0-16-7.2-16-16s7.2-16 16-16zm-16 80c0-8.8 7.2-16 16-16h32c8.8 0 16 7.2 16 16s-7.2 16-16 16h-32c-8.8 0-16-7.2-16-16zm32 160a32 32 0 1 1 0 64 32 32 0 1 1 0-64z"></path></svg>',
        "closed-book": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M96 0C43 0 0 43 0 96v320c0 53 43 96 96 96h320c17.7 0 32-14.3 32-32s-14.3-32-32-32v-64c17.7 0 32-14.3 32-32V32c0-17.7-14.3-32-32-32H96zm0 384h256v64H96c-17.7 0-32-14.3-32-32s14.3-32 32-32zm32-240c0-8.8 7.2-16 16-16h192c8.8 0 16 7.2 16 16s-7.2 16-16 16H144c-8.8 0-16-7.2-16-16zm16 48h192c8.8 0 16 7.2 16 16s-7.2 16-16 16H144c-8.8 0-16-7.2-16-16s7.2-16 16-16z"></path></svg>',
        "terminal": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512"><path d="M9.4 86.6c-12.5-12.5-12.5-32.7 0-45.2s32.8-12.5 45.3 0l192 192c12.5 12.5 12.5 32.8 0 45.3l-192 192c-12.5 12.5-32.8 12.5-45.3 0s-12.5-32.8 0-45.3L178.7 256 9.4 86.6zM256 416h288c17.7 0 32 14.3 32 32s-14.3 32-32 32H256c-17.7 0-32-14.3-32-32s14.3-32 32-32z"></path></svg>',
        "python": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M439.8 200.5c-7.7-30.9-22.3-54.2-53.4-54.2h-40.1v47.4c0 36.8-31.2 67.8-66.8 67.8H172.7c-29.2 0-53.4 25-53.4 54.3v101.8c0 29 25.2 46 53.4 54.3 33.8 9.9 66.3 11.7 106.8 0 26.9-7.8 53.4-23.5 53.4-54.3v-40.7H226.2v-13.6h160.2c31.1 0 42.6-21.7 53.4-54.2 11.2-33.5 10.7-65.7 0-108.6zM286.2 404c11.1 0 20.1 9.1 20.1 20.3 0 11.3-9 20.4-20.1 20.4-11 0-20.1-9.2-20.1-20.4.1-11.3 9.1-20.3 20.1-20.3zM167.8 248.1h106.8c29.7 0 53.4-24.5 53.4-54.3V91.9c0-29-24.4-50.7-53.4-55.6-35.8-5.9-74.7-5.6-106.8.1-45.2 8-53.4 24.7-53.4 55.6v40.7h106.9v13.6h-147c-31.1 0-58.3 18.7-66.8 54.2-9.8 40.7-10.2 66.1 0 108.6 7.6 31.6 25.7 54.2 56.8 54.2H101v-48.8c0-35.3 30.5-66.4 66.8-66.4zm-6.7-142.6c-11.1 0-20.1-9.1-20.1-20.3.1-11.3 9-20.4 20.1-20.4 11 0 20.1 9.2 20.1 20.4s-9 20.3-20.1 20.3z"></path></svg>',
        "jupyter": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M7.157 22.201A1.784 1.799 0 0 1 5.374 24a1.784 1.799 0 0 1-1.784-1.799 1.784 1.799 0 0 1 1.784-1.799 1.784 1.799 0 0 1 1.783 1.799zM20.582 1.427a1.415 1.427 0 0 1-1.415 1.428 1.415 1.427 0 0 1-1.416-1.428A1.415 1.427 0 0 1 19.167 0a1.415 1.427 0 0 1 1.415 1.427zM4.992 3.336A1.047 1.056 0 0 1 3.946 4.39a1.047 1.056 0 0 1-1.047-1.055A1.047 1.056 0 0 1 3.946 2.28a1.047 1.056 0 0 1 1.046 1.056zm7.336 1.517c3.769 0 7.06 1.38 8.768 3.424a9.363 9.363 0 0 0-3.393-4.547 9.238 9.238 0 0 0-5.377-1.728A9.238 9.238 0 0 0 6.95 3.73a9.363 9.363 0 0 0-3.394 4.547c1.713-2.04 5.004-3.424 8.772-3.424zm.001 13.295c-3.768 0-7.06-1.381-8.768-3.425a9.363 9.363 0 0 0 3.394 4.547A9.238 9.238 0 0 0 12.33 21a9.238 9.238 0 0 0 5.377-1.729 9.363 9.363 0 0 0 3.393-4.547c-1.712 2.044-5.003 3.425-8.772 3.425Z"></path></svg>',
        "magic": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512"><path d="M234.7 42.7 197 56.8c-3 1.1-5 4-5 7.2s2 6.1 5 7.2l37.7 14.1 14.1 37.7c1.1 3 4 5 7.2 5s6.1-2 7.2-5l14.1-37.7L315 71.2c3-1.1 5-4 5-7.2s-2-6.1-5-7.2l-37.7-14.1L263.2 5c-1.1-3-4-5-7.2-5s-6.1 2-7.2 5l-14.1 37.7zM46.1 395.4c-18.7 18.7-18.7 49.1 0 67.9l34.6 34.6c18.7 18.7 49.1 18.7 67.9 0l381.3-381.4c18.7-18.7 18.7-49.1 0-67.9l-34.6-34.5c-18.7-18.7-49.1-18.7-67.9 0L46.1 395.4zM484.6 82.6l-105 105-23.3-23.3 105-105 23.3 23.3zM7.5 117.2C3 118.9 0 123.2 0 128s3 9.1 7.5 10.8L64 160l21.2 56.5c1.7 4.5 6 7.5 10.8 7.5s9.1-3 10.8-7.5L128 160l56.5-21.2c4.5-1.7 7.5-6 7.5-10.8s-3-9.1-7.5-10.8L128 96l-21.2-56.5c-1.7-4.5-6-7.5-10.8-7.5s-9.1 3-10.8 7.5L64 96 7.5 117.2zm352 256c-4.5 1.7-7.5 6-7.5 10.8s3 9.1 7.5 10.8L416 416l21.2 56.5c1.7 4.5 6 7.5 10.8 7.5s9.1-3 10.8-7.5L480 416l56.5-21.2c4.5-1.7 7.5-6 7.5-10.8s-3-9.1-7.5-10.8L480 352l-21.2-56.5c-1.7-4.5-6-7.5-10.8-7.5s-9.1 3-10.8 7.5L416 352l-56.5 21.2z"></path></svg>',
        "package": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M50.7 58.5 0 160h208V32H93.7c-18.2 0-34.8 10.3-43 26.5zM240 160h208L397.3 58.5c-8.2-16.2-24.8-26.5-43-26.5H240v128zm208 32H0v224c0 35.3 28.7 64 64 64h320c35.3 0 64-28.7 64-64V192z"></path></svg>',
        "github": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 496 512"><path d="M165.9 397.4c0 2-2.3 3.6-5.2 3.6-3.3.3-5.6-1.3-5.6-3.6 0-2 2.3-3.6 5.2-3.6 3-.3 5.6 1.3 5.6 3.6zm-31.1-4.5c-.7 2 1.3 4.3 4.3 4.9 2.6 1 5.6 0 6.2-2s-1.3-4.3-4.3-5.2c-2.6-.7-5.5.3-6.2 2.3zm44.2-1.7c-2.9.7-4.9 2.6-4.6 4.9.3 2 2.9 3.3 5.9 2.6 2.9-.7 4.9-2.6 4.6-4.6-.3-1.9-3-3.2-5.9-2.9zM244.8 8C106.1 8 0 113.3 0 252c0 110.9 69.8 205.8 169.5 239.2 12.8 2.3 17.3-5.6 17.3-12.1 0-6.2-.3-40.4-.3-61.4 0 0-70 15-84.7-29.8 0 0-11.4-29.1-27.8-36.6 0 0-22.9-15.7 1.6-15.4 0 0 24.9 2 38.6 25.8 21.9 38.6 58.6 27.5 72.9 20.9 2.3-16 8.8-27.1 16-33.7-55.9-6.2-112.3-14.3-112.3-110.5 0-27.5 7.6-41.3 23.6-58.9-2.6-6.5-11.1-33.3 2.6-67.9 20.9-6.5 69 27 69 27 20-5.6 41.5-8.5 62.8-8.5s42.8 2.9 62.8 8.5c0 0 48.1-33.6 69-27 13.7 34.7 5.2 61.4 2.6 67.9 16 17.7 25.8 31.5 25.8 58.9 0 96.5-58.9 104.2-114.8 110.5 9.2 7.9 17 22.9 17 46.4 0 33.7-.3 75.4-.3 83.6 0 6.5 4.6 14.4 17.3 12.1C428.2 457.8 496 362.9 496 252 496 113.3 383.5 8 244.8 8zM97.2 352.9c-1.3 1-1 3.3.7 5.2 1.6 1.6 3.9 2.3 5.2 1 1.3-1 1-3.3-.7-5.2-1.6-1.6-3.9-2.3-5.2-1zm-10.8-8.1c-.7 1.3.3 2.9 2.3 3.9 1.6 1 3.6.7 4.3-.7.7-1.3-.3-2.9-2.3-3.9-2-.6-3.6-.3-4.3.7zm32.4 35.6c-1.6 1.3-1 4.3 1.3 6.2 2.3 2.3 5.2 2.6 6.5 1 1.3-1.3.7-4.3-1.3-6.2-2.2-2.3-5.2-2.6-6.5-1zm-11.4-14.7c-1.6 1-1.6 3.6 0 5.9 1.6 2.3 4.3 3.3 5.6 2.3 1.6-1.3 1.6-3.9 0-6.2-1.4-2.3-4-3.3-5.6-2z"></path></svg>',
        "issues": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><path d="M3.75 8a4.25 4.25 0 1 1 8.5 0 4.25 4.25 0 0 1-8.5 0ZM9.5 8a1.5 1.5 0 1 0-3.001.001A1.5 1.5 0 0 0 9.5 8Z"></path><path d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8Zm8-5.75a5.75 5.75 0 1 0 0 11.5 5.75 5.75 0 1 0 0-11.5Z"></path></svg>',
    }

    @env.macro
    def args_table():
        return _args_table()


README_TEMPLATE = r"""
{% include "docs/templates/logo.html" %}

<p align="center">
<a 
    href="https://jupyter-tikz.readthedocs.io/"
>Documentation</a> | <a
    href="https://github.com/lucaslrodri/jupyter-tikz/blob/main/notebooks/GettingStarted.ipynb"
>Getting Started notebook</a>
</p>

# Installation

{% include "./docs/installation.md" %}

# Basic usage

{% include "./docs/templates/basic-usage.md" %}

# Additional options

All additional options are listed below:

{{ args_table }}

# Contribute

{% include "./docs/templates/contribute.md" %}

# Changelog

{% include "./docs/about/changelog.md" %}

# Thanks

{% include "./docs/templates/motivation.md" %}

# License

{% include "./docs/templates/copyright.md" %}
""".strip()

if __name__ == "__main__":

    args_table = _args_table()

    print(os.getcwd())

    fs_loader = jinja2.FileSystemLoader(os.getcwd())
    tmpl_env = jinja2.Environment(loader=fs_loader)

    tmpl = tmpl_env.from_string(README_TEMPLATE)

    rendered_readme = tmpl.render(locals())

    # Remove mkdocs admonitions
    # 1. Define the regex pattern to match MkDocs admonitions
    admonition_pattern = re.compile(
        r'!!!\s+(note|abstract|info|tip|success|question|warning|failure|danger|bug|example|quote)\s*(?: ".*?")?\n    (.+)(?:\s*)(?=.+)',
    )

    # 2. Replace MkDocs admonitions with GitHub alerts
    print(re.findall(admonition_pattern, rendered_readme))
    rendered_readme = admonition_pattern.sub("", rendered_readme)

    # Remove code annotations
    rendered_readme = re.sub(
        r"\s\{\s\.(shell|python|latex)\s\.annotate\s\}",
        r"\1",
        rendered_readme,
        flags=re.DOTALL,
    )

    logterminal_div_pattern = '<div class="result log-terminal".*?>.*?</div>'

    rendered_readme = re.sub(
        logterminal_div_pattern, "", rendered_readme, flags=re.DOTALL
    )

    result_div_pattern = r'<div class="result"(.*?)>\s*(.*?)\s*</div>'

    rendered_readme = re.sub(
        result_div_pattern, r"\2", rendered_readme, flags=re.DOTALL
    )

    # License
    rendered_readme = rendered_readme.replace(
        "./about/license.md",
        "https://github.com/lucaslrodri/jupyter-tikz/blob/main/LICENSE",
    )

    # Development
    rendered_readme = rendered_readme.replace(
        "about/development/",
        "https://jupyter-tikz.readthedocs.io/stable/about/development/",
    )

    # Internal links

    domain = "https://jupyter-tikz.readthedocs.io/stable/"

    rendered_readme = rendered_readme.replace("./", domain).replace(".md", "")

    yaml_pattern = r"---\s*\n.*?\n---\s*\n"
    rendered_readme = re.sub(yaml_pattern, "", rendered_readme, flags=re.DOTALL)

    # Remove code annotations
    rendered_readme = re.sub(r"^1\.\s+.*$\n", "", rendered_readme, flags=re.MULTILINE)
    rendered_readme = re.sub(r" #\s*\(\d+\)!", "", rendered_readme, flags=re.DOTALL)

    # # Remove empty subsections

    # # 1. Define the regex pattern to match empty subsections
    empty_subsection_pattern = re.compile(r"###\s+.*\s*(?=\n##.*)")

    # # 2. Remove empty subsections
    rendered_readme = empty_subsection_pattern.sub("", rendered_readme)

    # Remove more than two consecutive new lines
    consecutive_newlines_pattern = re.compile(r"\n{3,}")
    rendered_readme = consecutive_newlines_pattern.sub("\n\n", rendered_readme)

    print(rendered_readme)

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(rendered_readme)
