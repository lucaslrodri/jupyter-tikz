import os
import sys
import tempfile
from shutil import copy
from string import Template
from subprocess import CalledProcessError, check_output
from textwrap import indent
from typing import Literal, Union

from IPython.core.magic import Magics, line_cell_magic, magics_class, needs_local_scope
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring
from IPython.display import SVG, Image


def build_template_extras(
    no_tikz: bool = False,
    tex_packages: str = "",
    tikz_libraries: str = "",
    pgfplots_libraries: str = "",
) -> str:
    """
    This function constructs a LaTeX preamble string for TikZ diagrams, including any additional LaTeX packages or libraries specified.

    Args:
        no_tikz (bool, optional): A flag to indicate whether the TikZ package should be imported. If True, the TikZ package is not imported; if False, the TikZ package is imported. Default is False.
        tex_packages (str, optional): A comma-separated list of additional LaTeX packages to include. These packages are included in the preamble.
        tikz_libraries (str, optional): A comma-separated list of TikZ libraries to include. These libraries are included in the preamble.
        pgfplots_libraries (str, optional): A comma-separated list of PGFPlots libraries to include. These libraries are included in the preamble.

    Returns:
        str: A LaTeX preamble string that includes the specified packages and libraries, as well as the TikZ package if the `no_tikz` flag is not set.
    """
    extras = []

    if not no_tikz:
        extras.append(r"\usepackage{tikz}")
    if tex_packages:
        extras.append(r"\usepackage{" + tex_packages + "}")
    if tikz_libraries:
        extras.append(r"\usetikzlibrary{" + tikz_libraries + "}")
    if pgfplots_libraries:
        extras.append(r"\usepgfplotslibrary{" + pgfplots_libraries + "}")
    if len(extras) > 0:
        extras = "\n".join(extras) + "\n"
    else:
        extras = ""
    return extras


IMPLICIT_PIC_TMPL = Template(
    r"""\documentclass{standalone}
$extras\begin{document}
	\begin{tikzpicture}
$src	\end{tikzpicture}
\end{document}"""
)

IMPLICIT_PIC_SCALE_TMPL = Template(
    r"""\documentclass{standalone}
\usepackage{graphicx}
$extras\begin{document}
	\scalebox{$scale}{
	\begin{tikzpicture}
$src	\end{tikzpicture}
	}
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
\usepackage{graphicx}
$extras\begin{document}
	\scalebox{$scale}{
$src	}
\end{document}"""
)


def build_tex_string(
    src: str, implicit_pic: bool = False, extras: str = "", scale: float = 1
) -> str:
    """
    This function prepares a LaTeX string for rendering TikZ diagrams.

    It can either wrap the provided TikZ code in a TikZpicture environment or treat the code as standalone. Additional LaTeX commands can be included through the `extras` parameter.

    Args:
        src (str): The TikZ code to be included in the LaTeX string. This code is either wrapped in a TikZpicture environment or left as is, based on the `implicit_pic` flag.
        implicit_pic (bool, optional): Determines whether the TikZ code should be wrapped in a TikZpicture environment. If True, the code is wrapped; if False, the code is treated as standalone latex class. Default is False.
        extras (str, optional): Additional LaTeX commands to be included. These can be preamble commands or commands to be included within the document environment, depending on how the LaTeX string is being constructed.
        scale (float, optional): The scale factor to apply to the TikZ diagram. This factor is used to wrap the TikZ code in a \scalebox command. Default is 1.

    Returns:
        str: A LaTeX string ready for compilation. This string includes the TikZ code (optionally wrapped in a TikZpicture environment) and any additional LaTeX commands specified in `extras`.
    """
    if implicit_pic:
        if len(src):
            src = indent(src.strip(), "\t\t") + "\n"
        if scale == 1:
            return IMPLICIT_PIC_TMPL.substitute(src=src, extras=extras)
        else:
            return IMPLICIT_PIC_SCALE_TMPL.substitute(
                src=src, extras=extras, scale=scale
            )
    else:
        if len(src):
            src = indent(src.strip(), "\t")
            if scale != 1:
                src += "\n"
        if scale == 1:
            return IMPLICIT_STANDALONE_TMPL.substitute(src=src, extras=extras)
        else:
            return IMPLICIT_STANDALONE_SCALE_TMPL.substitute(
                src=src, extras=extras, scale=scale
            )


def render_jinja(src: str, ns: dict[str, str]) -> Union[str, None]:
    """
    Renders the Jinja template with the provided namespace.

    Args:
        src (str): The Jinja template source code.
        ns (dict): The namespace to use for rendering the template.
            Example: `locals()` or `globals()`.

    Returns:
        str | None: The rendered template, or None if jinja2 is not installed.
    """

    try:
        import jinja2
    except ImportError:  # pragma no cover
        print("Please install jinja2", file=sys.stderr)
        print("$ pip install jinja2", file=sys.stderr)
        return None

    fs_loader = jinja2.FileSystemLoader(os.getcwd())
    tmpl_env = jinja2.Environment(loader=fs_loader)
    tmpl = tmpl_env.from_string(src)

    return tmpl.render(**ns)


