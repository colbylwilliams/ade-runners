#!/bin/bash

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

DIR=$(dirname "$0")
. $DIR/_common.sh

deploymentName=$(date +"%Y-%m-%d-%H%M%S")

echo -e "Deleting resource group: $ADE_ENVIRONMENT_RESOURCE_GROUP_NAME"

deploymentOutput=$(az deployment group create --resource-group "$ADE_ENVIRONMENT_RESOURCE_GROUP_NAME" \
                                              --name "$deploymentName" \
                                              --no-prompt true --no-wait --mode Complete \
                                              --template-file "$DIR/empty.json" 2>&1)

echo $deploymentOutput

if [ $? -eq 0 ]; then # deployment successfully created
    while true; do

        sleep 1

        ProvisioningState=$(az deployment group show --resource-group "$ADE_ENVIRONMENT_RESOURCE_GROUP_NAME" --name "$deploymentName" --query "properties.provisioningState" -o tsv)
        ProvisioningDetails=$(az deployment operation group list --resource-group "$ADE_ENVIRONMENT_RESOURCE_GROUP_NAME" --name "$deploymentName")

        trackDeployment "$ProvisioningDetails"

        if [[ "CANCELED|FAILED|SUCCEEDED" == *"${ProvisioningState^^}"* ]]; then

            echo -e "\nDeployment $deploymentName: $ProvisioningState"

            if [[ "CANCELED|FAILED" == *"${ProvisioningState^^}"* ]]; then
                exit 1
            else
                break
            fi
        fi

    done
fi

# trim spaces from output to avoid issues in the following (generic) error section
deploymentOutput=$(echo "$deploymentOutput" | sed -e 's/^[[:space:]]*//')

if [ ! -z "$deploymentOutput" ]; then

    if [ $(echo "$deploymentOutput" | jq empty > /dev/null 2>&1; echo $?) -eq 0 ]; then

        deploymentOutput="$( echo $deploymentOutput | jq --raw-output '.[] | .details[] | "Error: \(.message)\n"' | sed 's/\\n/\n/g'  )"

    fi

    echo "$deploymentOutput" && exit 1 # our script failed to enqueue a new deployment - we return a non-zero exit code to inidicate this

fi
