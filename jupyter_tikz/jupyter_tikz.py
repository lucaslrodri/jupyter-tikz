"""Jupyter TikZ is an IPython Cell and Line Magic for rendering TeX/TikZ outputs in Jupyter Notebooks."""

import os
import re
import subprocess
import sys
from pathlib import Path
from string import Template
from textwrap import indent
from typing import Any, Literal

from IPython import display
from IPython.core.magic import Magics, line_cell_magic, magics_class, needs_local_scope
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring
from IPython.display import SVG, Image

_EXTRAS_CONFLITS_ERR = "You cannot provide `preamble` and (`tex_packages`, `tikz_libraries`, and/or `pgfplots_libraries`) at the same time."
_PRINT_CONFLICT_ERR = (
    "You cannot use `--print-jinja` and `--print-tex` at the same time."
)
_INPUT_TYPE_CONFLIT_ERR = "You cannot use `--implicit-pic`, `--full-document` or/and `-as=<input_type>` at the same time."
_JINJA_NOT_INTALLED_ERR = (
    "Template cannot be rendered. Please install jinja2: `$ pip install jinja2`"
)
_NS_NOT_PROVIDED_ERR = 'Namespace must be provided when using `use_jinja`, i.e.: `ns=locals()` or `ns={"my_var": value}`'


