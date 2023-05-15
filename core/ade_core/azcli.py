#!/usr/bin/env python3

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import json
import os
import shutil
import subprocess

from .logger import error_exit, get_logger, trace
from .variables import (ADE_ENVIRONMENT_LOCATION, ADE_ENVIRONMENT_RESOURCE_GROUP_NAME, ADE_ENVIRONMENT_SUBSCRIPTION_ID,
                        ARM_USE_MSI, ade_debug)

log = get_logger(__name__)


def cli(command, log_command=True, log_output=True):
    '''Runs an azure cli command and returns the json response'''
    if isinstance(command, list):
        args = command
    elif isinstance(command, str):
        args = command.split()
    else:
        error_exit(log, f'az command must be a string or list, not {type(command)}')

    # resolve the full path to az (e.g. /usr/local/bin/az)
    az = shutil.which('az')

    # remove 'az' from the command
    if args[0] == 'az':
        args.pop(0)

    # add the full path to az
    if args[0] != az:
        args = [az] + args

    debug = ade_debug()

    if debug and '--debug' not in args:
        args.append('--debug')

    try:
        if log_command == False:
            # we still want to log the core command without the user-provided arguments,
            # so we find the index of the first arg starting with '-' and only log the args before
            # e.g. command: 'az login -u foo -p bar --tenant baz', will log: "az login ****"
            if (first_arg := next((i for i, a in enumerate(args) if a.startswith('-')), -1)) != -1:
                trace(log, f'Running az cli command: {" ".join(args[:first_arg])} ****')
        else:
            trace(log, f'Running az cli command: {" ".join(args)}')

        proc = subprocess.run(args, capture_output=True, check=True, text=True)

        if proc.returncode == 0 and not proc.stdout:
            return None

        if log_output:
            for line in proc.stdout.splitlines():
                log.info(line)

        resource = json.loads(proc.stdout)
        return resource

    except subprocess.CalledProcessError as e:
        if e.stderr and 'Code: ResourceNotFound' in e.stderr:
            return None
        error_exit(log, e.stderr if e.stderr else 'azure cli command failed')
    except json.decoder.JSONDecodeError:
        error_exit(log, '{}: {}'.format('Could not decode response json', proc.stderr if proc.stderr else proc.stdout if proc.stdout else proc))


def login():
    trace(log, 'Signing in to Azure CLI')

    az_client_id = os.environ.get('AZURE_CLIENT_ID')
    az_client_secret = os.environ.get('AZURE_CLIENT_SECRET')
    az_tenant_id = os.environ.get('AZURE_TENANT_ID')

    if ARM_USE_MSI:
        log.info(f'No credentials for Azure Service Principal')
        log.info(f'Logging in to Azure with managed identity')
        cli('az login --identity --allow-no-subscriptions')
    elif az_client_id and az_client_secret and az_tenant_id:
        log.info(f'Found credentials for Azure Service Principal')
        log.info(f'Logging in with Service Principal')
        cli(f'az login --service-principal -u {az_client_id} -p {az_client_secret} -t {az_tenant_id} --allow-no-subscriptions', log_command=False)

    if ADE_ENVIRONMENT_SUBSCRIPTION_ID:
        trace(log, f'Setting subscription to {ADE_ENVIRONMENT_SUBSCRIPTION_ID}')
        cli(f'az account set --subscription {ADE_ENVIRONMENT_SUBSCRIPTION_ID}')


def set_defaults():
    trace(log, 'Setting Azure CLI defaults')
    cli(f'az configure -d location={ADE_ENVIRONMENT_LOCATION}')
    cli(f'az configure -d group={ADE_ENVIRONMENT_RESOURCE_GROUP_NAME}')
    cli('az configure -l')
