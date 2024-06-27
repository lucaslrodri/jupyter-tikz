from IPython.display import SVG, Image
from typing import Union, Optional
from IPython.core.magic import Magics, line_cell_magic, magics_class, needs_local_scope
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring
import sys
import os
import tempfile


class TexDocument:
    def __init__(self, code: str):
        self.code = code
        self._src = self.code

    def __repr__(self) -> str:
        self.__str__()

    def __str__(self) -> str:
        return self.code

    def run_latex(self) -> Image | SVG:
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
                # TEXINPUTS=.;C:\Users\user\Documents\LaTeX\local\\;


class TemplateDocument(TexDocument): ...


class StandaloneDocument(TemplateDocument): ...


class Tikzpicture(TemplateDocument): ...


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
        help="Input type. Possible values are: 'full-document', 'standalone-document', 'tikzpicture'. Default is 'standalone-document'.",
    )
    @argument("code", nargs="?", help="the variable in IPython with the Tex/TikZ code")
    @needs_local_scope
    def tikz(self, line, cell=None, local_ns=None) -> Optional[Image | SVG]:

        args = parse_argstring(self.tikz, line)
        self._src = cell
        local_ns = local_ns or {}

        input_type = self.get_input_type(args.input_type)

        if input_type is None:
            print(
                f"'{args.input_type}' is not a valid input type.",
                "Valid input types are 'full-document', 'standalone-document', or 'tikzpicture'.",
                file=sys.stderr,
            )
            return

        if cell is None:
            if args.code is None:
                print('Use "%tikz?" for help', file=sys.stderr)
                return

            if args.code not in local_ns:
                self._src = args.code
            else:
                self._src = local_ns[args.code]

        if input_type == "full-document":
            self._tex = TexDocument(self._src)
        elif input_type == "standalone-document":
            self._tex = StandaloneDocument(self._src)
        elif input_type == "tikzpicture":
            self._tex = Tikzpicture(self._src)
