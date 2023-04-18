#!/usr/bin/env python3

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import argparse
import sys

from pathlib import Path

import ade_core.azcli as az
import ade_core.scripts as scripts

from ade_core.logger import error_exit, get_logger, trace
from ade_core.variables import (ADE_ACTION_NAME, ADE_CATALOG_ITEM, ADE_CATALOG_ITEM_TEMPLATE, IN_RUNNER,
                                RUNNER_ACTIONS_DIRECTORY, RUNNER_ENTRYPOINT_DIRECTORY, log_env_vars)

parser = argparse.ArgumentParser(description='Run an action')
parser.add_argument('script', help='The script to run', default=None, nargs='?')

args = parser.parse_args()
cmd_input = args.script

log = get_logger(__name__)

log.info('##################################')
log.info('Azure Depoyment Environment Runner')
log.info('##################################')
log.info('')
log.info(f'IN_RUNNER: {IN_RUNNER}')

log.info('')
log.info('Environment variables:')
log.info('======================')
log_env_vars(log)

# ensure the path to the catalog item is an existing directory
if not Path(ADE_CATALOG_ITEM).resolve().is_dir():
    error_exit(log, f'Catalog item {ADE_CATALOG_ITEM} not found')

# ensure the path to the catalog item template is a valid file path
if not Path(ADE_CATALOG_ITEM_TEMPLATE).resolve().is_file():
    error_exit(log, f'Catalog item template {ADE_CATALOG_ITEM_TEMPLATE} not found')

# if this image is used as a base for a custom image, the user can
# add files to the /entrypoint.d directory to be executed at startup
trace(log, f'Checking for entrypoint scripts in {RUNNER_ENTRYPOINT_DIRECTORY}')

if RUNNER_ENTRYPOINT_DIRECTORY.is_dir():
    scripts.run_all(RUNNER_ENTRYPOINT_DIRECTORY)

if IN_RUNNER:
    az.login()

# az.login will set the default sub to ADE_ENVIRONMENT_SUBSCRIPTION_ID
sub = az.cli('az account show')
log.info(f'Current subscription: {sub["name"]} ({sub["id"]})')


# the action script to execute is defined by the following options
# (the first option matching an executable script file wins)
#
# Option 1: a script path is provided as docker CMD command
#
# Option 2: a script file following the pattern [ADE_ACTION_NAME].[sh|py]
#           exists in the ADE_CATALOG_ITEM directory
#
# Option 3: a script file following the pattern [ADE_ACTION_NAME].[sh|py]
#           exists in the /actions.d directory (actions script directory)


path = None

trace(log, f'Checking for {ADE_ACTION_NAME} script in docker CMD')
if cmd_input:
    log.info(f'CMD input found: {cmd_input}')
    cmd_input = Path(cmd_input).resolve()

    if not cmd_input.is_file():
        log.info(f'CMD input script is not a file, ignoring: ({cmd_input})')

    elif cmd_input.suffix != '.sh' and cmd_input.suffix != '.py':
        error_exit(log, f'Invalid script type provided in CMD input: {cmd_input} (only .sh and .py scripts are supported)')

    else:
        path = cmd_input
else:
    log.info('No {ADE_ACTION_NAME} script found in docker CMD')

if path is None:
    trace(log, f'Checking for {ADE_ACTION_NAME} script catalog item folder')
    path = scripts.get_action_script(ADE_CATALOG_ITEM, ADE_ACTION_NAME)

if path is None:
    trace(log, f'Checking for {ADE_ACTION_NAME} runner actions folder')
    path = scripts.get_action_script(RUNNER_ACTIONS_DIRECTORY, ADE_ACTION_NAME)

if path is not None:
    scripts.run(path, ADE_CATALOG_ITEM)
    log.info('')
    log.info('Done.')
    sys.exit(0)
else:
    error_exit(log, f'No script found for action: {ADE_ACTION_NAME}')
