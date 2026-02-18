"""Checking functionality."""

from __future__ import annotations

import logging
import pathlib

from multiprocessing import Process, Pipe

from . import config, types


logger = logging.getLogger(__name__)


def _mp_check_file(
    pipe: Pipe,
    *args,
) -> list[types.LintError]:
    """Isolation function for check_file
    """
    from . import _fork_checker
    pipe.send(_fork_checker.check_file(*args))


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
    from . import _fork_checker
    _fork_checker.check_file(source_file, rstcheck_config, overwrite_with_file_config)


def _mp_check_source(
    pipe: Pipe,
    *args,
) -> list[types.LintError]:
    """Isolation function for check_file
    """
    from . import _fork_checker
    pipe.send(_fork_checker.check_source(*args))


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
    rec, snd = Pipe(duplex=False)
    p = Process(target=check_source,
        args=(
            snd, source, source_file, ignores, report_level, warn_unknown_settings
        )
                )
    p.start()
    p.join()
    if p.exitcode == 0:
        return rec.recv()

    raise AssertionError("Process didn't exit cleanly")
