import subprocess
from IPython import display
from typing import Literal, Optional
from IPython.core.magic import Magics, line_cell_magic, magics_class, needs_local_scope
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring
import sys
import os
import tempfile
from string import Template
from pathlib import Path
from shutil import copy


class TexDocument:
    def __init__(self, code: str, as_jinja=False, ns: dict[str, str] = None):
        self.code = code
        self.as_jinja = as_jinja
        self.ns = ns

        if self.as_jinja:
            self._render_jinja()
        self._build_tex_str()

    def _build_tex_str(self) -> str:
        self.latex_str = self.code

    def __repr__(self) -> str:
        self.__str__()

    def __str__(self) -> str:
        return self.code

    def _modify_texinputs(self, current_dir: str) -> str:
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
        self, dest: str, src: str = None, format: Literal["svg", "png", "code"] = "code"
    ):
        if dest is None:
            return None

        if format not in ["svg", "png", "code"]:
            raise ValueError(
                f"`{format}` is not a valid format. Valid formats are `svg`, `png`, and `code`."
            )

        dest_path = Path(dest)

        if os.environ.get("JUPYTER_TIKZ_SAVEDIR"):
            dest_path = os.environ.get("JUPYTER_TIKZ_SAVEDIR") / dest_path
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
                src = self.code
            dest_path.write_text(src)
        else:
            src_path = Path(src).resolve()
            copy(src_path, dest_path)
        return f"{dest_path}"

    def run_latex(
        self,
        tex_program: str = "pdflatex",
        tex_args: str = "",
        rasterize: bool = False,
        full_err: bool = False,
        save_image: str = None,
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

    def _render_jinja(self) -> None:
        try:
            import jinja2
        except ImportError:  # pragma no cover
            print("Please install jinja2", file=sys.stderr)
            print("$ pip install jinja2", file=sys.stderr)
            return

        fs_loader = jinja2.FileSystemLoader(os.getcwd())
        tmpl_env = jinja2.Environment(loader=fs_loader)

        tmpl = tmpl_env.from_string(self.code)
        ns = locals() if self.ns is None else self.ns

        self.code = tmpl.render(**ns)


class StandaloneDocument(TexDocument):
    TMPL = Template(
        "\\documentclass{standalone}\n"
        + "\\usepackage{tikz}\n"
        + "$extras"
        + "\\begin{document}\n"
        + "\t$tikzpicture\n"
        + "\\end{document}"
    )
    TMPL_SCALE = Template(
        "\\documentclass{standalone}\n"
        + "\\usepackage{graphicx}\n"
        + "\\usepackage{tikz}\n"
        + "$extras"
        + "\\begin{document}\n"
        + "\t\\scalebox{$scale}{\n"
        + "\t$tikzpicture\n"
        + "\t}\n"
        + "\\end{document}"
    )


class Tikzpicture(StandaloneDocument):
    TMPL = Template(
        "\\documentclass{standalone}\n"
        + "$extras"
        + "\\begin{document}\n"
        + "\t\begin{tikzpicture}\n"
        + "$src"
        + "\t\\end{tikzpicture}\n"
        + "\\end{document}"
    )
    TMPL_SCALE = Template(
        "\\documentclass{standalone}\n"
        + "$extras"
        + "\\begin{document}\n"
        + "\t\scalebox{$scale}{\n"
        + "\t\begin{tikzpicture}\n"
        + "$src"
        + "\t\\end{tikzpicture}\n"
        + "\t}\n"
        + "\\end{document}"
    )


# as "full-document", "standalone-document", "tikzpicture"


@magics_class
class TikZMagics(Magics):
    def get_input_type(self, input_type: str) -> Optional[str]:
        VALID_INPUT_TYPES = ["full-document", "standalone-document", "tikzpicture"]
        input_type = input_type.lower()
        input_type_len = len(input_type)

        for index, valid_input_type in enumerate(VALID_INPUT_TYPES):
            if input_type == valid_input_type[:input_type_len]:
                return VALID_INPUT_TYPES[index]

        return None

    @line_cell_magic
    @magic_arguments()
    @argument(
        "-as",
        "--input-type",
        dest="input_type",
        default="standalone",
        help="Input type. Possible values are: `full-document`, `standalone-document`, `tikzpicture`. Default is `standalone-document`.",
    )
    @argument("code", nargs="?", help="the variable in IPython with the Tex/TikZ code")
    @needs_local_scope
    def tikz(
        self, line, cell=None, local_ns=None
    ) -> Optional[display.Image | display.SVG]:

        args = parse_argstring(self.tikz, line)
        self.src = cell
        local_ns = local_ns or {}

        input_type = self.get_input_type(args.input_type)

        if input_type is None:
            print(
                f"`{args.input_type}` is not a valid input type.",
                "Valid input types are `full-document`, `standalone-document`, or `tikzpicture`.",
                file=sys.stderr,
            )
            return

        if cell is None:
            if args.code is None:
                print('Use "%tikz?" for help', file=sys.stderr)
                return

            if args.code not in local_ns:
                self.src = args.code
            else:
                self.src = local_ns[args.code]

        if input_type == "full-document":
            self.tex_obj = TexDocument(self.src)
        elif input_type == "standalone-document":
            self.tex_obj = StandaloneDocument(self.src)
        elif input_type == "tikzpicture":
            self.tex_obj = Tikzpicture(self.src)
