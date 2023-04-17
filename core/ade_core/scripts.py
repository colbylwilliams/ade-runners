#!/usr/bin/env python3

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import os
import shutil
import stat
import subprocess

from pathlib import Path
from typing import Union

from .logger import error_exit, get_logger

log = get_logger(__name__)


def _ensure_dir_path(path: Union[str, Path]) -> Path:
    '''Ensure the directory exists and is a directory'''
    dir_path = (path if isinstance(path, Path) else Path(path)).resolve()
    if not dir_path.is_dir():
        error_exit(log, f'{dir_path} does not exist or is not a directory')
    return dir_path


def _ensure_file_path(path: Union[str, Path]) -> Path:
    '''Ensure the file exists and is a file'''
    file_path = (path if isinstance(path, Path) else Path(path)).resolve()
    if not file_path.is_file():
        error_exit(log, f'{file_path} does not exist or is not a file')
    return file_path


def run(path: Union[str, Path], cwd: Union[str, Path, None] = None):
    '''Runs a python or bash script'''
    log.info('')
    log.info(f'Executing {path}')

    file_path = _ensure_file_path(path)

    if file_path.suffix == '.sh':
        # resolve the full path to sh. e.g. /bin/sh
        sh = shutil.which('sh')
        args = [sh, str(file_path)]
    elif file_path.suffix == '.py':
        # resolve the full path to python3
        p3 = shutil.which('python3')
        args = [p3, str(file_path)]
    else:
        error_exit(log, f'Unsupported script type: {file_path.suffix}')

    if not os.access(file_path, os.X_OK):
        log.info(f'{file_path} is not executable, setting executable bit')
        file_path.chmod(file_path.stat().st_mode | stat.S_IEXEC)

    try:
        log.info(' '.join(args))
        proc = subprocess.run(args, cwd=cwd, capture_output=True, check=True, text=True)
        if proc.stdout:
            for line in proc.stdout.splitlines():
                log.info(line)
        if proc.stderr:
            error_exit(log, f'\n\n{proc.stderr}')
    except subprocess.CalledProcessError as e:
        error_exit(log, f'Error executing {path} {e.stderr if e.stderr else e.stdout}')


def run_all(path: Union[str, Path], cwd: Union[str, Path, None] = None) -> int:
    '''Runs all python and bash scripts in a directory in ascending alphabetical order.'''

    dir_path = _ensure_dir_path(path)

    scripts = sorted(list(dir_path.glob('*.sh')) + list(dir_path.glob('*.py')))

    if scripts:
        log.info(f'Found {len(scripts)} scripts')

        for script in scripts:
            log.info(f' {script}')
        for script in scripts:
            run(script, cwd)

    return len(scripts)


def get_action_script(path: Union[str, Path], action: str) -> Path:
    '''Looks for python or bash script in the directory'''
    log.info('')
    log.info(f'Checking for action scripts in {path}...')

    dir_path = _ensure_dir_path(path)

    sh_path = dir_path / f'{action}.sh'
    py_path = dir_path / f'{action}.py'

    sh_isfile = sh_path.is_file()
    py_isfile = py_path.is_file()

    if sh_isfile or py_isfile:
        if sh_isfile and py_isfile:
            error_exit(log, f'Found both {action}.sh and {action}.py in {path}. Only one script file allowed.')

        action_script = sh_path if sh_isfile else py_path
        log.info(f'Found {action} script: {action_script}')
        return action_script

    log.info(f'No {action} script found')
    return None
