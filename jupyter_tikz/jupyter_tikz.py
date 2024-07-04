import os
import subprocess
import sys
import tempfile
from pathlib import Path
from shutil import copy
from string import Template
from textwrap import indent
from typing import Any, Literal, Optional

from IPython import display
from IPython.core.magic import Magics, line_cell_magic, magics_class, needs_local_scope
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring

_EXTRAS_CONFLITS_ERR = "You cannot provide `preamble` and (`tex_packages`, `tikz_libraries`, and/or `pgfplots_libraries`) at the same time."
_PRINT_CONFLICT_ERR = (
    "You cannot use `--print-jinja` and `--print-tex` at the same time."
)
_JINJA_NOT_INTALLED_ERR = (
    "Template cannot be rendered. Please install jinja2: `$ pip install jinja2`"
)
_NS_NOT_PROVIDED_ERR = 'Namespace must be provided when using `use_jinja`, i.e.: `ns=locals()` or `ns={"my_var": value}`'
_DEPRECATED_I_ERR = (
    "Deprecated: Do not use `--implicit-pic`. Use `-as=tikzpicture` instead."
)
_DEPRECATED_F_ERR = (
    "Deprecated: Do not use `--full-document`. Use `-as=full-document` instead."
)
_DEPRECATED_I_AND_F_ERR = (
    "Deprecated: Do not use `-i` or `-f`. Use `-as=<input_type>` instead."
)
_DEPRECATED_ASJINJA_ERR = (
    "Deprecated: Do not use `--as-jinja`. Use `--use-jinja` instead."
)


