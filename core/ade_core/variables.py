#!/usr/bin/env python3

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import os

from datetime import datetime, timezone
from logging import Logger
from pathlib import Path

# these are legacy names for environment variables.
# each key is the current (correct) name for the environment variable,
# and the value holds an array of previous names for the variable.
# we check the each key's legacy names array in order, so the array
# should be ordered newest (most recent) to oldest
_ADE_LEGACY_VARS = {
    'ADE_DEVCENTER_NAME': ['ADE_DEVCENTER'],
    'ADE_PROJECT_NAME': ['ADE_PROJECT'],
    'ADE_ACTION_NAME': ['ACTION_NAME'],
    'ADE_ACTION_OUTPUT': ['ACTION_OUTPUT'],
    'ADE_ACTION_STORAGE': ['ACTION_STORAGE'],
    'ADE_ACTION_TEMP': ['ACTION_TEMP'],
    'ADE_ACTION_PARAMETERS': ['ACTION_PARAMETERS'],
    'ADE_CATALOG': ['CATALOG'],
    'ADE_CATALOG_ITEM': ['CATALOG_ITEM'],
    'ADE_ENVIRONMENT_SUBSCRIPTION_ID': ['ENVIRONMENT_SUBSCRIPTION_ID'],
    'ADE_ENVIRONMENT_RESOURCE_GROUP_NAME': ['ENVIRONMENT_RESOURCE_GROUP_NAME'],
}


def _getenv(key: str, required=True) -> str:
    '''helper function to get the value of environment variables'''

    value = os.environ.get(key)

    # if we didn't find a value, check if we know
    # about legacy names for the environment variable
    if not value and key in _ADE_LEGACY_VARS:

        # try each legacy value in order
        for legacy in _ADE_LEGACY_VARS[key]:

            # if we find a value using the legacy key
            # set (correct) environment variable the value
            if (value := os.environ.get(legacy)):
                os.environ[key] = value
                break

    if required and not value:
        # if we didn't find a value, throw
        raise Exception(f'{key} required environment variable not set')

    return value


def _getenv_bool(key: str) -> bool:
    value = _getenv(key, required=False)
    return bool(value)


# ADE_DEBUG variable can be set by a script after initial import
# so it must be a function to return the most current value
# if set to true, scripts should propagate to tools they use
# e.g. pass the --debug flag to the az cli
def ade_debug() -> bool:
    return _getenv_bool('ADE_DEBUG')


# if a env var starts with one of the following, log it
_ADE_ENV_PREFIXES = ('ADE_', 'RUNNER_', 'AZURE_', 'ARM_', 'MSI_')

# if a env var key contains these words, don't log it
_ADE_SENSITIVE_KEYS = ('SECRET', 'PASSWORD', 'TOKEN', 'PRIVATE', '_KEY', 'USER')


def log_env_vars(log: Logger):
    '''Prints all relevant environment variables to the log'''
    for key, value in os.environ.items():
        key_upper = key.upper()
        if key_upper.startswith(_ADE_ENV_PREFIXES):
            log_value = '****' if any(x in key_upper for x in _ADE_SENSITIVE_KEYS) else value
            log.info(f'{key}: {log_value}')


# hard code this for now
ADE_ACTION_REPOSITORY = '/mnt/repository'

# the core docker image will always set ADE_RUNNER to 1
# this allows scripts behave differently when they are
# executed locally vs. in the runner container
IN_RUNNER = _getenv_bool('ADE_RUNNER')

# when testing containers locally, we need to mock some
# configuration (like mounted volumes).
RUNNER_LOCAL_BUILD = _getenv_bool('RUNNER_LOCAL_BUILD')

# create a shared timestamp for scripts to use
ADE_TIMESTAMP = datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')
os.environ['ADE_TIMESTAMP'] = ADE_TIMESTAMP

ADE_PROJECT_NAME = _getenv('ADE_PROJECT_NAME')
ADE_DEVCENTER_NAME = _getenv('ADE_DEVCENTER_NAME')

ADE_ACTION_NAME = _getenv('ADE_ACTION_NAME')
ADE_ACTION_OUTPUT = _getenv('ADE_ACTION_OUTPUT')
ADE_ACTION_STORAGE = _getenv('ADE_ACTION_STORAGE')
ADE_ACTION_TEMP = _getenv('ADE_ACTION_TEMP')

ADE_ACTION_PARAMETERS = _getenv('ADE_ACTION_PARAMETERS', required=False)

ADE_CATALOG = _getenv('ADE_CATALOG')
# resolve the path to make it absolute, resolving all symlinks on the way and also normalizing it
ADE_CATALOG = Path(ADE_CATALOG).resolve().as_posix()

ADE_CATALOG_ITEM = _getenv('ADE_CATALOG_ITEM')

# ADE_CATALOG is the path to the catalog folder, but ADE_CATALOG_ITEM is the name of the catalog item
# so we'll ADE_CATALOG_ITEM_NAME with the initial value of ADE_CATALOG_ITEM
if (ADE_CATALOG_ITEM_NAME := ADE_CATALOG_ITEM):
    os.environ['ADE_CATALOG_ITEM_NAME'] = ADE_CATALOG_ITEM_NAME

