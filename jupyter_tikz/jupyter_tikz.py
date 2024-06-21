from argparse import Namespace
import sys
import os
from subprocess import CalledProcessError, check_output
import tempfile
from typing import Literal
from IPython.core.magic import Magics, magics_class, line_cell_magic, needs_local_scope
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring
from IPython.display import SVG, Image
from string import Template
from textwrap import indent
from xml.dom import minidom
from hashlib import md5


IMPLICIT_PIC_TMPL = Template(
    r"""\documentclass{standalone}
$extras\begin{document}
	\begin{tikzpicture}
$src	\end{tikzpicture}
\end{document}"""
)

IMPLICIT_PIC_SCALE_TMPL = Template(
    r"""\documentclass{standalone}
$extras\begin{document}
	\begin{tikzpicture}
		\scalebox{$scale}{
$src		}
	\end{tikzpicture}
\end{document}"""
)

IMPLICIT_STANDALONE_TMPL = Template(
    r"""\documentclass{standalone}
$extras\begin{document}
$src
\end{document}"""
)

IMPLICIT_STANDALONE_SCALE_TMPL = Template(
    r"""\documentclass{standalone}
$extras\begin{document}
	\scalebox{$scale}{
$src	}
\end{document}"""
)


def build_tex_string(src: str, implicit_pic: bool, extras: str) -> str:
    """
    This function prepares a LaTeX string for rendering TikZ diagrams.
    Constructs a LaTeX string for TikZ diagrams, optionally wrapped in a TikZpicture environment.

    This function prepares a LaTeX string for rendering TikZ diagrams. It can either wrap the provided TikZ code in a TikZpicture environment or treat the code as standalone. Additional LaTeX commands can be included through the `extras` parameter.

    Parameters:
    - src (str): The TikZ code to be included in the LaTeX string. This code is either wrapped in a TikZpicture environment or left as is, based on the `implicit_pic` flag.
    - implicit_pic (bool): Determines whether the TikZ code should be wrapped in a TikZpicture environment. If True, the code is wrapped; if False, the code is treated as standalone latex class.
    - extras (str): Additional LaTeX commands to be included. These can be preamble commands or commands to be included within the document environment, depending on how the LaTeX string is being constructed.

    Returns:
    - str: A LaTeX string ready for compilation. This string includes the TikZ code (optionally wrapped in a TikZpicture environment) and any additional LaTeX commands specified in `extras`.
    """
    if implicit_pic:
        if len(src):
            src = indent(src.strip(), "\t\t") + "\n"
        return IMPLICIT_PIC_TMPL.substitute(src=src, extras=extras)
    else:
        if len(src):
            src = indent(src.strip(), "\t")
        return IMPLICIT_STANDALONE_TMPL.substitute(src=src, extras=extras)


def run_latex(
    src: str,
    rasterize: bool = False,
    tex_program: Literal["pdflatex", "xelatex", "lualatex"] = "pdflatex",
    dpi: int = 150,
    scale: float = 1,
    full_err: bool = False,
    pdftocairo_path: str = "pdftocairo",
) -> Image | SVG | None:
    current_dir = os.getcwd()  # get current working directory
    working_dir = os.path.join(tempfile.gettempdir(), "itikz")
    os.makedirs(working_dir, exist_ok=True)

    src_hash = md5(src.encode()).hexdigest()

    env = os.environ.copy()
    if "TEXINPUTS" in env:
        env["TEXINPUTS"] = os.path.join(current_dir, env["TEXINPUTS"])
    else:
        env["TEXINPUTS"] = current_dir  # add current directory to TEXINPUTS

    output_path = os.path.join(working_dir, src_hash)
    tex_path = f"{output_path}.tex"

    with open(tex_path, "w") as f:
        f.write(src)

    print("File written", tex_path)

    tex_filename = os.path.basename(tex_path)
    image_format = "svg" if not rasterize else "png"

    pdftocairo_command = [pdftocairo_path, f"-{image_format}"]
    if rasterize:
        pdftocairo_command.extend(["-singlefile", "-r", f"{dpi}"])
    pdftocairo_command.append(f"{output_path}.pdf")
    pdftocairo_command.append(f"{output_path}.svg" if not rasterize else output_path)

    try:
        check_output([tex_program, tex_filename], env=env, cwd=working_dir)
    except CalledProcessError as e:
        err_msg = e.output.decode()
        if not full_err:  # tail -n 20
            err_msg = "\n".join(err_msg.splitlines()[-20:])

        print(err_msg, file=sys.stderr)
        return None
    print("File compiled", tex_path)

    try:
        check_output(pdftocairo_command, cwd=working_dir)
    except CalledProcessError as e:
        err_msg = e.output.decode()
        if not full_err:  # tail -n 20
            err_msg = "\n".join(err_msg.splitlines()[-20:])

        print(err_msg, file=sys.stderr)
        return None

    image_path = f"{output_path}.{image_format}"
    if not rasterize:
        with open(image_path, "r") as f:
            image = f.read()
            if scale != 1.0:
                (doc,) = minidom.parseString(image).getElementsByTagName("svg")
                doc.setAttribute("style", f"transform: scale({scale});")
                return SVG(doc.toxml())
            else:
                return SVG(image)
    else:
        return Image(filename=image_path)