class TexDocument:
    """This class provides functionality to create and render a LaTeX document given the full LaTeX code. It can also constructs LaTeX code using Jinja2 templates."""

    def __init__(
        self, code: str, use_jinja: bool = False, ns: dict[str, Any] | None = None
    ):
        """Initializes the `TexDocument` class.

        Args:
            code: LaTeX code to render.
            use_jinja: A flag to indicate if the code uses Jinja2 template.
            ns: A namespace dictionary with the variables to render the Jinja2 template. It must be provided when `use_jinja` is `True`.

        Raises:
            ValueError: If `use_jinja` is `True` and `ns` is not provided.
        """
        self._code: str = code.strip()
        self._use_jinja: bool = use_jinja
        if self._use_jinja and not ns:
            raise ValueError(_NS_NOT_PROVIDED_ERR)

        if self._use_jinja:
            self._render_jinja(ns)

    @property
    def full_latex(self) -> str:
        """Returns the full LaTeX code to render."""
        return self._code

    @property
    def tikz_code(self) -> str | None:
        r"""Returns the TikZ code."""
        pattern = r"\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}"
        match = re.search(pattern, self.full_latex, re.DOTALL)
        if match:
            return match.group(0)
        return None

    @staticmethod
    def _arg_head(arg, limit=60) -> str:
        if type(arg) == str:
            arg = arg.strip()
            arg = f"{arg[:limit]}..." if len(arg) > limit else arg
            arg = str(repr(arg.strip()))
        else:
            arg = str(arg)
        return arg

    def __hash__(self) -> int:
        """Returns the hash value of the full LaTeX code."""
        return hash(self.full_latex)

    @property
    def _hex_hash(self) -> str:
        """Returns the hexadecimal representation of the hash value of the full LaTeX code."""
        return f"{abs(self.__hash__()):x}"

    def __repr__(self) -> str:
        params_dict = self.__dict__
        if "scale" in params_dict.keys():
            if params_dict["scale"] == 1.0:
                del params_dict["scale"]

        params = ", ".join(
            [
                f'{k if k != "_use_jinja" else "use_jinja"}={self._arg_head(v)}'
                for k, v in params_dict.items()
                if k not in ["_code", "full_latex", "ns"] and v
            ]
        )
        if params:
            params = ", " + params
        return f"{self.__class__.__name__}({self._arg_head(self._code)}{params})"

    def __str__(self) -> str:
        """Returns the LaTeX code string to render.

        Returns:
            str: The LaTeX code to render.
        """
        return self._code

    def _clearup_latex_garbage(self, keep_temp) -> None:
        if not (keep_temp):  # F
            files = Path().glob(f"{self._hex_hash}.*")
            for file in files:
                if file.exists():
                    file.unlink()

    def _run_command(self, command: str, full_err: bool = False, **kwargs) -> int:

        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            check=False,
            **kwargs,
        )
        if result.returncode != 0:
            err_msg = result.stderr if result.stderr else result.stdout
            if not full_err:  # tail -n 20
                err_msg = "\n".join(err_msg.splitlines()[-20:])
            print(err_msg, file=sys.stderr)
        return result.returncode

    def _save(
        self, dest: str, ext: Literal["tikz", "tex", "png", "svg", "pdf"]
    ) -> None:
        dest_path = Path(dest)

        if os.environ.get("JUPYTER_TIKZ_SAVEDIR"):
            dest_path = str(os.environ.get("JUPYTER_TIKZ_SAVEDIR")) / dest_path
        else:
            dest_path = dest_path

        dest_path = dest_path.resolve()

        if dest_path.suffix != f".{ext}":
            dest_path = dest_path.with_suffix(dest_path.suffix + f".{ext}")

        dest_path.parent.mkdir(parents=True, exist_ok=True)

        if ext == "tikz":
            if not self.tikz_code:
                raise ValueError("No TikZ code to save.")
            dest_path.with_suffix(".tikz").write_text(self.tikz_code, encoding="utf-8")
        else:
            Path(self._hex_hash).with_suffix(f".{ext}").replace(
                dest_path.with_suffix(f".{ext}")
            )

    def run_latex(
        self,
        tex_program: str = "pdflatex",
        tex_args: str | None = None,
        rasterize: bool = False,
        full_err: bool = False,
        keep_temp: bool = False,
        save_image: str | None = None,
        dpi: int = 96,
        grayscale: bool = False,
        save_tex: str | None = None,
        save_tikz: str | None = None,
        save_pdf: str | None = None,
    ) -> Image | SVG | None:
        """Run the LaTeX program to render the LaTeX code.

        Args:
            tex_program: The LaTeX program to use for compilation.
            tex_args: Arguments to pass to the TeX program.
            rasterize: Output a rasterized image (PNG) instead of SVG.
            full_err: Print the full error message when an error occurs. If False, it prints only the last 20 lines.
            keep_temp: Keep temporary LaTeX files.
            save_image: Save the output image to file.
            dpi: DPI to use when rasterizing the image.
            grayscale: Set grayscale to a rasterized image.
            save_tex: Save the full LaTeX code to file.
            save_tikz: Save the TikZ code to file.
            save_pdf: Save the output PDF to file.

        Returns:
            Image | SVG | None: The rendered image. None if an error occurs.
        """
        try:

            tex_path = Path().resolve() / f"{self._hex_hash}.tex"
            tex_path.write_text(self.full_latex, encoding="utf-8")

            tex_command = tex_program
            if tex_args:
                tex_command += f" {tex_args}"
            tex_command += f" {tex_path}"

            res = self._run_command(tex_command, full_err=full_err)
            if res != 0:
                self._clearup_latex_garbage(keep_temp)
                return None

            image_format = "svg" if not rasterize else "png"

            if os.environ.get("JUPYTER_TIKZ_PDFTOCAIROPATH"):
                pdftocairo_path = os.environ.get("JUPYTER_TIKZ_PDFTOCAIROPATH")
            else:
                pdftocairo_path = "pdftocairo"

            pdftocairo_command = f"{pdftocairo_path} -{image_format}"
            if rasterize:
                pdftocairo_command += (
                    f" -singlefile -{'gray' if grayscale else 'transp'} -r {dpi}"
                )

            pdftocairo_command += f" {tex_path.with_suffix('.pdf')}"
            pdftocairo_command += (
                f" {tex_path.with_suffix('.svg')}"
                if not rasterize
                else f" {tex_path.parent / tex_path.stem}"
            )
            res = self._run_command(pdftocairo_command, full_err=full_err)

            if res != 0:
                self._clearup_latex_garbage(keep_temp)
                return None

            image = (
                display.Image(tex_path.with_suffix(".png"))
                if rasterize
                else display.SVG(tex_path.with_suffix(".svg"))
            )

            if save_image:
                self._save(save_image, image_format)
            if save_tex:
                self._save(save_tex, "tex")
            if save_pdf:
                self._save(save_pdf, "pdf")
            if save_tikz and self.tikz_code:
                self._save(save_tikz, "tikz")

            self._clearup_latex_garbage(keep_temp)

            return image
        except Exception as e:
            raise e
        finally:
            self._clearup_latex_garbage(keep_temp)

    def _render_jinja(self, ns) -> None:
        try:
            import jinja2
        except ImportError:
            raise ImportError(_JINJA_NOT_INTALLED_ERR)

        fs_loader = jinja2.FileSystemLoader(os.getcwd())
        tmpl_env = jinja2.Environment(loader=fs_loader)

        tmpl = tmpl_env.from_string(self._code)

        self._code = tmpl.render(**ns)


