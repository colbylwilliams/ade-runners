#!/bin/bash

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -e # exit on error

trace() {
    echo -e "\n>>> $@ ...\n"
}

trace "Running: azd --help"
azd --help

trace "Running: azd template list"
azd template list