# The class MUST call this class decorator at creation time
@magics_class
class TikZMagics(Magics):
    args = Namespace()
    src = ""

    def build_template_extras(self):
        extras = []

        if self.args.latex_preamble:
            extras.append(self.args.latex_preamble)
        else:
            if not self.args.no_tikz:
                extras.append(r"\usepackage{tikz}")
            if self.args.tex_packages:
                extras.append(r"\usepackage{" + self.args.tex_packages + "}")
            if self.args.tikz_libraries:
                extras.append(r"\usetikzlibrary{" + self.args.tikz_libraries + "}")
            if self.args.pgfplots_libraries:
                extras.append(
                    r"\usepgfplotslibrary{" + self.args.pgfplots_libraries + "}"
                )
        if len(extras) > 0:
            extras = "\n".join(extras) + "\n"
        else:
            extras = ""
        return extras

    @line_cell_magic
    @magic_arguments()
    @argument(
        "-p",
        "--latex_preamble",
        dest="latex_preamble",
        default="",
        help='LaTeX preamble to insert before document, e.g., -x "$preamble", with preamble some IPython variable',
    )
    @argument(
        "-t",
        "--tex-packages",
        dest="tex_packages",
        default="",
        help='Comma separated list of tex packages, e.g., "-t amsfonts,amsmath"',
    )
    @argument(
        "-nt",
        "--no-tikz",
        dest="no_tikz",
        action="store_true",
        default=False,
        help="Do not import tikz package, useful when using other enviroments like pgfplots",
    )
    @argument(
        "-l",
        "--tikz-libraries",
        dest="tikz_libraries",
        default="",
        help='Comma separated list of tikz libraries, e.g., "-l arrows,automata"',
    )
    @argument(
        "-lp",
        "--pgfplots-libraries",
        dest="pgfplots_libraries",
        default="",
        help='Comman separated list of pgfplots libraries, e.g., "-lp groupplots,external"',
    )
    @argument(
        "-i",
        "--implicit-pic",
        dest="implicit_pic",
        action="store_true",
        default=False,
        help="Implicitly wrap the code in a standalone document with a tikzpicture environment",
    )
    @argument(
        "-f",
        "--full-document",
        dest="full_document",
        action="store_true",
        default=False,
        help="Use entire LaTeX document as input",
    )
    @argument(
        "-sc",
        "--scale",
        dest="scale",
        type=float,
        default=1.0,
        help='Scale the SVG output using CSS. Default is "--scale 1"',
    )
    @argument(
        "-r",
        "--rasterize",
        dest="rasterize",
        action="store_true",
        default=False,
        help="Output a rasterized image instead of SVG",
    )
    @argument(
        "-d",
        "--dpi",
        dest="dpi",
        type=int,
        default=150,
        help='DPI of rasterized output images. Default is "--dpi 150"',
    )
    @argument(
        "-e",
        "--full-err",
        dest="full_err",
        action="store_true",
        default=False,
        help="Show full error message",
    )
    @argument(
        "-tp",
        "--tex-program",
        dest="tex_program",
        default="pdflatex",
        help='TeX program to use for rendering, e.g., "-lp groupplots,external"',
    )
    @argument(
        "-ptc",
        "--pdftocairo-path",
        dest="pdftocairo_path",
        default="pdftocairo",
        help='PDF to Cairo command to use for rasterizing, e.g., "-pc path_to_pdftocairo.exe". Default is "-pc pdftocairo"',
    )
    @argument("code", nargs="?", help="the variable in IPython with the string source")
    @needs_local_scope
    def tikz(self, line, cell=None, local_ns=None) -> Image | SVG | None:
        r"""
        Renders a TikZ diagram in a Jupyter notebook cell. Works as both as %tikz and %%tikz.

        When used as %tikz, the code argument is required:
            In [1]: %tikz \draw (0,0) rectangle (1,1);


        As a cell, this will run a block of TikZ code:
            In [2]: %%tikz
                \draw (0,0) rectangle (1,1);

        Additional options can be passed to the magic command:
            In [3]: %%tikz --rasterize --dpi=1200 -l arrows,automata
                \draw (0,0) rectangle (1,1);
                \filldraw (0.5,0.5) circle (.1);
        """

        self.args = parse_argstring(self.tikz, line)
        self.src = cell

        if local_ns is None:
            local_ns = {}

        if cell is None:
            if self.args.code is None:
                print('Use "%tikz?" for help', file=sys.stderr)
                return

            if self.args.code not in local_ns:
                self.src = self.args.code
            else:
                self.src = local_ns[self.args.code]

        if self.args.implicit_pic and self.args.full_document:
            print(
                "Can't use --full-document and --implicit-pic together", file=sys.stderr
            )
            return None

        if self.args.latex_preamble and (
            self.args.tikz_libraries
            or self.args.tex_packages
            or self.args.pgfplots_libraries
        ):
            print(
                "Packages and libraries should be passed in the preamble or as arguments, not both",
                file=sys.stderr,
            )
            return None

        if not self.args.full_document:
            extras = self.build_template_extras()
            self.src = build_tex_string(self.src, self.args.implicit_pic, extras)

        print(self.src)

        image = run_latex(
            self.src,
            rasterize=self.args.rasterize,
            tex_program=self.args.tex_program,
            dpi=self.args.dpi,
            scale=self.args.scale,
            full_err=self.args.full_err,
            pdftocairo_path=self.args.pdftocairo_path,
        )

        if image is None:
            return None

        return image