class TexFragment(TexDocument):
    """This class provides functionality to create and render a standalone LaTeX document given a TikZ Picture or LaTeX fragment."""

    TMPL = Template(
        "\\documentclass{standalone}\n"
        + "$preamble"
        + "\\begin{document}\n"
        + "$scale_begin"
        + "$tikzpicture_begin"
        + "$code"
        + "$tikzpicture_end"
        + "$scale_end"
        + "\\end{document}"
    )
    TMPL_STANDALONE_PREAMBLE = Template(
        "$graphicx_package"
        + "$tikz_package"
        + "$tex_packages"
        + "$tikz_libraries"
        + "$pgfplots_libraries"
    )

    def __init__(
        self,
        code: str,
        implicit_tikzpicture: bool = False,
        scale: float = 1.0,
        preamble: str | None = None,
        tex_packages: str | None = None,
        tikz_libraries: str | None = None,
        pgfplots_libraries: str | None = None,
        no_tikz: bool = False,
        **kargs,
    ):
        """Initializes the `TexFragment` class.

        Args:
            code: TikZ Picture or LaTeX fragment to render.
            implicit_tikzpicture: A flag to indicate if the final LaTeX should implicitly wrap a TikZ Picture.
            scale: The scale factor to apply to the TikZ/LaTeX code. It uses the `\\scalebox` command from graphicx package.
            preamble: LaTeX preamble to insert before the document.
            tex_packages: Comma-separated list of TeX packages.
            tikz_libraries: Comma-separated list of TikZ libraries.
            pgfplots_libraries: Comma-separated list of pgfplots libraries.
            no_tikz: Force to not import the TikZ package.

        Raises:
            ValueError: If `preamble` and (`tex_packages`, `tikz_libraries`, and/or `pgfplots_libraries`) are provided at the same time.
        """
        if preamble and (tex_packages or tikz_libraries or pgfplots_libraries):
            raise ValueError(_EXTRAS_CONFLITS_ERR)

        self.template = "tikzpicture" if implicit_tikzpicture else "standalone-document"
        self.scale = scale or 1.0
        if preamble:
            self.preamble = preamble.strip() + "\n"
        else:
            self.preamble = self._build_standalone_preamble(
                tex_packages, tikz_libraries, pgfplots_libraries, no_tikz
            )

        super().__init__(code, **kargs)

    def _build_standalone_preamble(
        self,
        tex_packages: str | None = None,
        tikz_libraries: str | None = None,
        pgfplots_libraries: str | None = None,
        no_tikz: bool = False,
    ) -> str:
        tikz_package = "" if no_tikz else "\\usepackage{tikz}\n"

        graphicx_package = "" if self.scale == 1 else "\\usepackage{graphicx}\n"

        tex_packages = "\\usepackage{%s}\n" % tex_packages if tex_packages else ""
        tikz_libraries = (
            "\\usetikzlibrary{%s}\n" % tikz_libraries if tikz_libraries else ""
        )
        pgfplots_libraries = (
            "\\usepgfplotslibrary{%s}\n" % pgfplots_libraries
            if pgfplots_libraries
            else ""
        )

        return self.TMPL_STANDALONE_PREAMBLE.substitute(
            graphicx_package=graphicx_package,
            tikz_package=tikz_package,
            tex_packages=tex_packages,
            tikz_libraries=tikz_libraries,
            pgfplots_libraries=pgfplots_libraries,
        )

    @property
    def full_latex(self) -> str:
        """Returns the full LaTeX code to render."""
        if self.scale != 1:
            scale_begin = indent("\\scalebox{" + str(self.scale) + "}{\n", " " * 4)
            scale_end = indent("}\n", " " * 4)
        else:
            scale_begin = ""
            scale_end = ""

        if self.template == "tikzpicture":
            tikzpicture_begin = indent("\\begin{tikzpicture}\n", " " * 4)
            tikzpicture_end = indent("\\end{tikzpicture}\n", " " * 4)
            code_indent = " " * 8
        else:
            tikzpicture_begin = ""
            tikzpicture_end = ""
            code_indent = " " * 4

        code = indent(self._code, code_indent) + "\n" if self._code else ""

        return self.TMPL.substitute(
            preamble=self.preamble,
            scale_begin=scale_begin,
            tikzpicture_begin=tikzpicture_begin,
            code=code,
            tikzpicture_end=tikzpicture_end,
            scale_end=scale_end,
        )