class TexDocument:
    def __init__(
        self, code: str, use_jinja: bool = False, ns: Optional[dict[str, Any]] = None
    ):
        self._code = code.strip()
        self.use_jinja = use_jinja
        if self.use_jinja and not ns:
            raise ValueError(_NS_NOT_PROVIDED_ERR)

        if self.use_jinja:
            self._render_jinja(ns)
        self._build_latex_str()

    def _build_latex_str(self) -> None:
        self.latex_str = self._code

    @staticmethod
    def _arg_head(arg, limit=60) -> str:
        if type(arg) == str:
            arg = arg.strip()
            arg = f"{arg[:limit]}..." if len(arg) > limit else arg
            arg = str(repr(arg.strip()))
        else:
            arg = str(arg)
        return arg

    def __repr__(self) -> str:
        params_dict = self.__dict__
        if "scale" in params_dict.keys():
            if params_dict["scale"] == 1.0:
                del params_dict["scale"]

        params = ", ".join(
            [
                f"{k}={self._arg_head(v)}"
                for k, v in params_dict.items()
                if k not in ["_code", "latex_str", "ns"] and v
            ]
        )
        if params:
            params = ", " + params
        return f"{self.__class__.__name__}({self._arg_head(self._code)}{params})"

    def __str__(self) -> str:
        return self._code

    @staticmethod
    def _modify_texinputs(current_dir: str) -> dict[str, str]:
        env = os.environ.copy()
        # TEXINPUTS is a environment variable that tells LaTeX where to look for files
        # https://tex.stackexchange.com/questions/410350/texinputs-on-windows
        if "TEXINPUTS" in env:
            env["TEXINPUTS"] = current_dir + os.pathsep + env["TEXINPUTS"]
        else:
            env["TEXINPUTS"] = "." + os.pathsep + current_dir + os.pathsep * 2
            # note that the trailing double pathsep will insert the standard
            # search path (otherwise we would lose access to all packages)
            # TEXINPUTS=.;C:\Users\user\Documents\LaTeX\local\\;

        return env

    def _run_command(
        self, command: str, working_dir: str, full_err: bool = False, **kwargs
    ) -> int:

        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            check=False,
            cwd=working_dir,
            **kwargs,
        )
        if result.returncode != 0:
            err_msg = result.stderr if result.stderr else result.stdout
            if not full_err:  # tail -n 20
                err_msg = "\n".join(err_msg.splitlines()[-20:])
            print(err_msg, file=sys.stderr)
        return result.returncode

    def save(
        self,
        dest: str,
        src: Optional[str] = None,
        format: Literal["svg", "png", "code"] = "code",
    ) -> Optional[str]:
        if dest is None:
            return None

        if format not in ["svg", "png", "code"]:
            raise ValueError(
                f"`{format}` is not a valid format. Valid formats are `svg`, `png`, and `code`."
            )

        if format != "code" and src is None:
            raise ValueError("src must be provided when format is not code.")

        dest_path = Path(dest)

        if os.environ.get("JUPYTER_TIKZ_SAVEDIR"):
            dest_path = str(os.environ.get("JUPYTER_TIKZ_SAVEDIR")) / dest_path
        else:
            dest_path = dest_path

        dest_path = dest_path.resolve()

        if format == "svg" and (dest_path.suffix != ".svg"):
            dest_path = dest_path.with_suffix(dest_path.suffix + ".svg")
        elif format == "png" and (dest_path.suffix != ".png"):
            dest_path = dest_path.with_suffix(dest_path.suffix + ".png")
        elif format == "code" and (not dest_path.suffix):
            dest_path = dest_path.with_suffix(".tex")

        dest_path.parent.mkdir(parents=True, exist_ok=True)

        if format == "code":
            if src is None:
                src = self._code
            dest_path.write_text(src)
        else:
            if src is not None:
                src_path = Path(src).resolve()
                copy(src_path, dest_path)
        return f"{dest_path}"

    def run_latex(
        self,
        tex_program: str = "pdflatex",
        tex_args: Optional[str] = None,
        rasterize: bool = False,
        full_err: bool = False,
        save_image: Optional[str] = None,
        dpi: int = 96,
    ) -> Optional[display.Image | display.SVG]:
        current_dir = os.getcwd()  # get current working directory

        with tempfile.TemporaryDirectory() as working_dir:
            tex_path = Path(working_dir) / "tikz.tex"

            env = self._modify_texinputs(current_dir)
            output_stem = tex_path.parent.resolve() / tex_path.stem

            tex_path.write_text(self.latex_str, encoding="utf-8")

            tex_command = tex_program
            if tex_args:
                tex_command += f" {tex_args}"
            tex_command += f" {tex_path.resolve()}"

            res = self._run_command(tex_command, working_dir, full_err, env=env)
            if res != 0:
                return None

            image_format = "svg" if not rasterize else "png"

            if os.environ.get("JUPYTER_TIKZ_PDFTOCAIROPATH"):
                pdftocairo_path = os.environ.get("JUPYTER_TIKZ_PDFTOCAIROPATH")
            else:
                pdftocairo_path = "pdftocairo"

            pdftocairo_command = f"{pdftocairo_path} -{image_format}"
            if rasterize:
                pdftocairo_command += f" -singlefile -transp -r {dpi}"

            pdftocairo_command += f" {output_stem}.pdf"
            pdftocairo_command += (
                f" {output_stem}.svg" if not rasterize else f" {output_stem}"
            )
            res = self._run_command(pdftocairo_command, working_dir, full_err)
            if res != 0:
                return None

            if not rasterize:
                if save_image:
                    self.save(save_image, f"{output_stem}.svg", "svg")
                return display.SVG(f"{output_stem}.svg")
            else:
                if save_image:
                    self.save(save_image, f"{output_stem}.png", "png")
                return display.Image(f"{output_stem}.png")

    def _render_jinja(self, ns) -> None:
        try:
            import jinja2
        except ImportError:
            raise ImportError(_JINJA_NOT_INTALLED_ERR)

        fs_loader = jinja2.FileSystemLoader(os.getcwd())
        tmpl_env = jinja2.Environment(loader=fs_loader)

        tmpl = tmpl_env.from_string(self._code)

        self._code = tmpl.render(**ns)


