#!/bin/bash

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -e # exit on error
trap 'catch $? $LINENO' EXIT

catch() {
    if [ "$1" != "0" ]; then
        # we trapped an error - write some reporting output
        error "Exit code $1 was returned from line #$2 !!!"
    fi

    # if [ $ADE_BLOCK_ON_FAIL == "true" ]; then
    #     echo "Blocking for 600s."
    #     sleep 600s
    # fi
}

trace() {
    echo -e "\n>>> $@ ...\n"
}

error() {
    echo "Error: $@" 1>&2
}

logEnvironment() {
    trace "Listing relevant environment variables"
    echo "ACTION_NAME: $ACTION_NAME"
    echo "ACTION_OUTPUT: $ACTION_OUTPUT"
    echo "ACTION_STORAGE: $ACTION_STORAGE"
    echo "ACTION_TEMP: $ACTION_TEMP"
    echo "ACTION_PARAMETERS: **REDACTED**"
    echo "CATALOG: $CATALOG"
    echo "CATALOG_ITEM: $CATALOG_ITEM"
    echo "ENVIRONMENT_RESOURCE_GROUP_NAME: $ENVIRONMENT_RESOURCE_GROUP_NAME"

    trace "Listing relevant ARM environment variables"
    echo "MSI_ENDPOINT: $MSI_ENDPOINT"
    echo "ARM_MSI_ENDPOINT: $ARM_MSI_ENDPOINT"
    echo "ARM_USE_MSI: $ARM_USE_MSI"
    echo "ARM_TENANT_ID: $ARM_TENANT_ID"
    echo "ARM_SUBSCRIPTION_ID: $ARM_SUBSCRIPTION_ID"
    echo "ARM_RESOURCE_GROUP_NAME: $ARM_RESOURCE_GROUP_NAME"
}

logEnvironment

mkdir -p "$(dirname "$ACTION_OUTPUT")"  # ensure the log folder exists
touch $ACTION_OUTPUT                    # ensure the log file exists

# exec 1>$ACTION_OUTPUT                   # forward stdout to log file
# exec 2>&1                               # redirect stderr to stdout


find "/entrypoint.d/" -follow -type f -iname "*.sh" -print | sort -n | while read -r f; do
    # execute each shell script found enabled for execution
    if [ -x "$f" ]; then trace "Running '$f'"; "$f"; fi
done

trace "Connecting to Azure"

if [ $ARM_USE_MSI ]; then
    trace "Signing in using MSI"
    while true; do
        # managed identity isn't available immediately
        # we need to do retry after a short nap
        az login --identity --allow-no-subscriptions --only-show-errors --output none && {
            echo "done"
            break
        } || sleep 5
    done
elif [[ ! -z "$AZURE_CLIENT_ID" && ! -z "$AZURE_CLIENT_SECRET" && ! -z "$AZURE_TENANT_ID" ]]; then
    trace "Signing in using service principal"
    az login --service-principal --username "$AZURE_CLIENT_ID" --password "$AZURE_CLIENT_SECRET" --tenant "$AZURE_TENANT_ID" --allow-no-subscriptions --only-show-errors --output none
    echo "done"
else
    trace "No Azure MSI or service principal credentials found"
fi

if [[ ! -z "$ENVIRONMENT_SUBSCRIPTION_ID" ]]; then
    trace "Selecting Subscription"
    az account set --subscription $ENVIRONMENT_SUBSCRIPTION_ID
    echo "$(az account show -o json | jq --raw-output '"\(.name) (\(.id))"')"
fi

if [[ ! -z "$CATALOG" ]]; then
    trace "Selecting Catalog directory"
    cd $(echo "$CATALOG" | sed 's/^file:\/\///') && echo $PWD
else
    trace "Selecting default Catalog directory"
    cd "Catalog" && echo $PWD
fi
ls


if [[ ! -z "$CATALOG_ITEM" ]]; then
    trace "Selecting Catalog Item directory"
    cd $(echo "$CATALOG_ITEM" | sed 's/^file:\/\///') && echo $PWD
fi
ls

# the script to execute is defined by the following options
# (the first option matching an executable script file wins)
#
# Option 1: a script path is provided as docker CMD command
#
# Option 2: a script file following the pattern [ACTION_NAME].sh exists in the
#           current working directory (catalog item directory)
#
# Option 3: a script file following the pattern [ACTION_NAME].sh exists in the
#           /actions.d directory (actions script directory)

script="$@"

if [[ -z "$script" ]]; then
    script="$(find $PWD -maxdepth 1 -iname "$ACTION_NAME.sh")"
    if [[ -z "$script" ]]; then
        script="$(find /actions.d -maxdepth 1 -iname "$ACTION_NAME.sh")"
    fi
    if [[ -z "$script" ]]; then
        error "Action $ACTION_NAME is not supported." && exit 1
    fi
fi

if [[ -f "$script" && -x "$script" ]]; then
    # lets execute the task script - isolate execution in sub shell
    trace "Executing script ($script)"; ( exec "$script"; exit $? ) || exit $?
elif [[ -f "$script" ]]; then
    error "Script '$script' is not marked as executable" && exit 1
else
    error "Script '$script' does not exist" && exit 1
fi
