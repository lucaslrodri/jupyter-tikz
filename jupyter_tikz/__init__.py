__author__ = """Lucas Lima Rodrigues"""
__email__ = "lucaslrodri@gmail.com"
__version__ = "0.1.0"

from .jupyter_tikz import *


def load_ipython_extension(ipython):  # pragma: no cover
    ipython.register_magics(TikZMagics)
