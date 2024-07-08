# Changelog

All notable changes to this project are presented below.

## v0.1.0

- First version released on PyPI.

## v0.1.1

**🐞 Bug Fixes**

- Minor fixes in README.

**🚀 Features**

- Added PyPI badge.

## v0.2.0

**🚀 Features**

- Option to save output code to an IPython variable (`-sv=<var_name>`).
- Flag (`--no-compile`) to prevent LaTeX compilation and image rendering.
- Support for LaTeX `\input{...}` commands.

## v0.2.1

**🐞 Bug Fixes**

- Minor adjustments in the README and Getting Started Notebook.

## v0.3.0

**🚀 Features**

- Web documentation.
- Flag (`--print-tex`) to print the full LaTeX document.
- UTF-8 support.

**🚨 Breaking Changes**

- Replaced `--full-document` and `--implicit-pic` with `--input-type=<str>`. `-f` and `-i` still work as aliases.
- Changed the `--as-jinja` flag to `--use-jinja`.
- Reworked the API to an object-oriented approach.