class TexTemplate(TexDocument):
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
        preamble: Optional[str] = None,
        tex_packages: Optional[str] = None,
        tikz_libraries: Optional[str] = None,
        pgfplots_libraries: Optional[str] = None,
        no_tikz: bool = False,
        **kargs,
    ):
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
        tex_packages: Optional[str] = None,
        tikz_libraries: Optional[str] = None,
        pgfplots_libraries: Optional[str] = None,
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

    def _build_latex_str(self) -> None:
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

        self.latex_str = self.TMPL.substitute(
            preamble=self.preamble,
            scale_begin=scale_begin,
            tikzpicture_begin=tikzpicture_begin,
            code=code,
            tikzpicture_end=tikzpicture_end,
            scale_end=scale_end,
        )


@magics_class
class TikZMagics(Magics):
    def _get_input_type(self, input_type: str) -> Optional[str]:
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
    @argument(  # New
        "-as",
        "--input-type",
        dest="input_type",
        default="standalone",
        help="Type of the input. Possible values are: `full-document`, `standalone-document`, `tikzpicture`. Defaults to `standalone-document`.",
    )
    @argument(  # Deprecated
        "-i",
        "--implicit-pic",
        dest="implicit_pic",
        action="store_true",
        default=False,
        help="Deprecated. Use `-as=tikzpicture` instead.",
    )
    @argument(  # Deprecated
        "-f",
        "--full-document",
        dest="full_document",
        action="store_true",
        default=False,
        help="Deprecated. Use `-as=full-document` instead.",
    )
    @argument(
        "-p",
        "--latex_preamble",
        dest="latex_preamble",
        default=None,
        help='LaTeX preamble to insert before the document, e.g., `-p="$preamble"`, with the preamble being an IPython variable.',
    )
    @argument(
        "-t",
        "--tex-packages",
        dest="tex_packages",
        default=None,
        help="Comma-separated list of TeX packages, e.g., `-t=amsfonts,amsmath`.",
    )
    @argument(
        "-nt",
        "--no-tikz",
        dest="no_tikz",
        action="store_true",
        default=False,
        help="Force to not import the TikZ package.",
    )
    @argument(
        "-l",
        "--tikz-libraries",
        dest="tikz_libraries",
        default=None,
        help="Comma-separated list of TikZ libraries, e.g., `-l=arrows,automata`.",
    )
    @argument(
        "-lp",
        "--pgfplots-libraries",
        dest="pgfplots_libraries",
        default=None,
        help="Comma-separated list of PGFPlots libraries, e.g., `-lp=groupplots,external`.",
    )
    @argument(  # New
        "-j",
        "--use-jinja",
        dest="use_jinja",
        action="store_true",
        default=False,
        help="Render the input using Jinja2.",
    )
    @argument(  # Deprecated
        "--as-jinja",
        dest="as_jinja",
        action="store_true",
        default=False,
        help="Deprecated. Use `--use-jinja` instead.",
    )
    @argument(
        "-pj",
        "--print-jinja",
        dest="print_jinja",
        action="store_true",
        default=False,
        help="Print the rendered Jinja2 template.",
    )
    @argument(
        "-pt",
        "--print-tex",
        dest="print_tex",
        action="store_true",
        default=False,
        help="Print full LaTeX document.",
    )
    @argument(
        "-sc",
        "--scale",
        dest="scale",
        type=float,
        default=1.0,
        help="The scale factor to apply to the TikZ diagram. Defaults to `-sc=1`.",
    )
    @argument(
        "-r",
        "--rasterize",
        dest="rasterize",
        action="store_true",
        default=False,
        help="Output a rasterized image (PNG) instead of SVG.",
    )
    @argument(
        "-d",
        "--dpi",
        dest="dpi",
        type=int,
        default=96,
        help="DPI of the rasterized output image. Defaults to `-d=96`.",
    )
    @argument(
        "-e",
        "--full-err",
        dest="full_err",
        action="store_true",
        default=False,
        help="Show full error message.",
    )
    @argument(
        "-tp",
        "--tex-program",
        dest="tex_program",
        default="pdflatex",
        help="TeX program to use for rendering, e.g., `-tp=lualatex`.",
    )
    @argument(
        "-ta",
        "--tex-args",
        dest="tex_args",
        default=None,
        help='Additional arguments to pass to the TeX program, e.g., `-ta="$tex_args_ipython_variable"`.',
    )
    @argument(
        "-nc",
        "--no-compile",
        dest="no_compile",
        action="store_true",
        default=False,
        help="Do not compile the LaTeX code.",
    )
    @argument(
        "-s",
        "--save-tex",
        dest="save_tex",
        type=str,
        default=None,
        help="Save the TikZ or LaTeX code to file, e.g., `-s filename.tikz`.",
    )
    @argument(
        "-S",
        "--save-image",
        dest="save_image",
        type=str,
        default=None,
        help="Save the output image to file, e.g., `-S filename.svg`.",
    )
    @argument(
        "-sv",
        "--save-var",
        dest="save_var",
        type=str,
        default=None,
        help="Save the TikZ or LaTeX code to an IPython variable, e.g., `-sv varname`.",
    )
    @argument("code", nargs="?", help="the variable in IPython with the Tex/TikZ code")
    @needs_local_scope
    def tikz(
        self, line, cell: Optional[str] = None, local_ns=None
    ) -> Optional[display.Image | display.SVG]:

        args = parse_argstring(self.tikz, line)

        if args.latex_preamble and (
            args.tex_packages or args.tikz_libraries or args.pgfplots_libraries
        ):
            print(_EXTRAS_CONFLITS_ERR, file=sys.stderr)
            return

        if args.implicit_pic and not args.full_document:
            print(
                _DEPRECATED_I_ERR,
                file=sys.stderr,
            )
            return
        elif args.full_document and not args.implicit_pic:
            print(
                _DEPRECATED_F_ERR,
                file=sys.stderr,
            )
            return
        elif args.implicit_pic or args.full_document:
            print(
                _DEPRECATED_I_AND_F_ERR,
                file=sys.stderr,
            )
            return
        if args.as_jinja:
            print(
                _DEPRECATED_ASJINJA_ERR,
                file=sys.stderr,
            )
            return
        if args.print_jinja and args.print_tex:
            print(
                _PRINT_CONFLICT_ERR,
                file=sys.stderr,
            )
            return

        self.input_type = self._get_input_type(args.input_type)
        if self.input_type is None:
            print(
                f"`{args.input_type}` is not a valid input type.",
                "Valid input types are `full-document`, `standalone-document`, or `tikzpicture`.",
                file=sys.stderr,
            )
            return

        self.src = cell or ""
        local_ns = local_ns or {}

        if cell is None:
            if args.code is None:
                print('Use "%tikz?" for help', file=sys.stderr)
                return

            if args.code not in local_ns:
                self.src: str = args.code
            else:
                self.src: str = local_ns[args.code]

        if self.input_type == "full-document":
            self.tex_obj = TexDocument(self.src, use_jinja=args.use_jinja, ns=local_ns)
        else:
            implicit_tikzpicture = self.input_type == "tikzpicture"
            self.tex_obj = TexTemplate(
                self.src,
                implicit_tikzpicture=implicit_tikzpicture,
                preamble=args.latex_preamble,
                tex_packages=args.tex_packages,
                no_tikz=args.no_tikz,
                tikz_libraries=args.tikz_libraries,
                pgfplots_libraries=args.pgfplots_libraries,
                scale=args.scale,
                use_jinja=args.use_jinja or args.print_jinja,
                ns=local_ns,
            )

        if args.print_jinja:
            print(self.tex_obj)
        if args.print_tex:
            print(self.tex_obj.latex_str)

        image = None
        if not args.no_compile:
            image = self.tex_obj.run_latex(
                tex_program=args.tex_program,
                tex_args=args.tex_args,
                rasterize=args.rasterize,
                full_err=args.full_err,
                save_image=args.save_image,
                dpi=args.dpi,
            )
            if image is None:
                return None

        if args.save_var:
            local_ns[args.save_var] = str(self.tex_obj)

        if args.save_tex:
            self.saved_path = self.tex_obj.save(args.save_tex, format="code")

        return image