def save(
    src: str, dest: str, format: Literal["svg", "png", "code"] = "code"
) -> Union[str, None]:
    """
    Saves the source code or image to the specified destination path.

    Args:
        src (str): The source code or image path.
        dest (str): The destination path.

    Returns:
        str | None: The path to the saved file, or None if destination is None.
    """

    if dest is None:
        return None

    if os.environ.get("JUPYTER_TIKZ_SAVEDIR"):
        save_path = os.path.join(os.environ.get("JUPYTER_TIKZ_SAVEDIR"), dest)
    else:
        save_path = dest

    if format != "code" and (not save_path.endswith(f".{format}")):
        save_path += f".{format}"
    elif format == "code" and not (
        save_path.endswith(".tex")
        or save_path.endswith(".tikz")
        or save_path.endswith(".pgf")
        or save_path.endswith(".txt")
    ):
        save_path += ".tex"

    save_folder = os.path.dirname(save_path)
    if save_folder:
        os.makedirs(save_folder, exist_ok=True)

    if format == "code":
        with open(save_path, "w") as f:
            f.write(src)
    else:
        copy(src, save_path)
    return save_path


def run_latex(
    src: str,
    rasterize: bool = False,
    tex_program: Literal["pdflatex", "xelatex", "lualatex"] = "pdflatex",
    tex_args: str = "",
    dpi: int = 96,
    full_err: bool = False,
    save_image: str = None,
) -> Union[Image | SVG | None]:
    """
    This function compiles a LaTeX string containing TikZ code and returns an SVG or rasterized image.

    Parameters:

    - src (str): The LaTeX string containing the TikZ code to be compiled.
    - rasterize (bool, optional): A flag indicating whether the output should be rasterized. If True, the output is rasterized; if False, the output is an SVG image. Default is False.
    - tex_program (str, optional): The TeX program to use for rendering the TikZ code. This can be one of "pdflatex", "xelatex", or "lualatex". Default is "pdflatex".
    - tex_args (str, optional): Additional arguments to pass to the TeX program.
    - dpi (int, optional): The DPI (dots per inch) to use for rasterizing the output. This parameter is only used when `rasterize` is True. Default is 96.
    - full_err (bool, optional): A flag indicating whether the full error message should be displayed. If True, the full error message is displayed; if False, only the last 20 lines of the error message are displayed. Default is False.
    - save_image (str, optional): The path to save the output image. If None, the image is not saved to disk. Default is None.

    Returns:
    - Image | SVG | None: An Image (PNG) or SVG object representing the compiled TikZ diagram, or None if an error occurred during compilation.
    """
    current_dir = os.getcwd()  # get current working directory
    with tempfile.TemporaryDirectory() as working_dir:
        env = os.environ.copy()
        # TEXINPUTS is a environment variable that tells LaTeX where to look for files
        # https://tex.stackexchange.com/questions/410350/texinputs-on-windows
        if "TEXINPUTS" in env:
            env["TEXINPUTS"] = current_dir + os.pathsep + env["TEXINPUTS"]
        else:
            env["TEXINPUTS"] = "." + os.pathsep + current_dir + os.pathsep * 2
            # note that the trailing double pathsep will insert the standard
            # search path (otherwise we would lose access to all packages)
            # TEXINPUTS=.;C:\Users\joseph\Documents\LaTeX\local\\;

        output_path = os.path.join(working_dir, "tikz")
        tex_path = f"{output_path}.tex"

        with open(tex_path, "w") as f:
            f.write(src)

        tex_filename = os.path.basename(tex_path)

        tex_command = [tex_program]
        if tex_args:
            tex_command.extend(tex_args.split())
        tex_command.append(tex_filename)
        try:
            check_output(tex_command, env=env, cwd=working_dir)
        except CalledProcessError as e:
            err_msg = e.output.decode()
            if not full_err:  # tail -n 20
                err_msg = "\n".join(err_msg.splitlines()[-20:])

            print(err_msg, file=sys.stderr)
            return None

        image_format = "svg" if not rasterize else "png"

        if os.environ.get("JUPYTER_TIKZ_PDFTOCAIROPATH"):
            pdftocairo_path = os.environ.get("JUPYTER_TIKZ_PDFTOCAIROPATH")
        else:
            pdftocairo_path = "pdftocairo"

        pdftocairo_command = [pdftocairo_path, f"-{image_format}"]
        if rasterize:
            pdftocairo_command.extend(["-singlefile", "-transp", "-r", f"{dpi}"])
        pdftocairo_command.append(f"{output_path}.pdf")
        pdftocairo_command.append(
            f"{output_path}.svg" if not rasterize else output_path
        )
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
                if save_image:
                    save(image_path, save_image, format="svg")
                return SVG(image)
        else:
            if save_image:
                save(image_path, save_image, format="png")
            return Image(filename=image_path)


