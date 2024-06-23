from jupyter_tikz.jupyter_tikz import build_template_extras


def test_build_template_extras_no_params():
    res = build_template_extras()
    expected_res = "\\usepackage{tikz}\n"

    assert res == expected_res


def test_build_template_extras_no_extras_no_tikz():
    no_tikz = True

    res = build_template_extras(no_tikz=no_tikz)
    expected_res = ""

    assert res == expected_res


def test_build_template_extras_with_packages():
    tex_packages = "a,b"

    res = build_template_extras(tex_packages=tex_packages)
    expected_res = "\\usepackage{tikz}\n\\usepackage{a,b}\n"

    assert res == expected_res


def test_build_template_extras_with_packages_no_tikz():
    tex_packages = "a,b"
    no_tikz = True

    res = build_template_extras(tex_packages=tex_packages, no_tikz=no_tikz)
    expected_res = "\\usepackage{a,b}\n"

    assert res == expected_res


def test_build_template_extras_with_packages_and_libraries():
    tex_packages = "a,b"
    tiz_libraries = "c,d"

    res = build_template_extras(tex_packages=tex_packages, tikz_libraries=tiz_libraries)
    expected_res = "\\usepackage{tikz}\n\\usepackage{a,b}\n\\usetikzlibrary{c,d}\n"

    assert res == expected_res


def test_build_template_extras_with_packages_libraries_and_pgfplots_libraries():
    tex_packages = "a,b"
    tiz_libraries = "c,d"
    pgfplots_libraries = "e,f"

    res = build_template_extras(
        tex_packages=tex_packages,
        tikz_libraries=tiz_libraries,
        pgfplots_libraries=pgfplots_libraries,
    )
    expected_res = "\\usepackage{tikz}\n\\usepackage{a,b}\n\\usetikzlibrary{c,d}\n\\usepgfplotslibrary{e,f}\n"

    assert res == expected_res
