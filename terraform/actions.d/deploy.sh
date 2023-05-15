#!/bin/bash

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -e # exit on error

trace() {
    echo -e "\n>>> $@ ..."
}

readonly EnvironmentState="$ADE_ACTION_STORAGE/environment.tfstate"
readonly EnvironmentPlan="$ADE_ACTION_TEMP/environment.tfplan"
readonly EnvironmentVars="$ADE_ACTION_TEMP/environment.tfvars.json"

echo "$ADE_ACTION_PARAMETERS" > $EnvironmentVars

# https://developer.hashicorp.com/terraform/cli/config/environment-variables#tf_input
export TF_INPUT=0

# https://developer.hashicorp.com/terraform/cli/config/environment-variables#tf_cli_args-and-tf_cli_args_name
TF_CLI_ARGS="-input=false"

# https://developer.hashicorp.com/terraform/cli/config/environment-variables#tf_in_automation
export TF_IN_AUTOMATION=true

trace "Terraform Info"
terraform -version

trace "Initializing Terraform"
terraform init -no-color

trace "Creating Terraform Plan"
terraform plan -no-color -compact-warnings -refresh=true -lock=true -state=$EnvironmentState -out=$EnvironmentPlan -var-file="$EnvironmentVars" -var "resource_group_name=$ADE_ENVIRONMENT_RESOURCE_GROUP_NAME"

trace "Applying Terraform Plan"
terraform apply -no-color -compact-warnings -auto-approve -lock=true -state=$EnvironmentState $EnvironmentPlan