# The class MUST call this class decorator at creation time
@magics_class
class TikZMagics(Magics):
    @line_cell_magic
    @magic_arguments()
    @argument(
        "-p",
        "--latex_preamble",
        dest="latex_preamble",
        default="",
        help='LaTeX preamble to insert before the document, e.g., `-p="$preamble"`, with the preamble being an IPython variable.',
    )
    @argument(
        "-t",
        "--tex-packages",
        dest="tex_packages",
        default="",
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
        default="",
        help="Comma-separated list of TikZ libraries, e.g., `-l=arrows,automata`.",
    )
    @argument(
        "-lp",
        "--pgfplots-libraries",
        dest="pgfplots_libraries",
        default="",
        help="Comma-separated list of PGFPlots libraries, e.g., `-lp=groupplots,external`.",
    )
    @argument(
        "-i",
        "--implicit-pic",
        dest="implicit_pic",
        action="store_true",
        default=False,
        help="Implicitly wrap the code in a standalone document with a `tikzpicture` environment.",
    )
    @argument(
        "-f",
        "--full-document",
        dest="full_document",
        action="store_true",
        default=False,
        help="Use a full LaTeX document as input.",
    )
    @argument(
        "-j",
        "--as-jinja",
        dest="as_jinja",
        action="store_true",
        default=False,
        help="Render the input as a Jinja2 template.",
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
        "-sc",
        "--scale",
        dest="scale",
        type=float,
        default=1.0,
        help="The scale factor to apply to the TikZ diagram. Default is `-sc=1`.",
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
        help="DPI of the rasterized output image. Default is `-d=96`.",
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
        help="TeX program to use for rendering, e.g., `-tp=lualatex`.",
    )
    @argument(
        "-ta",
        "--tex-args",
        dest="tex_args",
        default="",
        help='Additional arguments to pass to the TeX program, e.g., `-ta="$tex_args_ipython_variable"`',
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
        help="Save the TikZ or TeX code to file, e.g., `-s filename.tikz`. Default is None.",
    )
    @argument(
        "-S",
        "--save-image",
        dest="save_image",
        type=str,
        default=None,
        help="Save the output image to file, e.g., `-S filename.svg`. Default is None.",
    )
    @argument(
        "-sv",
        "--save-var",
        dest="save_var",
        type=str,
        default=None,
        help="Save the TikZ or TeX code to an IPython variable, e.g., `-sv varname`. Default is None.",
    )
    @argument("code", nargs="?", help="the variable in IPython with the string source")
    @needs_local_scope
    def tikz(self, line, cell=None, local_ns=None) -> Union[Image, SVG, None]:
        r"""
        Renders a TikZ diagram in a Jupyter notebook cell. This function can be used as both a line magic (%tikz) and a cell magic (%%tikz).

        When used as cell magic, it executes the TeX/TikZ code within the cell:
            Example:
                In [3]: %%tikz
                        \begin{tikzpicture}
                            \draw (0,0) rectangle (1,1);
                        \end{tikzpicture}

        When used as line magic, the TeX/TikZ code is passed as an IPython string variable:
            Example:
                In [4]: %tikz "$ipython_string_variable_with_code"

        Additional options can be passed to the magic command to control the output:
            Example:
                In [5]: %%tikz -i --rasterize --dpi=1200 -l arrows,automata
                        \draw (0,0) rectangle (1,1);
                        \filldraw (0.5,0.5) circle (.1);
        """

        args = parse_argstring(self.tikz, line)
        src = cell

        if local_ns is None:
            local_ns = {}

        if cell is None:
            if args.code is None:
                print('Use "%tikz?" for help', file=sys.stderr)
                return

            if args.code not in local_ns:
                src = args.code
            else:
                src = local_ns[args.code]

            save_code = src
        else:
            save_code = cell

        if args.implicit_pic and args.full_document:
            print(
                "Can't use --full-document and --implicit-pic together", file=sys.stderr
            )
            return None

        if args.as_jinja:
            src = render_jinja(src, local_ns)
            save_code = src
            if args.print_jinja:
                print(src)

        if args.latex_preamble and (
            args.tikz_libraries or args.tex_packages or args.pgfplots_libraries
        ):
            print(
                "Packages and libraries should be passed in the preamble or as arguments, not both",
                file=sys.stderr,
            )
            return None

        if not args.full_document:
            if args.latex_preamble:
                extras = args.latex_preamble + "\n"
            else:
                extras = build_template_extras(
                    no_tikz=args.no_tikz,
                    tex_packages=args.tex_packages,
                    tikz_libraries=args.tikz_libraries,
                    pgfplots_libraries=args.pgfplots_libraries,
                )

            src = build_tex_string(
                src,
                implicit_pic=args.implicit_pic,
                extras=extras,
                scale=args.scale,
            )

        if args.no_compile:
            if save_code:
                if args.save_var:
                    local_ns[args.save_var] = save_code
                if args.save_tex:
                    save(save_code, args.save_tex, format="code")
            return None

        image = run_latex(
            src,
            rasterize=args.rasterize,
            tex_program=args.tex_program,
            dpi=args.dpi,
            full_err=args.full_err,
            save_image=args.save_image,
        )

        if image is None:
            return None

        if save_code:
            if args.save_var:
                local_ns[args.save_var] = save_code
            if args.save_tex:
                save(save_code, args.save_tex, format="code")

        return image
