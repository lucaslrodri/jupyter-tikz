All notable changes to this project are presented below.

## v0.4.1

**✨ Improvements**

- Switched temporary file names to MD5 hashing for deterministic hashes.

**🚀 Features**

- Support to social cards (Twitter and Facebook OG).

**🐞 Bug Fixes**

- Fixed indentation in `TexDocument.tikz_code`.
- Fixed docs issues.

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