# and update the value of ADE_CATALOG_ITEM to represent the path to the item
if (ADE_CATALOG_ITEM := (Path(ADE_CATALOG) / ADE_CATALOG_ITEM_NAME).resolve().as_posix()):
    os.environ['ADE_CATALOG_ITEM'] = ADE_CATALOG_ITEM

# ADE_TEMPLATE_PATH should always be treated as a relative path (I think)
# so strip './' or '/' prefix from the path so we can resolve the absolute path
# for the value of ADE_CATALOG_ITEM_TEMPLATE
if (ADE_TEMPLATE_PATH := _getenv('ADE_TEMPLATE_PATH')):
    if ADE_TEMPLATE_PATH.startswith('./'):
        ADE_TEMPLATE_PATH = ADE_TEMPLATE_PATH[2:]
    if ADE_TEMPLATE_PATH.startswith('/'):
        ADE_TEMPLATE_PATH = ADE_TEMPLATE_PATH[1:]

# use ADE_TEMPLATE_PATH to resolve the full path to the template file
ADE_CATALOG_ITEM_TEMPLATE = (Path(ADE_CATALOG_ITEM) / ADE_TEMPLATE_PATH).resolve().as_posix()
os.environ['ADE_CATALOG_ITEM_TEMPLATE'] = ADE_CATALOG_ITEM_TEMPLATE


ADE_ENVIRONMENT_TYPE = _getenv('ADE_ENVIRONMENT_TYPE')
ADE_ENVIRONMENT_NAME = _getenv('ADE_ENVIRONMENT_NAME')
ADE_ENVIRONMENT_LOCATION = _getenv('ADE_ENVIRONMENT_LOCATION')

ADE_ENVIRONMENT_SUBSCRIPTION_ID = _getenv('ADE_ENVIRONMENT_SUBSCRIPTION_ID')
ADE_ENVIRONMENT_RESOURCE_GROUP_NAME = _getenv('ADE_ENVIRONMENT_RESOURCE_GROUP_NAME')

# add convenience variable for the environment subscription's full resource id
ADE_ENVIRONMENT_SUBSCRIPTION = f'/subscriptions/{ADE_ENVIRONMENT_SUBSCRIPTION_ID}'
os.environ['ADE_ENVIRONMENT_SUBSCRIPTION'] = ADE_ENVIRONMENT_SUBSCRIPTION

# add convenience variable for the full resource id of the environment resource group
ADE_ENVIRONMENT_RESOURCE_GROUP_ID = f'/subscriptions/{ADE_ENVIRONMENT_SUBSCRIPTION_ID}/resourceGroups/{ADE_ENVIRONMENT_RESOURCE_GROUP_NAME}'
os.environ['ADE_ENVIRONMENT_RESOURCE_GROUP_ID'] = ADE_ENVIRONMENT_RESOURCE_GROUP_ID


if IN_RUNNER:
    if RUNNER_LOCAL_BUILD:
        # for testing containers locally, create folders to simulate
        # the runners mounted volumes (e.g. /mnt/storage)
        for volume in [ADE_ACTION_STORAGE, ADE_ACTION_TEMP, ADE_ACTION_REPOSITORY]:
            Path(volume).resolve().mkdir(parents=True, exist_ok=True)

    # ensure the ADE_ACTION_OUTPUT file is created
    Path(ADE_ACTION_OUTPUT).resolve().touch(exist_ok=True)

    if RUNNER_LOCAL_BUILD:
        # for testing containers locally, we don't actually
        # mount a catalog repo so we create it here
        Path(ADE_CATALOG_ITEM).resolve().mkdir(parents=True, exist_ok=True)

        # then make sure the catalog item's template exists
        Path(ADE_CATALOG_ITEM_TEMPLATE).resolve().touch(exist_ok=True)

# the runner should always set this to true but custom action
# scripts may want to log in using a service principal. to do
# so they would set ARM_USE_MSI to false in that script and
# set AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET
ARM_USE_MSI = _getenv_bool('ARM_USE_MSI')

ARM_TENANT_ID = _getenv('ARM_TENANT_ID')
ARM_SUBSCRIPTION_ID = _getenv('ARM_SUBSCRIPTION_ID')
# ARM_RESOURCE_GROUP_NAME = _getenv('ARM_RESOURCE_GROUP_NAME')

RUNNER_ACTIONS_DIRECTORY = Path('/actions.d') if IN_RUNNER else Path(__file__).resolve().parent.parent / 'actions.d'
os.environ['RUNNER_ACTIONS_DIRECTORY'] = RUNNER_ACTIONS_DIRECTORY.as_posix()

RUNNER_ENTRYPOINT_DIRECTORY = Path('/entrypoint.d') if IN_RUNNER else Path(__file__).resolve().parent.parent / 'entrypoint.d'
os.environ['RUNNER_ENTRYPOINT_DIRECTORY'] = RUNNER_ENTRYPOINT_DIRECTORY.as_posix()
