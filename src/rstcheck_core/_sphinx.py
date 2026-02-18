"""Sphinx helper functions."""

from __future__ import annotations

import logging
import pathlib
import tempfile

from . import _docutils, _extras

if _extras.SPHINX_INSTALLED:
    import sphinx.application
    import sphinx.domains.c
    import sphinx.domains.cpp
    import sphinx.domains.javascript
    import sphinx.domains.python
    import sphinx.domains.std
    import sphinx.util.docutils


logger = logging.getLogger(__name__)

def setup_app(srcdir: pathlib.Path | None) -> sphinx.application.Sphinx | None:
    """Setup a sphinx application for the given srcdir
    """
    if _extras.SPHINX_INSTALLED:
        logger.debug("Create dummy sphinx application.")
        with tempfile.TemporaryDirectory() as temp_dir:
            outdir = pathlib.Path(temp_dir) / "_build"
            new_srcdir = temp_dir
            if srcdir:
                new_srcdir = srcdir.absolute()
            return sphinx.application.Sphinx(
                srcdir=str(new_srcdir),
                confdir=None,
                status=None,
                outdir=str(outdir),
                doctreedir=str(outdir),
                buildername="dummy",
            )
    return None