_ARGS = {
    "input-type": {  # New
        "short-arg": "as",
        "dest": "input_type",
        "type": str,
        "default": "standalone-document",
        "desc": "Type of the input. Possible values are: `full-document`, `standalone-document` and `tikzpicture`",
        "example": "`-as=full-document`",
    },
    "implicit-pic": {  # Deprecated
        "short-arg": "i",
        "dest": "implicit_pic",
        "type": bool,
        "desc": "Alias for `-as=tikzpicture`",
    },
    "full-document": {  # Deprecated
        "short-arg": "f",
        "dest": "full_document",
        "type": bool,
        "desc": "Alias for `-as=full-document`",
    },
    "latex-preamble": {
        "short-arg": "p",
        "dest": "latex_preamble",
        "type": str,
        "default": None,
        "desc": "LaTeX preamble to insert before the document",
        "example": '`-p="$preamble"`, with the preamble being an IPython variable',
    },
    "tex-packages": {
        "short-arg": "t",
        "dest": "tex_packages",
        "type": str,
        "default": None,
        "desc": "Comma-separated list of TeX packages",
        "example": "`-t=amsfonts,amsmath`",
    },
    "no-tikz": {
        "short-arg": "nt",
        "dest": "no_tikz",
        "type": bool,
        "desc": "Force to not import the TikZ package",
    },
    "tikz-libraries": {
        "short-arg": "l",
        "dest": "tikz_libraries",
        "type": str,
        "default": None,
        "desc": "Comma-separated list of TikZ libraries",
        "example": "`-l=calc,arrows`",
    },
    "pgfplots-libraries": {
        "short-arg": "lp",
        "dest": "pgfplots_libraries",
        "type": str,
        "default": None,
        "desc": "Comma-separated list of pgfplots libraries",
        "example": "`-pl=groupplots,external`",
    },
    "use-jinja": {  # Changed
        "short-arg": "j",
        "dest": "use_jinja",
        "type": bool,
        "desc": "Render the code using Jinja2",
    },
    "print-jinja": {
        "short-arg": "pj",
        "dest": "print_jinja",
        "type": bool,
        "desc": "Print the rendered Jinja2 template",
    },
    "print-tex": {  # New
        "short-arg": "pt",
        "dest": "print_tex",
        "type": bool,
        "desc": "Print the full LaTeX document",
    },
    "scale": {
        "short-arg": "sc",
        "dest": "scale",
        "type": float,
        "default": 1.0,
        "desc": "The scale factor to apply to the TikZ diagram",
        "example": "`-sc=0.5`",
    },
    "rasterize": {
        "short-arg": "r",
        "dest": "rasterize",
        "type": bool,
        "desc": "Output a rasterized image (PNG) instead of SVG",
    },
    "dpi": {
        "short-arg": "d",
        "dest": "dpi",
        "type": int,
        "default": 96,
        "desc": "DPI to use when rasterizing the image",
        "example": "`--dpi=300`",
    },
    "gray": {  # New
        "short-arg": "g",
        "dest": "gray",
        "type": bool,
        "desc": "Set grayscale to the rasterized image",
    },
    "full-err": {
        "short-arg": "e",
        "dest": "full_err",
        "type": bool,
        "desc": "Print the full error message when an error occurs",
    },
    "keep-temp": {  # New
        "short-arg": "k",
        "dest": "keep_temp",
        "type": bool,
        "desc": "Keep temporary files",
    },
    "tex-program": {
        "short-arg": "tp",
        "dest": "tex_program",
        "type": str,
        "default": "pdflatex",
        "desc": "TeX program to use for compilation",
        "example": "`-tp=xelatex` or `-tp=lualatex`",
    },
    "tex-args": {
        "short-arg": "ta",
        "dest": "tex_args",
        "type": str,
        "default": None,
        "desc": "Arguments to pass to the TeX program",
        "example": '`-ta="$tex_args_ipython_variable"`',
    },
    "no-compile": {
        "short-arg": "nc",
        "dest": "no_compile",
        "type": bool,
        "desc": "Do not compile the TeX code",
    },
    "save-tikz": {  # New
        "short-arg": "s",
        "dest": "save_tikz",
        "type": str,
        "default": None,
        "desc": "Save the TikZ code to file",
        "example": "`-s filename.tikz`",
    },
    "save-tex": {  # Changed
        "short-arg": "st",
        "dest": "save_tex",
        "type": str,
        "default": None,
        "desc": "Save full LaTeX code to file",
        "example": "`-st filename.tex`",
    },
    "save-pdf": {  # New
        "short-arg": "sp",
        "dest": "save_pdf",
        "type": str,
        "default": None,
        "desc": "Save PDF file",
        "example": "`-sp filename.pdf`",
    },
    "save-image": {
        "short-arg": "S",
        "dest": "save_image",
        "type": str,
        "default": None,
        "desc": "Save the output image to file",
        "example": "`-S filename.png`",
    },
    "save-var": {
        "short-arg": "sv",
        "dest": "save_var",
        "type": str,
        "default": None,
        "desc": "Save the TikZ or LaTeX code to an IPython variable",
        "example": "`-sv my_var`",
    },
}


