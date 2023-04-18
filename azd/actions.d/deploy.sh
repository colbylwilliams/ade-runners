#!/bin/bash

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -e # exit on error

trace() {
    echo -e "\n>>> $@ ...\n"
}

# AZURE_ENV_NAME is the name of the key used to store the envname property in the environment.
AZURE_ENV_NAME="$ADE_ENVIRONMENT_TYPE"

# AZURE_LOCATION is the name of the key used to store the location property in the environment.
AZURE_LOCATION="$ADE_ENVIRONMENT_LOCATION"

# AZURE_SUBSCRIPTION_ID is the name of they key used to store the subscription id property in the environment.
AZURE_SUBSCRIPTION_ID="$ADE_ENVIRONMENT_SUBSCRIPTION_ID"

# AZURE_PRINCIPAL_ID is the name of they key used to store the id of a principal in the environment.
# AZURE_PRINCIPAL_ID="$AZURE_PRINCIPAL_ID"

# AZURE_TENANT_ID is the tenant that owns the subscription
AZURE_TENANT_ID="$ARM_TENANT_ID"

# AZURE_CONTAINER_REGISTRY_ENDPOINT is the name of they key used to store the endpoint of the container registry to push to.
# AZURE_CONTAINER_REGISTRY_ENDPOINT="$AZURE_CONTAINER_REGISTRY_ENDPOINT"

# AZURE_AKS_CLUSTER_NAME is the name of they key used to store the endpoint of the AKS cluster to push to.
# AZURE_AKS_CLUSTER_NAME="$AZURE_AKS_CLUSTER_NAME"

# AZURE_RESOURCE_GROUP is the name of the azure resource group that should be used for deployments
AZURE_RESOURCE_GROUP="$ADE_ENVIRONMENT_RESOURCE_GROUP_NAME"

trace "Running: azd --help"
azd --help

trace "Running: azd version"
azd version

trace "Running: git version"
git --version

trace "Setting up git config"

echo "Setting git user.name to ade"
git config --global user.name "ade"

echo "Setting git usere.mail to ade@microsoft.com"
git config --global user.email "ade@microsoft.com"

trace "Running: azd init -t todo-python-mongo"
azd init --template todo-python-mongo \
    --cwd $ADE_ACTION_TEMP \
    --environment $ADE_ENVIRONMENT_TYPE \
    --location $ADE_ENVIRONMENT_LOCATION \
    --subscription $ADE_ENVIRONMENT_SUBSCRIPTION_ID \
    --no-prompt
