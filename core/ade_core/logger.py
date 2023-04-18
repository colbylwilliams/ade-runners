#!/usr/bin/env python3

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import logging
import sys

from .variables import ADE_ACTION_OUTPUT, ade_debug


def get_logger(name):
    '''Get the logger for the script'''
    _debug = ade_debug()

    _logger = logging.getLogger(name)
    _logger.setLevel(logging.DEBUG if _debug else logging.INFO)

    formatter = logging.Formatter('{asctime} {levelname:<8}: {message}',
                                  datefmt='%m/%d/%Y %I:%M:%S %p', style='{',)
    ch = logging.StreamHandler()
    ch.setLevel(level=_logger.level)
    ch.setFormatter(formatter)
    _logger.addHandler(ch)

    fh = logging.FileHandler(ADE_ACTION_OUTPUT)
    fh.setLevel(level=_logger.level)
    fh.setFormatter(formatter)
    _logger.addHandler(fh)

    return _logger


def trace(log: logging.Logger, message):
    log.info('')
    log.info(f'>>> {message} ...')
    log.info('')


def error_exit(log: logging.Logger, message):
    log.error(message)
    sys.exit(message)