def _get_arg_params(arg: str) -> tuple[tuple[str, str], dict[str, Any]]:
    def get_arg_help(arg: str) -> str:
        help = _ARGS[arg]["desc"].replace("<br>", " ")
        if _ARGS[arg].get("example"):
            help += f", e.g., {_ARGS[arg]['example']}"
        if _ARGS[arg].get("default"):
            help += (
                f". Defaults to `-{_ARGS[arg]['short-arg']}={_ARGS[arg]['default']}`"
            )
        help += "."
        return help

    args = (f"-{_ARGS[arg]['short-arg']}", f"--{arg}")
    kwargs = {"dest": _ARGS[arg]["dest"]}
    if _ARGS[arg]["type"] == bool:
        kwargs["action"] = "store_true"
        kwargs["default"] = False
    elif _ARGS[arg]["type"] == str:
        kwargs["default"] = _ARGS[arg]["default"]
    else:
        kwargs["type"] = _ARGS[arg]["type"]
        kwargs["default"] = _ARGS[arg]["default"]
    kwargs["help"] = get_arg_help(arg)
    return args, kwargs


def _apply_args():
    def decorator(magic_command):
        for arg in reversed(_ARGS.keys()):
            args, kwargs = _get_arg_params(arg)
            magic_command = argument(*args, **kwargs)(magic_command)
        return magic_command

    return decorator


