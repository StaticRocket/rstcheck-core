"""Checking functionality."""

from __future__ import annotations

import os
import logging
import pathlib

from . import config, types, _fork_checker


logger = logging.getLogger(__name__)


def check_file(
    source_file: pathlib.Path,
    rstcheck_config: config.RstcheckConfig,
    overwrite_with_file_config: bool = True,  # noqa: FBT001,FBT002
) -> list[types.LintError]:
    """Check the given file for issues.

    On every call docutils' caches for roles and directives are cleared by reloading their modules.

    :param source_file: Path to file to check
    :param rstcheck_config: Main configuration of the application
    :param overwrite_with_file_config: If the loaded file config should overwrite the
        ``rstcheck_config``;
        defaults to :py:obj:`True`
    :return: A list of found issues
    """
    pid = os.fork()
    if pid == 0:
        from . import _fork_checker
        _fork_checker.check_file(source_file, rstcheck_config, overwrite_with_file_config)
        os._exit(0)
    else:
        os.waitpid(pid, 0)



def check_source(
    source: str,
    source_file: types.SourceFileOrString | None = None,
    ignores: types.IgnoreDict | None = None,
    report_level: config.ReportLevel = config.DEFAULT_REPORT_LEVEL,
    *,
    warn_unknown_settings: bool = False,
) -> types.YieldedLintError:
    """Check the given rst source for issues.

    :param source_file: Path to file the source comes from if it comes from a file;
        defaults to :py:obj:`None`
    :param ignores: Ignore information; defaults to :py:obj:`None`
    :param report_level: Report level; defaults to
        :py:data:`rstcheck_core.config.DEFAULT_REPORT_LEVEL`
    :param warn_unknown_settings: If a warning should be logged for unknown settings in config file;
        defaults to :py:obj:`False`
    :return: :py:obj:`None`
    :yield: Found issues
    """
    pid = os.fork()
    if pid == 0:
        from . import _fork_checker
        _fork_checker.check_source(
            source, source_file, ignores, report_level, warn_unknown_settings
        )
        os._exit(0)
    else:
        os.waitpid(pid, 0)
