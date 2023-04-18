#!/bin/bash

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

trace() {
    echo -e "\n>>> $@ ..."
}

trace "Running: azd --help"
azd --help

trace "Running: azd template list"
azd template list

# tail -f /dev/null
