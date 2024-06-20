from argparse import Namespace
from IPython.core.magic import Magics, magics_class, line_cell_magic, needs_local_scope
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring
from string import Template


IMPLICIT_PIC_TMPL = Template(
    r"""\documentclass{standalone}
$extras
\begin{document}
\begin{tikzpicture}
$src
\end{tikzpicture}
\end{document}"""
)
IMPLICIT_PIC_SCALE_TMPL = Template(
    r"""\documentclass{standalone}
$extras
\begin{document}
\scalebox{$scale}{
\begin{tikzpicture}
$src
\end{tikzpicture}
}
\end{document}"""
)

IMPLICIT_STANDALONE_TMPL = Template(
    r"""\documentclass{standalone}
$extras
\begin{document}
$src
\end{document}"""
)
IMPLICIT_STANDALONE_SCALE_TMPL = Template(
    r"""\documentclass{standalone}
$extras
\begin{document}
\scalebox{$scale}{
$src
}
\end{document}"""
)


def build_tex_string(src: str, implicit_pic: bool, scale: float, extras: str):

    if scale != 1.0:
        if implicit_pic:
            return IMPLICIT_PIC_SCALE_TMPL.substitute(
                src=src, scale=scale, extras=extras
            )
        else:
            return IMPLICIT_STANDALONE_SCALE_TMPL.substitute(
                src=src, scale=scale, extras=extras
            )
    else:
        if implicit_pic:
            return IMPLICIT_PIC_TMPL.substitute(src=src, extras=extras)
        else:
            return IMPLICIT_STANDALONE_TMPL.substitute(src=src, extras=extras)


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
        extras = "\n".join(extras)
        return extras

    @line_cell_magic
    @magic_arguments()
    @argument(
        "-t",
        "--tex-packages",
        dest="tex_packages",
        default="",
        help='Comma separated list of tex packages, e.g., "-t amsfonts,amsmath"',
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
        "-p",
        "--latex_preamble",
        dest="latex_preamble",
        default="",
        help='LaTeX preamble to insert before document, e.g., -x "$preamble", with preamble some IPython variable.',
    )
    @argument(
        "-sc",
        "--scale",
        dest="scale",
        type=float,
        default=1.0,
        help='Scaling factor of pictures. Default is "--scale 1".',
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
        "-i",
        "--implicit-pic",
        dest="implicit_pic",
        action="store_true",
        default=False,
        help="Implicitly wrap the code in a standalone document with a tikzpicture environment.",
    )
    @argument(
        "-nt",
        "--no-tikz",
        dest="no_tikz",
        action="store_true",
        default=False,
        help="Do not import tikz package, useful when using other enviroments like pgfplots",
    )
    @argument("code", nargs="?", help="the variable in IPython with the string source")
    @needs_local_scope
    def tikz(self, line, cell=None, local_ns=None):
        """Magic that works both as %tikz and as %%tikz"""

        self.args = parse_argstring(self.tikz, line)
        self.src = cell

        if local_ns is None:
            local_ns = {}

        if cell is None:
            if self.args.code is None:
                raise ValueError("No code provided")

            if self.args.code not in local_ns:
                self.src = self.args.code
            else:
                self.src = local_ns[self.args.code]

        if self.args.implicit_pic and self.args.full_document:
            raise ValueError("Can't use --full-document and --implicit-pic together")

        if self.args.latex_preamble and (
            self.args.tikz_libraries
            or self.args.tex_packages
            or self.args.pgfplots_libraries
        ):
            raise ValueError(
                "Packages and libraries should be passed in the preamble or as arguments, not both."
            )

        if not self.args.full_document:
            extras = self.build_template_extras()
            self.src = build_tex_string(
                self.src, self.args.implicit_pic, self.args.scale, extras
            )

        print(self.args)
        print(local_ns)
        print(self.src)