@magics_class
class TikZMagics(Magics):
    def _get_input_type(self, input_type: str) -> str | None:
        VALID_INPUT_TYPES = ["full-document", "standalone-document", "tikzpicture"]
        input_type = input_type.lower()
        input_type_len = len(input_type)

        for index, valid_input_type in enumerate(VALID_INPUT_TYPES):
            if input_type == valid_input_type[:input_type_len]:
                return VALID_INPUT_TYPES[index]

        return None

    # Path to the pdftocairo executable
    @line_cell_magic
    @magic_arguments()
    @_apply_args()
    @argument(  # Deprecated
        "--as-jinja",
        dest="as_jinja",
        action="store_true",
        default=False,
        help="Deprecated. Use `--use-jinja` instead.",
    )
    @argument("code", nargs="?", help="the variable in IPython with the Tex/TikZ code")
    @needs_local_scope
    def tikz(self, line, cell: str | None = None, local_ns=None) -> Image | SVG | None:
        r"""
        Renders a TikZ diagram in a Jupyter notebook cell. This function can be used as both a line magic (%tikz) and a cell magic (%%tikz).

        When used as cell magic, it executes the TeX/TikZ code within the cell:
            Example:
                In [3]: %%tikz
                   ...:  \begin{tikzpicture}
                   ...:     \draw (0,0) rectangle (1,1);
                   ...: \end{tikzpicture}

        When used as line magic, the TeX/TikZ code is passed as an IPython string variable:
            Example:
                In [4]: %tikz "$ipython_string_variable_with_code"

        Additional options can be passed to the magic command to customize LaTeX code and rendering output:
            Example:
                In [5]: %%tikz -l=arrows,matrix
                   ...: \matrix (m) [matrix of math nodes, row sep=3em, column sep=4em] {
                   ...:     A & B \\
                   ...:     C & D \\
                   ...: };
                   ...: \path[-stealth, line width=.4mm]
                   ...:     (m-1-1) edge node [left ] {$ac$} (m-2-1)
                   ...:     (m-1-1) edge node [above] {$ab$} (m-1-2)
                   ...:     (m-1-2) edge node [right] {$bd$} (m-2-2)
                   ...:     (m-2-1) edge node [below] {$cd$} (m-2-2);
        """

        self.args = parse_argstring(self.tikz, line)

        if self.args.latex_preamble and (
            self.args.tex_packages
            or self.args.tikz_libraries
            or self.args.pgfplots_libraries
        ):
            print(_EXTRAS_CONFLITS_ERR, file=sys.stderr)
            return

        if (self.args.implicit_pic and self.args.full_document) or (
            (self.args.implicit_pic or self.args.full_document)
            and self.args.input_type != "standalone-document"
        ):
            print(
                _INPUT_TYPE_CONFLIT_ERR,
                file=sys.stderr,
            )
            return
        if self.args.as_jinja:
            self.args.use_jinja = True
        if self.args.print_jinja and self.args.print_tex:
            print(
                _PRINT_CONFLICT_ERR,
                file=sys.stderr,
            )
            return

        if self.args.implicit_pic:
            self.input_type = "tikzpicture"
        elif self.args.full_document:
            self.input_type = "full-document"
        else:
            self.input_type = self._get_input_type(self.args.input_type)
        if self.input_type is None:
            print(
                f"`{self.args.input_type}` is not a valid input type.",
                "Valid input types are `full-document`, `standalone-document`, or `tikzpicture`.",
                file=sys.stderr,
            )
            return

        self.src = cell or ""
        local_ns = local_ns or {}

        if cell is None:
            if self.args.code is None:
                print('Use "%tikz?" for help', file=sys.stderr)
                return

            if self.args.code not in local_ns:
                self.src: str = self.args.code
            else:
                self.src: str = local_ns[self.args.code]

        if self.input_type == "full-document":
            self.tex_obj = TexDocument(
                self.src, use_jinja=self.args.use_jinja, ns=local_ns
            )
        else:
            implicit_tikzpicture = self.input_type == "tikzpicture"
            self.tex_obj = TexFragment(
                self.src,
                implicit_tikzpicture=implicit_tikzpicture,
                preamble=self.args.latex_preamble,
                tex_packages=self.args.tex_packages,
                no_tikz=self.args.no_tikz,
                tikz_libraries=self.args.tikz_libraries,
                pgfplots_libraries=self.args.pgfplots_libraries,
                scale=self.args.scale,
                use_jinja=self.args.use_jinja or self.args.print_jinja,
                ns=local_ns,
            )

        if self.args.print_jinja:
            print(self.tex_obj)
        if self.args.print_tex:
            print(self.tex_obj.full_latex)

        image = None
        if not self.args.no_compile:
            image = self.tex_obj.run_latex(
                tex_program=self.args.tex_program,
                tex_args=self.args.tex_args,
                rasterize=self.args.rasterize,
                full_err=self.args.full_err,
                keep_temp=self.args.keep_temp,
                save_tikz=self.args.save_tikz,
                save_tex=self.args.save_tex,
                save_pdf=self.args.save_pdf,
                save_image=self.args.save_image,
                dpi=self.args.dpi,
                grayscale=self.args.gray,
            )
            if image is None:
                return None

        if self.args.save_var:
            local_ns[self.args.save_var] = str(self.tex_obj)

        return image
